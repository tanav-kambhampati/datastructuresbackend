import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

# Load the titanic dataset
carsalarydata = pd.read_csv('carsalarydata.csv')

# Preprocess the data
carsalarydata.drop(['Car'], axis=1, inplace=True)
carsalarydata.dropna(inplace=True)
carsalarydata['Affordability'] = carsalarydata['Affordability'].apply(lambda x: 1 if x == 'True' else 0)

# Encode categorical variables
categorical_variables = ['Salary']
categorical_data = carsalarydata[categorical_variables]
enc = OneHotEncoder(handle_unknown='ignore')
onehot = enc.fit_transform(categorical_data)
onehot_array = onehot.toarray()
cols = enc.get_feature_names_out(categorical_variables)
encoded_df = pd.DataFrame(onehot_array, columns=cols)
carsalarydata_encoded = pd.concat([carsalarydata.drop(columns=categorical_variables), encoded_df], axis=1)
carsalarydata_encoded.dropna(inplace=True) 


# Split the data into training and testing sets
X = carsalarydata_encoded.drop(columns=['Affordability'])
y = carsalarydata_encoded['Affordability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a decision tree classifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

# Test the model
y_pred = dt.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

