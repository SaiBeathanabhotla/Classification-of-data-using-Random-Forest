#University of Massachusetts Lowell
#Course: Data Mining(COMP. 5440)
Name: Sai Krishna Kiran Beathanabhotla
Studnet ID#: 01690333


Home Path : /usr/cs/grad/master/sbeathan
Directory: DataMining


In order to test the project, we need to go to
PATH: /usr/cs/grad/master/sbeathan/DataMining/random-forest/random-forest/src

This path has main.py, DecisionTree.py and RandomForest.py files.

To test Decision Tree:  

python main.py -m 0


To test Random Forest:  

python main.py -m 1



### DESCRIPTION OF THE CODE
###Main 

Main.py
    This is the main program, has no changes and is untouched from the professor's code, which has the functions :

    load_data: to  extract the attributes from the dataset
    main: to specify the default conditions and
    test_model: to test the accuracy for the decision trees and random forest

#### Decision Tree Class

#### Creating a Decision Tree
DecisionTree.py

1. The train(self, records, attributes) function is the entry point to the creation of a decision tree.
2. The train function calls the tree_growth function where we call the find_best_split function in order to find the best split among the dataset.
3. After the values are returned from the find_best_split function, we then check the stopping condition. If the stopping condition is met, we assign a label to the node.
4. If the condition is not met, we then call the deepbootstrap function which returns the sampled records from either left_branch or right_branch.
5. After the sampling is done, we call the tree_growth function for the left_branch or right_branch. This is done until stopping condition is met.

Also, find_best_split function, calls the splitRecords function which splits the records into trueRecords and falseRecords.
Then we calculate the Gini Index for the records which would be used to calculate the Information gain.
Deep bootstrapping is done during the tree growth where we randomly sample all the records and take only 75% of them.
Function stopping_cond is used to terminate the tree-growth process by testing whether all the records have either the
 same class label or the same attribute values
Function predict predicts the label of the samples.


###RandomForest

RandomForest.py
####Creating a Random Forest
. 
1. The Random Forest Class first calls the bootstrap method to produce the bootstraped samples by taking the same number of samples as 
the size of the provided data set.

Function: bootstrap(self, records)  
This function bootstrap will return a set of records, with the same size of the original records but the sampling is done with replacement.
Statement: return random.sample(records, len(records))

2. Using this bootstrap sample set, the Random Forest class then creates a DecisionTree() with it and adds the tree to the forest list.

Function: train(self, records, attributes)
	a. We first create a tree as below.
            tree = DecisionTree()

        b. The below statement will randomly select 50% attributes for the tree
            tree_attributes = random.sample(attributes, int(len(attributes) * 0.5))

        c. Calling the bootstrap method to select samples for the tree
            bootstrap_samples = self.bootstrap(records)

        d. Training the tree with the below statement
            tree.train(bootstrap_samples, tree_attributes)

        e. Now we add the tree to the forest list
            self.forest.append(tree) 
This procedure is repeated for the number of requested trees (self.tree_num) in the forest and the result is appended to the forest list.


3. Prediction with the Random Forest

We take the sample data and send it as input to the function which is tested through all the forest list trees and the output is calculated 
by incrementing the value of the paticular label.
	a. The looping is done as follows though all the trees in the list.
	   for i in range(0, self.tree_num):
            	predicted_label = self.forest[i].predict(sample)
	b. We increment the count of each label by checking if they are equal or not as below.
	   if predicted_label not in predictions.keys():
                predictions[predicted_label] = 1
           else:
                predictions[predicted_label] += 1
	c. After the comparision, we return the maximum value as the output as follows.
	   return max(predictions, key=predictions.get)




