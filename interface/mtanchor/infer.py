# EM Algorithm code adapted from python-topic-model
# https://github.com/arongdari/python-topic-model
import numpy 
from sklearn.decomposition import LatentDirichletAllocation 
from scipy.special import gammaln, psi
import multiprocessing.pool



def variational_bayes(word_doc, topic_word):
    n_topics = topic_word.shape[0]
    n_words, n_docs = word_doc.shape
    model = vbLDA(n_docs, n_words, n_topics, topic_word)
    doc_ids = []
    doc_cnt = []
    for doc in range(n_docs):

        doc_start = word_doc.indptr[doc]
        doc_end = word_doc.indptr[doc + 1]


        doc_ids.append(word_doc.indices[doc_start: doc_end])
        doc_cnt.append(word_doc.data[doc_start: doc_end])

    model.fit(doc_ids, doc_cnt)
    gamma = model.gamma 
    for d in range(n_docs):
        if numpy.isnan(gamma[d,:]).any():
            gamma[d] = numpy.ones(n_topics) / n_topics
    gamma = gamma / gamma.sum(axis=1)[:, numpy.newaxis]
    return gamma




def dirichlet_expectation(alpha):
    if len(alpha.shape) == 1:
        return psi(alpha) - psi(numpy.sum(alpha))
    return psi(alpha) - psi(numpy.sum(alpha, 1))[:, numpy.newaxis]


class vbLDA:
    """
    Latent dirichlet allocation,
    Blei, David M and Ng, Andrew Y and Jordan, Michael I, 2003
    Latent Dirichlet allocation with mean field variational inference
    """

    def __init__(self, n_doc, n_voca, n_topic, topic_word, alpha=0.1, beta=0.01, is_compute_bound=False):
        self.n_voca = n_voca
        self.n_topic = n_topic
        self.n_doc = n_doc
        self.alpha = alpha
        self.beta = beta

        self._lambda = topic_word
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = numpy.exp(self._Elogbeta)
        self.gamma_iter = 5
        self.gamma = 1 * numpy.random.gamma(100., 1. / 100, (self.n_doc, self.n_topic))

        self.is_compute_bound = is_compute_bound


    def fit(self, doc_ids, doc_cnt, max_iter=1):

        for i in range(max_iter):
            _, bound = self.do_m_step(doc_ids, doc_cnt)
 


    def do_e_step(self, doc_ids, doc_cnt):
        """
        compute approximate topic distribution of each document and each word
        """
        
        Elogtheta = dirichlet_expectation(self.gamma)
        expElogtheta = numpy.exp(Elogtheta)


        sstats = numpy.zeros(self._lambda.shape)

        def e_step(d):
            ids = doc_ids[d]
            cnt = numpy.array(doc_cnt[d])
            if numpy.sum(cnt) != 0:

                gammad = self.gamma[d, :]

                expElogthetad = expElogtheta[d, :]
                expElogbetad = self._expElogbeta[:, ids]
                phinorm = numpy.dot(expElogthetad, expElogbetad) + 1e-100

                for iter in range(self.gamma_iter):
                    lastgamma = gammad

                    gammad = self.alpha + expElogthetad * numpy.dot(cnt / phinorm, expElogbetad.T)

                    Elogthetad = dirichlet_expectation(gammad)
                    expElogthetad = numpy.exp(Elogthetad)
                    phinorm = numpy.dot(expElogthetad, expElogbetad) + 1e-100

                    meanchange = numpy.mean(abs(gammad - lastgamma))

                    if (meanchange < 1e-3):
                        break

                self.gamma[d, :] = gammad
                sstats[:, ids] += numpy.outer(expElogthetad.T, cnt / phinorm)


        worker = lambda d: e_step(d)
        chunksize =  5000
        with multiprocessing.pool.ThreadPool() as pool:
            pool.map(worker, range(self.n_doc), chunksize)

        sstats = sstats * self._expElogbeta

        return (self.gamma, sstats)




    def do_m_step(self, doc_ids, doc_cnt):
        """
        estimate topic distribution based on computed approx. topic distribution
        """
        (gamma, sstats) = self.do_e_step(doc_ids, doc_cnt)

        self._lambda = self.beta + sstats
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = numpy.exp(self._Elogbeta)

        bound = 0
        if self.is_compute_bound:
            bound = self.approx_bound(doc_ids, doc_cnt, gamma)

        return gamma, bound



    def approx_bound(self, doc_ids, doc_cnt, gamma):
        """
        Compute lower bound of the corpus
        """

        score = 0
        Elogtheta = dirichlet_expectation(gamma)

        # E[log p(docs | theta, beta)]
        for d in range(0, self.n_doc):
            ids = doc_ids[d]
            cts = numpy.array(doc_cnt[d])
            phinorm = numpy.zeros(len(ids))
            for i in range(0, len(ids)):
                temp = Elogtheta[d, :] + self._Elogbeta[:, ids[i]]
                tmax = max(temp)
                phinorm[i] = numpy.log(sum(numpy.exp(temp - tmax))) + tmax
            score += numpy.sum(cts * phinorm)

        # E[log p(theta | alpha) - log q(theta | gamma)]
        score += numpy.sum((self.alpha - gamma) * Elogtheta)
        score += numpy.sum(gammaln(gamma) - gammaln(self.alpha))
        score += sum(gammaln(self.alpha * self.n_topic) - gammaln(numpy.sum(gamma, 1)))

        # E[log p(beta | eta) - log q (beta | lambda)]
        score = score + numpy.sum((self.beta - self._lambda) * self._Elogbeta)
        score = score + numpy.sum(gammaln(self._lambda) - gammaln(self.beta))
        score = score + numpy.sum(gammaln(self.beta * self.n_voca) - gammaln(numpy.sum(self._lambda, 1)))

        return score



