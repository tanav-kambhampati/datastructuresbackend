## Python Titanic Model, prepared for a titanic.py file

# Import the required libraries for the VehiclesModel class
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns

class VehiclesModel:
    """A class used to represent the Titanic Model for employee survival prediction.
    """
    # a singleton instance of VehiclesModel, created to train the model only once, while using it for prediction multiple times
    _instance = None
    
    # constructor, used to initialize the VehiclesModel
    def __init__(self):
        # the titanic ML model
        self.model = None
        self.dt = None
        # define ML features and target
        self.features = ['Car', 'Salary']
        self.target = 'Affordability'
        # load the titanic dataset
        self.vehicles_data = pd.read_csv('carsalarydata.csv')
        # one-hot encoder used to encode 'embarked' column
        self.encoder = OneHotEncoder(handle_unknown='ignore')

    # clean the titanic dataset, prepare it for training
    def _clean(self):
        self.vehicles_data['Affordability'] = self.vehicles_data['Affordability'].apply(lambda x: 1 if x == "True" else 0)

        # Encode the 'Car' column into numerical values
        le = LabelEncoder()
        self.vehicles_data['Car'] = le.fit_transform(self.vehicles_data['Car'])

        # One-hot encode the 'Car' column
        onehot = pd.get_dummies(self.vehicles_data['Car'], prefix='Car')
        self.vehicles_data = pd.concat([self.vehicles_data.drop(columns=['Car']), onehot], axis=1)

        # Drop rows with missing values
        self.vehicles_data.dropna(inplace=True)
        

    # train the titanic model, using logistic regression as key model, and decision tree to show feature importance
    def _train(self):
        # split the data into features and target
        X = self.vehicles_data[self.features]
        y = self.vehicles_data[self.target]
        
        # perform train-test split
        self.model = LogisticRegression(max_iter=1000)
        
        # train the model
        self.model.fit(X, y)
        
        # train a decision tree classifier
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)
        
    @classmethod
    def get_instance(cls):
             
        # check for instance, if it doesn't exist, create it
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        # return the instance, to be used for prediction
        return cls._instance

    def predict(self, employee):
    # clean the employee data
        employee_df = pd.DataFrame(employee, index=[0])
    
    # One-hot encode the 'Car' column in the employee data
        onehot = pd.get_dummies(employee_df['Car'], prefix='Car')
        employee_df = pd.concat([employee_df.drop(columns=['Car']), onehot], axis=1)
    
    # Drop the 'Affordability' column from employee data
        employee_df.drop(['Affordability'], axis=1, inplace=True)
    
    # predict the survival probability and extract the probabilities from numpy array
        dontgetcar, getcar = np.squeeze(self.model.predict_proba(employee_df))
    
    # return the survival probabilities as a dictionary
        return {'Dont Get Car': dontgetcar, 'Get Car': getcar}

    
    def feature_weights(self):
        
        # extract the feature importances from the decision tree model
        importances = self.dt.feature_importances_
        # return the feature importances as a dictionary, using dictionary comprehension
        return {feature: importance for feature, importance in zip(self.features, importances)} 
    
def initTitanic():

    VehiclesModel.get_instance()
    
def testTitanic():

     
    # setup employee data for prediction
    print(" Step 1:  Define theoritical employee data for prediction: ")
    employee = {
        'name': ['John Mortensen'],
        'pclass': [2],
        'sex': ['male'],
        'age': [64],
        'sibsp': [1],
        'parch': [1],
        'fare': [16.00],
        'embarked': ['S'],
        'alone': [False]
    }
    print("\t", employee)
    print()

    # get an instance of the cleaned and trained Titanic Model
    VehiclesModel = VehiclesModel.get_instance()
    print(" Step 2:", VehiclesModel.get_instance.__doc__)
   
    # print the survival probability
    print(" Step 3:", VehiclesModel.predict.__doc__)
    probability = VehiclesModel.predict(employee)
    print('\t Chance you dont get a car: {:.2%}'.format(probability.get('dontgetcar'))) 
    print('\t Chance you do get a car: {:.2%}'.format(probability.get('getcar')))
    print()
    
    # print the feature weights in the prediction model
    print(" Step 4:", VehiclesModel.feature_weights.__doc__)
    importances = VehiclesModel.feature_weights()
    for feature, importance in importances.items():
        print("\t\t", feature, f"{importance:.2%}") # importance of each feature, each key/value pair
        
if __name__ == "__main__":
    print(" Begin:", testTitanic.__doc__)
    testTitanic()



# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import OneHotEncoder

# # Load the titanic dataset
# carsalarydata = pd.read_csv('carsalarydata.csv')

# # Preprocess the data
# carsalarydata.drop(['Car'], axis=1, inplace=True)
# carsalarydata.dropna(inplace=True)
# carsalarydata['Affordability'] = carsalarydata['Affordability'].apply(lambda x: 1 if x == 'True' else 0)

# # Encode categorical variables
# categorical_variables = ['Salary']
# categorical_data = carsalarydata[categorical_variables]
# enc = OneHotEncoder(handle_unknown='ignore')
# onehot = enc.fit_transform(categorical_data)
# onehot_array = onehot.toarray()
# cols = enc.get_feature_names_out(categorical_variables)
# encoded_df = pd.DataFrame(onehot_array, columns=cols)
# carsalarydata_encoded = pd.concat([carsalarydata.drop(columns=categorical_variables), encoded_df], axis=1)
# carsalarydata_encoded.dropna(inplace=True) 


# # Split the data into training and testing sets
# X = carsalarydata_encoded.drop(columns=['Affordability'])
# y = carsalarydata_encoded['Affordability']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# # Train a decision tree classifier
# dt = DecisionTreeClassifier()
# dt.fit(X_train, y_train)

# # Test the model
# y_pred = dt.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print('Accuracy:', accuracy)

