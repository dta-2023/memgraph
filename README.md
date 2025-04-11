# Invoice Fraud Detection
## 📚 Table of Contents
Description

Technologies Used

Project Workflow

Prerequisites

Installation

Usage

Data Generation

License

## 📝 Description
Invoice Fraud Detection is a machine learning-based system designed to automatically detect fraudulent invoices. It leverages XGBoost, a powerful gradient boosting algorithm, to classify invoices as either fraudulent or legitimate based on features such as total amount, status, and due date.

The project integrates with Memgraph, a graph database that stores relationships between users and invoices. This allows for efficient querying, advanced data analysis, and real-time fraud detection.

## 🔑 Key Features:
Machine Learning Model: Detects fraudulent invoices using features like invoice amount, status, and due date.

Graph Database Integration: Uses Memgraph to represent relationships between users and invoices for real-time querying and detection.

Synthetic Data Generation: Generates realistic data using Faker, including fraudulent and legitimate invoices.

Real-time Fraud Detection: New invoices can be processed on the fly, and predictions are stored in both CSV and Memgraph.

## 🛠️ Technologies Used
Python: Main programming language.

XGBoost: Gradient boosting algorithm for classification.

Pandas: Data manipulation and preprocessing.

Faker: Generates synthetic data (users and invoices).

Joblib: Saves and loads trained machine learning models.

Memgraph: Graph database for managing relationships.

Scikit-learn: Data preprocessing, encoding, and dataset splitting.

## 🔄 Project Workflow
Data Generation
Using Faker to create:

Users (with attributes like VAT number, name, email)

Invoices (amount, status, due date)

Fraud labels (fraudulent or legitimate)

Data Preprocessing

Categorical data encoding

Handling missing values

Model Training

Training XGBoost using preprocessed data

Tuning hyperparameters like learning_rate, n_estimators, max_depth

Memgraph Integration

Storing users, invoices, and relationships in Memgraph

Relationships include: UPLOADED_BY, NEEDS_PAYMENT_FROM

Real-time Detection

New invoices are classified

Results saved in both CSV and Memgraph for analysis

## ✅ Prerequisites
Before starting, make sure the following libraries are installed:

xgboost
pandas
scikit-learn
joblib
faker
gqlalchemy
memgraph
To install them:

pip install -r requirements.txt
📦 Installation
Clone the repository:

git clone <repository_url>
cd <project_folder>
Install dependencies:

pip install -r requirements.txt
Set up Memgraph:
Make sure Memgraph is installed and running. You can follow the official Memgraph documentation for installation and setup instructions.

🚀 Usage
## 🧠 Real-time Fraud Detection
Once your environment is ready:

The system generates synthetic data

Trains the XGBoost model

Saves prediction results into both CSV and Memgraph

Steps:
Generate data, train the model, and store results in Memgraph.

Add new invoices — the model will classify them as fraudulent or legitimate.

View results by querying Memgraph or inspecting the output CSV.

## 📊 Data Generation
Synthetic data is generated using the Faker library:

Users: VAT number, name, email, etc.

Invoices: Invoice ID, amount, status, due date, tax ID.

Fraud Labels: Certain invoices are flagged as fraudulent based on patterns like high amounts or unusual statuses.

All data is saved to a CSV file and also loaded into Memgraph for graph analysis.
