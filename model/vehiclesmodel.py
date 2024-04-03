import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

# Load the titanic dataset
rocket_data = pd.read_csv('rocket_launch_data.csv')

# Preprocess the data
rocket_data.drop(['origin_country'], axis=1, inplace=True)
rocket_data.dropna(inplace=True)
rocket_data['success_rate'] = rocket_data['success_rate'].apply(lambda x: 1 if x == 'Success' else 0)

# Encode categorical variables
categorical_variables = ['payload_mass', 'company', 'engine_strength']
categorical_data = rocket_data[categorical_variables]
enc = OneHotEncoder(handle_unknown='ignore')
onehot = enc.fit_transform(categorical_data)
onehot_array = onehot.toarray()
cols = enc.get_feature_names_out(categorical_variables)
encoded_df = pd.DataFrame(onehot_array, columns=cols)
rocket_data_encoded = pd.concat([rocket_data.drop(columns=categorical_variables), encoded_df], axis=1)
rocket_data_encoded.dropna(inplace=True) 


# Split the data into training and testing sets
X = rocket_data_encoded.drop('success_rate', axis=1)
y = rocket_data_encoded['success_rate']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a decision tree classifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

# Test the model
y_pred = dt.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

