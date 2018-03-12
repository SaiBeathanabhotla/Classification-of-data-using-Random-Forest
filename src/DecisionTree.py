import math
import random

class TreeNode(object):
    def __init__(self, isLeaf=False):

       #Your code here
       """
       self.isLeaf = isLeaf
       self.attr = None
       self.val = None
       self.label = None
       self.left_subtree = None
       self.right_subtree = None
       """
       print("init")

    def predict(self, sample):
        """
        This function predicts the label of given sample
        """
        # Your code here
	'''
	curr_node = self
        while not curr_node.isLeaf:
            if curr_node.label is None:
                if sample["attributes"][curr_node.attr] == curr_node.val:
                    curr_node = curr_node.left_subtree
                else:
                    curr_node = curr_node.right_subtree
            else:
                curr_node.isLeaf = False

        return curr_node.label
	'''

class DecisionTree(object):
    """
    Class of the Decision Tree
    """

    def __init__(self):
        self.root = None

    def gain(self, records, trueRecords, falseRecords):
	#In this function we calculate the Gini Index of the records and also calculate the gain.

        giniTrueRecords = self.giniIndex(trueRecords)
        giniFalseRecords = self.giniIndex(falseRecords)
        giniRecords = self.giniIndex(records)
        recordsLength = float(len(records))
        trueRecordsLength = float(len(trueRecords))
        falseRecordsLength = float(len(falseRecords))
        pr1 = trueRecordsLength / recordsLength
        pr2 = falseRecordsLength / recordsLength
	#Calculating Gain with the Gini Indexes of both the sets.
        gain = giniRecords - (pr1 * giniTrueRecords + pr2 * giniFalseRecords)
	#We return the value of gain to the calling function.
        return gain

    def giniIndex(self, records):
	#In this function we calculate the Gini value and return the same
        labelP = 0.0
        labelE = 0.0
        for row in records:
            if row["label"] == "p":
                labelP += 1
            else:
                labelE += 1
        recordLength = labelP + labelE
        if labelP == 0.0 or labelE == 0.0:
            giniValue = 0.0
        else:
            prP = labelP / recordLength
            prE = labelE / recordLength
            giniValue = 1.0 - (math.pow(prP, 2) + math.pow(prE, 2))

        return giniValue

    def deepbootstrap(self, records):
        """
        This function bootstrap will return a set of records, which has the same
        size with the original records but with replacement.
        """
	#Randomly sampling the records and returning only 75% of them during the tree growth

        bootstrap_records = random.sample(records, int((len(records) * 75) / 100))
        return bootstrap_records

    def classify(self, records):
        """
        This function determines the class label to be assigned to a leaf node.
        In most cases, the leaf node is assigned to the class that has the
        majority number of training records

        This function should return a label that is assigned to the node
        """

    def splitRecords(self, records, attr, value):
	#Here we split the records into trueRecords and falseRecords and return the values to the calling function
        trueRecords = []
        falseRecords = []
        for row in records:
	#We go through all the records and check if the values are equal and then append them to the lists.
            if row["attributes"][attr] == value:
                trueRecords.append(row)
            else:
                falseRecords.append(row)

        return (trueRecords, falseRecords)


    def stopping_cond(self, records):
        """
        The stopping_cond() function is used to terminate the tree-growing
        process by testing whether all the records have either the same class
        label or the same attribute values.

        This function should return True/False to indicate whether the stopping
        criterion is met
        """
	#Here we check if the labels are equal are not and will return true/false based on the comparision
        firstRowLabel = records[0]["label"]
        for row in records:
            if (row["label"] != firstRowLabel):
                return False
        return True

    def find_best_split(self, records, attributes):
        """
        The find_best_split() function determines which attribute should be
        selected as the test condition for splitting the trainig records.

        This function should return multiple information:
            attribute selected for splitting
            threshhold value for splitting
            left subset
            right subset
        """
        bestAttrbute_value = {}
        bestInfoGain = 0.0
        left_branch = []
        right_branch = []

        for attr in attributes:
	# creat a dictionary to hold the values of the attribute
            attrValues = {}
            for entry in records:
	    #Assigning 1 to all the values in the dictionary
                attrValues[(entry["attributes"][attr ])] = '1'
            for value in attrValues:
	    # split records on the values of the attribute
                (trueRecords, falseRecords) = self.splitRecords(records, attr, value)
		#We call the function gain which return the gain of trueRecords and falseRecords
                gain = self.gain(records, trueRecords, falseRecords)
		#Comparing the gain with bestInfoGain and would swap if the value of gain is higher
                if (gain > bestInfoGain):
                    bestInfoGain = gain
                    left_branch = trueRecords
                    right_branch = falseRecords
                    bestAttrbute_value["columnIndex"] = attr
                    bestAttrbute_value["columnValue"] = value
	#We return the attribute selected for splitting, maximum gain for splitting, left branch and righ branch of the tree

        return bestAttrbute_value, bestInfoGain, left_branch, right_branch

    def tree_growth(self, records, attributes):
        """
        This function grows the Decision Tree recursively until the stopping
        criterion is met. Please see textbook p164 for more details

        This function should return a TreeNode
        """
        # Your code here
        # Hint-1: Test whether the stopping criterion has been met by calling function stopping_cond()
        # Hint-2: If the stopping criterion is met, you may need to create a leaf node
        # Hint-3: If the stopping criterion is not met, you may need to create a
        #         TreeNode, then split the records into two parts and build a
        #         child node for each part of the subset

        (node, bestInfoGain, leftSubset, rightSubset) = self.find_best_split(records, attributes)

	#We now check for the stopping condition after getting the values from find_best_split dunction
        if bestInfoGain == 0.0:
            labelP = 0.0
            labelE = 0.0
            for row in records:
                if row["label"] == "p":
                    labelP += 1
                else:
                    labelE += 1
            if (labelP > labelE):
                node = {"label": "p"}
            else:
                node = {"label": "e"}

        else:
	    #Here we check for the stopping condition
            if self.stopping_cond(leftSubset):
                node["left"] = {"label": leftSubset[0]["label"]}
            else:
		#If the condition is not met, we randomly sample the records using deepbootstrap function
                leftSubset = self.deepbootstrap(leftSubset)
                node["left"] = self.tree_growth(leftSubset, attributes)

            if self.stopping_cond(rightSubset):
                node["right"] = {"label": rightSubset[0]["label"]}
            else:
                rightSubset = self.deepbootstrap(rightSubset)
                node["right"] = self.tree_growth(rightSubset, attributes)

        return node

    def train(self, records, attributes):
        """
        This function trains the model with training records "records" and
        attribute set "attributes", the format of the data is as follows:
            records: training records, each record contains following fields:
                label - the lable of this record
                attributes - a list of attribute values
            attributes: a list of attribute indices that you can use for
                        building the tree
        Typical data will look like:
            records: [
                        {
                            "label":"p",
                            "attributes":['p','x','y',...]
                        },
                        {
                            "label":"e",
                            "attributes":['b','y','y',...]
                        },
                        ...]
            attributes: [0, 2, 5, 7,...]
        """
	#This is the entry of the decision tree model. We call the tree_growth function here

        self.root = self.tree_growth(records, attributes)

    def predict(self, sample):
        """
        This function predict the label for new sample by calling the predict
        function of the root node
        """
	#This function predicts the label for a given sample.
        node = self.root
        notLeafNode = True
        while notLeafNode:
            if (node.get("label") == None):
                columnIndex = node.get("columnIndex")
                columnValue = node.get("columnValue")

                if sample["attributes"][columnIndex] == columnValue:
                    node = node["left"]
                else:
                    node = node["right"]
            else:
                notLeafNode = False

        return node["label"]

