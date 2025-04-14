# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report

import joblib

# Load data from a CSV file
file_path = r'C:\Users\filip\Desktop\S4_DTA\Memgraph_ML\invoice_with_fraud2.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to verify its content
print(data.head())

# Convert the 'due_date' column to datetime type
data['due_date'] = pd.to_datetime(data['due_date'])
# Convert the date to a timestamp (numeric representation of the date)
data['due_date'] = data['due_date'].apply(lambda x: x.timestamp())

# Encode the categorical 'status' variable into numeric values (0 or 1)
label_encoder = LabelEncoder()
data['status'] = label_encoder.fit_transform(data['status'])

# Display the first few rows with the modified 'status' and 'due_date' columns
print(data[['status', 'due_date']].head())

# Select the explanatory variables (X) and the target variable (y)
X = data[['total_amount', 'status', 'due_date']]  
y = data['fraud']   # 'fraud' is the target (0 for non-fraudulent, 1 for fraudulent)

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display the shapes of the training and testing sets
print("Training set:", X_train.shape)
print("Test set:", X_test.shape)

# Save the model after training

# Convert the data into DMatrix format, which is optimized for XGBoost
train_data = xgb.DMatrix(X_train, label=y_train)
test_data = xgb.DMatrix(X_test, label=y_test)

# Define the parameters for the XGBoost model
params = {
    'objective': 'binary:logistic',  # Binary classification (fraud or not)
    'eval_metric': 'logloss',  # Logarithmic loss for evaluation
    'max_depth': 5,  # Maximum depth of the tree
    'learning_rate': 0.1,  # Learning rate (for updating weights)
    'n_estimators': 100  # Number of trees to train
}

# Train the XGBoost model
model = xgb.train(params, train_data, num_boost_round=100)

# Make predictions on the test set
y_pred = model.predict(test_data)
# Convert the predicted probabilities to classes (0 or 1)
y_pred = [1 if x > 0.5 else 0 for x in y_pred]

# Evaluate the model with accuracy and classification report
print("Accuracy:", accuracy_score(y_test, y_pred))  # Model accuracy on the test set
print("Classification Report:\n", classification_report(y_test, y_pred))  # Detailed model performance

# Save the trained model to a file
joblib.dump(model, 'fraud_detection_model.pkl')

# Load the saved model for future predictions
model = joblib.load('fraud_detection_model.pkl')

# Example of a new invoice to predict
new_invoice = pd.DataFrame({
    'total_amount': [30000000],  # Invoice amount (in monetary units)
    'status': [label_encoder.transform(['paid'])[0]],  # Encode the invoice status (e.g., 'paid')
    'due_date': [pd.to_datetime('2025-12-31').timestamp()]  # Convert the due date to timestamp
})

# Convert the new invoice data into DMatrix format for XGBoost
new_data = xgb.DMatrix(new_invoice)
# Make a prediction on whether the invoice is fraudulent
prediction = model.predict(new_data)

# Display the prediction result
if prediction[0] > 0.5:
    print("The invoice is fraudulent.")
else:
    print("The invoice is legitimate.")
