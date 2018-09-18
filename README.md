# MTAnchor

Repository contains demo code for MTAnchor, an interactive, multilingual topic modeling system.  The code accompanies the paper _Multilingual Anchoring: Interactive Topic Modeling and Alignment Across Languages_ (Yuan et al., 2018).

## Dependencies
- Python 3
- Numpy
- Scipy
- Scikit-learn
- Flask 
- Flask_sqlalchemy 
- Flask_migrate 
- [Anchor-topic](https://github.com/forest-snow/anchor-topic) 

All above packages can be installed with ```pip install```.

## Setup
- Clone repository: ```git clone https://github.com/forest-snow/mtanchor_demo.git```
- Move to folder: ```cd mtanchor_demo```
- Install dependencies: ```pip install -r requirements.txt```
- Run bash script: ```./mtanchor.sh```
- Go to ```http://127.0.0.1:5000/``` in your browser

## Usage
- **Read** over _Multilingual Anchoring: Interactive Topic Modeling and Alignment Across Languages_ to understand how MTAnchor works.
- **Look** at the most likely words for each topic in the blue boxes and the anchor words in the purple boxes. 
- **Move** words from blue boxes to purple boxes to add them as anchors (note that interface will not let you mix words from languages).  You may also remove words from the purple boxes to delete them as anchors.
- **Hover** over words to see their translation (if available).
- **Click** on words to see occurrences of words and their translations highlighted across the interface.
- **Search** for words and see what words exist in the corpora. Once you have selected a word from the dropdown menu, then you have the option of adding the word and/or its translation as an anchor to the topic.
- **Add or remove** topics from the interface.
- **Update** topics with your newly chosen anchors (note that interface will not let you update topics if no anchor word is chosen).
- **Restart** your progress if you want to start over.
- **End** app with ```Ctrl+C```.

## Memory space
The demo uses a SQLite database (stored in your local files) to save data.  Since this is only a demo, only top 1000 words from each corpus is included in the vocabulary.  The demo doesn't let user submit their results to prevent database from getting too large. If you find that the database is taking up too much space, run ```delete_db.sh``` to delete all data from the database.

## See also
- Interface was initially based upon Jeff Lund's [tbuie interface](https://github.com/byu-aml-lab/tbuie).
- Topic model is built using code from [anchor-topic](https://github.com/forest-snow/anchor-topic) package.

## Citation
```sh
@inproceedings{yuan2018mtanchor,
  title={Multilingual Anchoring: Interactive Topic Modeling and Alignment Across Languages},
  author={Yuan, Michelle and Van Durme, Benjamin and Boyd-Graber, Jordan},
  booktitle={Advances in neural information processing systems},
  year={2018}
}
```
## License
Copyright (C) 2018, Michelle Yuan

Licensed under the terms of the MIT License. A full copy of the license can be found in LICENSE.
