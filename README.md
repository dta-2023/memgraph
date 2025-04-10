Invoice Fraud Detection
Table of Contents
Description

Technologies Used

Project Workflow

Prerequisites

Installation

Usage

Data Generation

License

Description
Invoice Fraud Detection is a machine learning-based system that aims to automatically detect fraudulent invoices. The system uses XGBoost, a powerful gradient boosting algorithm, to classify invoices as either fraudulent or legitimate based on various features such as the total amount, invoice status, and due date.

The project is integrated with Memgraph, a graph database that stores relationships between users and invoices. By using Memgraph, the system benefits from efficient querying and the ability to easily analyze and visualize the connections between invoices and the users involved. This integration also allows for real-time fraud detection.

Key Features:
Machine Learning Model: Uses XGBoost to detect fraudulent invoices based on various features like invoice amount, status, and due date.

Graph Database Integration: Memgraph is used to store and analyze relationships between users and invoices, allowing efficient querying and real-time fraud detection.

Synthetic Data Generation: The project generates synthetic user and invoice data, including fraudulent invoices, to train the machine learning model and simulate real-world fraud detection scenarios.

Real-time Fraud Detection: New invoices can be processed and classified in real-time, with predictions about fraud status stored in both CSV files and Memgraph.

Technologies Used
Python: Main programming language for the project.

XGBoost: Gradient boosting algorithm used for fraud detection classification.

Pandas: Used for data manipulation and preprocessing.

Faker: Python library used to generate synthetic data for users and invoices.

Joblib: Used for saving and loading the trained machine learning model.

Memgraph: Graph database used to store relationships between invoices and users for efficient querying.

Scikit-learn: Used for preprocessing, encoding categorical data, and splitting data into training and test sets.

Project Workflow
The workflow for the project is as follows:

Data Generation: Synthetic data is generated using the Faker library. This data includes:

Users (with attributes such as VAT number, name, email, etc.)

Invoices (with attributes such as amount, status, due date, etc.)

Fraud labels (indicating whether the invoice is fraudulent or legitimate)

Data Preprocessing: The generated data is preprocessed and encoded for machine learning. Categorical features are converted into numerical values, and missing values are handled.

Model Training: Using the preprocessed data, an XGBoost model is trained to classify invoices as fraudulent or legitimate. The model is optimized using hyperparameters such as learning_rate, n_estimators, and max_depth.

Integration with Memgraph: The processed data, including users, invoices, and fraud labels, is stored in Memgraph. The relationships between users and invoices are represented as graph edges (e.g., UPLOADED_BY and NEEDS_PAYMENT_FROM), allowing for efficient querying and fraud detection.

Real-time Fraud Detection: New invoices can be added to the system. The model predicts whether they are fraudulent or legitimate, and the results are stored in both a CSV file and Memgraph for further analysis.

Prerequisites
Before starting, make sure you have the following libraries installed:

xgboost

pandas

scikit-learn

joblib

faker

gqlalchemy

memgraph

To install these dependencies, you can use the following command:

bash
Copier
Modifier
pip install -r requirements.txt
Installation
Clone the repository:

bash
Copier
Modifier
git clone <repository_url>
cd <project_folder>
Install dependencies:

Install the required dependencies by running:

bash
Copier
Modifier
pip install -r requirements.txt
Set up Memgraph:

Make sure that Memgraph is installed and running on your system. You can follow the official Memgraph documentation to set it up.

Usage
Real-time Fraud Detection
Once the environment is set up, the system will automatically generate synthetic invoice data, train the fraud detection model using XGBoost, and store the results in both a CSV file and Memgraph. The data will include information about users, invoices, and fraud labels.

How to Use:
Step 1: Generate synthetic data, train the model, and store the results in Memgraph.

Step 2: Add new invoices to the system for fraud detection. The model will classify them as fraudulent or legitimate.

Step 3: View fraud detection results in real-time by querying the data in Memgraph or inspecting the CSV file.

Data Generation
Synthetic data is generated using the Faker library. The data includes:

Users: Each user has attributes like VAT number, name, email, etc.

Invoices: Attributes include invoice ID, amount, status, due date, and tax ID.

Fraud labels: Some invoices are flagged as fraudulent based on certain characteristics (e.g., unusually high amounts or rare invoice statuses).

The synthetic data is stored in a CSV file and also loaded into Memgraph for analysis.