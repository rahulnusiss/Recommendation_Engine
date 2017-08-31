import pandas as pd
import time
#import redis
from numpy import *
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def info(msg):
    current_app.logger.info(msg)


class ContentEngine(object):

    SIMKEY = 'p:smlr:%s'


    def __init__(self):
        """self._r = redis.StrictRedis.from_url(current_app.config['REDIS_URL'])"""
        self._r = zeros((120,2))

    def train(self, data_source):
        start = time.time()
        ds = pd.read_csv(data_source)
        print("Training data ingested in %s seconds." % (time.time() - start))

        # Flush the stale training data from redis
        #self._r.flushdb()

        n = size(ds['id'], axis=0)
        print (n)
        scoreMatrix = [[0 for j in range(n)] for i in range(2)]
        scoreMatrix[0] = ds['id']
        scoreMatrix[0] = scoreMatrix[0].copy()

        start = time.time()
        scoreMatrix2 = self._train(ds, 'description', 'SHOES', scoreMatrix, 1)
        scoreMatrix3 = self._train(ds, 'color', 'BLUE', scoreMatrix2, 1)
        scoreMatrix4 = self._train(ds, 'gender', 'MEN', scoreMatrix3, 5)
        print (scoreMatrix4[1])

        """ Sorting according to score
        Using bubble sort"""
        sorted = False  # We haven't started sorting yet

        while not sorted:
            sorted = True  # Assume the list is now sorted
            for element in range(0, n-1):
                if scoreMatrix4[1][element] < scoreMatrix4[1][element + 1]:
                    sorted = False  # We found two elements in the wrong order
                    hold = scoreMatrix4[1][element + 1]
                    scoreMatrix4[1][element + 1] = scoreMatrix4[1][element]
                    scoreMatrix4[1][element] = hold
                    hold2 = scoreMatrix4[0][element + 1]
                    scoreMatrix4[0][element + 1] = scoreMatrix4[0][element]
                    scoreMatrix4[0][element] = hold2

        print("After Sorting")
        print(scoreMatrix4)
        print("Engine trained in %s seconds." % (time.time() - start))

    def _train(self, ds, attrName, attrValue, scoreMatrix, scoreFactorToAdd):
        """
        Train the engine.
        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product. The 'stop_words' param
        tells the TF-IDF module to ignore common english words like 'the', etc.
        Then we compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).
        Iterate through each item's similar items and store the 100 most-similar. Stops at 100 because well...
        how many similar products do you really need to show?
        Similarities and their scores are stored in redis as a Sorted Set, with one set for each item.
        :param ds: A pandas dataset containing two fields: description & id
        :return: Nothin!
        """
        user = [attrValue]
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tf.fit(ds[attrName])
        #tfidf_matrix = tf.fit_transform(ds['description'])
        tfidf_matrix_user = tf.transform(user)
        tfidf_matrix = tf.transform(ds[attrName])

        cosine_similarities = linear_kernel(tfidf_matrix_user, tfidf_matrix)
        #print (cosine_similarities[0])
        print(size(cosine_similarities, axis = 1))
        print(shape(cosine_similarities))

        n = size(cosine_similarities, axis=1)
        print(n)

        #print(scoreMatrix)
        print(size(scoreMatrix, axis=0))

        scoreMatrix[1] = scoreMatrix[1] + scoreFactorToAdd*cosine_similarities[0]
        #print(scoreMatrix)

        for idx, row in ds.iterrows():
            a = 0
            #similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            #similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

            #similar_items = [(cosine_similarities[idx], user)]

            # First item is the item itself, so remove it.
            # This 'sum' is turns a list of tuples into a single tuple: [(1,2), (3,4)] -> (1,2,3,4)
            #flattened = sum(similar_items[1:], ())
            #print (flattened[0])
            #self._r[idx] = flattened[0]
            #self._r[idx][1] = flattened[1]
            #self._r[idx+1] = (self.SIMKEY % row['id'], *flattened)

        #print (flattened)
        #print(similar_items)

        #print(similar_indices)
        return scoreMatrix

    def predict(self, item_id, num):
        """
        Couldn't be simpler! Just retrieves the similar items and their 'score' from redis.
        :param item_id: string
        :param num: number of similar items to return
        :return: A list of lists like: [["19", 0.2203], ["494", 0.1693], ...]. The first item in each sub-list is
        the item ID and the second is the similarity score. Sorted by similarity score, descending.
        """
        return self._r.zrange(self.SIMKEY % item_id, 0, num-1, withscores=True, desc=True)


content_engine = ContentEngine()