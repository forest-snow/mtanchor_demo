# MTAnchor

Repository contains demo code for MTAnchor, an interactive, multilingual topic modeling system.  The code accompanies the paper _Multilingual Anchoring: Interactive Topic Modeling and Alignment Across Languages_ (Yuan et al., 2018).

# Dependencies
- Numpy
- Scipy
- Flask (0.12)
- Anchor-topic 
- Scikit-learn

All above packages can be installed with ```pip install```.

# Setup
- Clone repository
- Type following commands to start session:
```sh
export FLASK_APP=run.py
flask run
```
- Go to ```http://127.0.0.1:5000/``` in your browser

# Usage
- **Read** over _Multilingual Anchoring: Interactive Topic Modeling and Alignment Across Languages_ to understand how MTAnchor works.
- **Move** words from blue boxes to purple boxes to add them as anchors (note that interface will not let you mix words from languages).  You may also remove words from the purple boxes to delete them as anchors.
- **Hover** over words to see their translation (if available).
- **Click** on words to see occurrences of words and their translations highlighted across the interface.
- **Search** for words and see what words exist in the corpora. Once you have selected a word from the dropdown menu, then you have the option of adding the word and/or its translation as an anchor to the topic.
- **Add or remove** topics from the interface.
- **Update** topics with your newly chosen anchors (note that interface will not let you update topics if no anchor word is chosen).
- **Restart** your progress if you want to start over.

# Memory space
The demo uses a SQLite database (stored in your local files) to save data.  Since this is only a demo, only top 1000 words from each corpus is included in the vocabulary.  The demo doesn't let user submit their results to prevent database from getting too large. It is also recommended to limit number of topics (no more than 20) so that database remains small.

# Citation
```sh
@inproceedings{yuan2018mtanchor,
  title={Multilingual Anchoring: Interactive Topic Modeling and Alignment Across Languages},
  author={Yuan, Michelle and Van Durme, Benjamin and Boyd-Graber, Jordan},
  booktitle={Advances in neural information processing systems},
  year={2018}
}
```
