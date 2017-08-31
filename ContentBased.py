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

    def __init__(self):
        """ For intialization TBD"""

    def train(self, data_source):
        start = time.time()
        ds = pd.read_csv(data_source)
        print("Training data ingested in %s seconds." % (time.time() - start))

        n = size(ds['id'], axis=0)

        scoreMatrix = [[0 for j in range(n)] for i in range(2)]
        scoreMatrix[0] = ds['id']
        # Workaround for a panda bug. Better solution TBD
        scoreMatrix[0] = scoreMatrix[0].copy()

        start = time.time()
        scoreMatrix = self._train(ds, 'description', 'SHOES', scoreMatrix, 1)
        scoreMatrix = self._train(ds, 'color', 'BLUE', scoreMatrix, 1)
        scoreMatrix = self._train(ds, 'gender', 'LADIES', scoreMatrix, 6)
        scoreMatrix = self._train(ds, 'gender', 'NEUTER', scoreMatrix, 3)

        #Sort the items in descending order of their score so that most matching items is at top
        scoreMatrix = self.sortScore(scoreMatrix,n)

        print("After Sorting")
        print(scoreMatrix)
        print("Engine trained in %s seconds." % (time.time() - start))

    def _train(self, ds, attrName, attrValue, scoreMatrix, scoreFactor):
        """
        Train the engine.
        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product. The 'stop_words' param
        tells the TF-IDF module to ignore common english words like 'the', etc.
        First fitting the attribute name taken.
        Transform for the corresponding attribute name then for the attribute value.
        Then we compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).
        Similarities and their scores are stored in score matrix.
        :param ds: A pandas dataset which is taken as input
        :param attrName: The attribute to consider for the score
        :param attrValue: The value of the attribute
        :param scoreMatrix: The matrix with the score of products. Dimension [2, no. of products in ds].
                            Column 1 = product_id, column2 = score of the product
        :param scoreFactor: Factor to be multiplied for the chosen attribute
        :return: 2D score matrix with first column as id and second as score!
        """
        user = [attrValue]
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tf.fit(ds[attrName])
        tfidf_matrix_user = tf.transform(user)
        tfidf_matrix = tf.transform(ds[attrName])

        cosine_similarities = linear_kernel(tfidf_matrix_user, tfidf_matrix)
        #Adding to previous score for the corresponding product(s)
        scoreMatrix[1] = scoreMatrix[1] + scoreFactor*cosine_similarities[0]
        return scoreMatrix


    def sortScore(self, scoreMatrix, n):

        """ Sorting according to score
        Using bubble sort
        :param scoreMatrix: Unsorted score matrix dimension (2, no. of products)
        :param n: Length of a column of matrix i.e, no. of products or no. of rows
        :return scoreMatrix: Sorted score matrix
        """
        sorted = False  # We haven't started sorting yet

        while not sorted:
            sorted = True  # Assume the list is now sorted
            for element in range(0, n - 1):
                if scoreMatrix[1][element] < scoreMatrix[1][element + 1]:
                    sorted = False  # We found two elements in the wrong order
                    hold = scoreMatrix[1][element + 1]
                    scoreMatrix[1][element + 1] = scoreMatrix[1][element]
                    scoreMatrix[1][element] = hold
                    hold2 = scoreMatrix[0][element + 1]
                    scoreMatrix[0][element + 1] = scoreMatrix[0][element]
                    scoreMatrix[0][element] = hold2
        return scoreMatrix


content_engine = ContentEngine()