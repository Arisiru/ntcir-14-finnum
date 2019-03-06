import nltk
nltk.download("stopwords")

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import json
import re
import os


tokenizer = RegexpTokenizer(r"\w+")
system_patern = re.compile("sys[floats|ints|ticker|url]+")

# create English stop words list
en_stop = stopWords = set(stopwords.words("english"))

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
data = json.load(open(os.path.join("..", "data", "features" ,"all_features_0.json")))

# compile sample documents into a list
doc_set = [" ".join(x["features"]["tokens_terms"]) + " " + " ".join(x["features"]["tags"]) for x in data]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    tokens = [i for i in tokens if i not in en_stop]
    tokens = [i for i in tokens if system_patern.match(i) is None]
    # stem tokens
    tokens = [p_stemmer.stem(i) for i in tokens]
    
    # add tokens to list
    texts.append(tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=200)

for indx, entity in enumerate(data):
    topic_distribution = ldamodel.get_document_topics(corpus[indx], minimum_probability=0.0)
    entity["features"]["topic_distr"] = [float(x[1]) for x in topic_distribution]

json.dump(data, open(os.path.join("..", "data", "features" ,"all_features_1.json"), "w"))

