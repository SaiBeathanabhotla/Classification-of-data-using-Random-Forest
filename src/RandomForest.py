import random
from DecisionTree import DecisionTree


class RandomForest(object):
    """
    Class of the Random Forest
    """

    def __init__(self, tree_num):
        self.tree_num = tree_num
        self.forest = []

    def train(self, records, attributes):
        """
        This function will train the random forest, the basic idea of training a
        Random Forest is as follows:
        1. Draw n bootstrap samples using bootstrap() function
        2. For each of the bootstrap samples, grow a tree with a subset of
            original attributes, which is of size m (m << # of total attributes)
        """
        # Your code here

        for tree in range(self.tree_num):

            # creating a tree
            tree = DecisionTree()

            # randomly selecting 50% attributes for the tree
            tree_attributes = random.sample(attributes, int(len(attributes) * 0.5))

            # selecting bootstrap samples for the tree by calling the bootstrap method
            bootstrap_samples = self.bootstrap(records)

            # training the tree
            tree.train(bootstrap_samples, tree_attributes)

            # adding the tree to the forest list
            self.forest.append(tree)

    def predict(self, sample):
        """
        The predict function predicts the label for new data by aggregating the
        predictions of each tree.

        This function should return the predicted label
        """
        # Your code here
	#Here we take a dictionary and will keep incrementing the values of the labels.
        predictions = {}

        for i in range(0, self.tree_num):
            predicted_label = self.forest[i].predict(sample)

            if predicted_label not in predictions.keys():
                predictions[predicted_label] = 1
            else:
                predictions[predicted_label] += 1

	#We will return the maximum value of the predictions.
        return max(predictions, key=predictions.get)

    def bootstrap(self, records):
        """
        This function bootstrap will return a set of records, which has the same
        size with the original records but with replacement.
        """
        #Sampling the records and returning them to the calling function.
        return random.sample(records, len(records))