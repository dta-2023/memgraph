# Invoice Fraud Detection Project

## Table of Contents

- [Invoice Fraud Detection Project](#invoice-fraud-detection-project)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
    - [Key Features:](#key-features)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
    - [How the Files Work Together:](#how-the-files-work-together)
  - [Project Workflow](#project-workflow)
    - [1. **Data Generation**](#1-data-generation)
    - [2. **Data Preprocessing**](#2-data-preprocessing)
    - [3. **Model Training**](#3-model-training)
    - [4. **Integration with Memgraph**](#4-integration-with-memgraph)
    - [5. **Real-time Fraud Detection**](#5-real-time-fraud-detection)
  - [Usage](#usage)
    - [Real-time Fraud Detection](#real-time-fraud-detection)
    - [Steps to Use:](#steps-to-use)
  - [Data Generation](#data-generation)
 

## Description

Invoice Fraud Detection is a machine learning-based system designed to identify fraudulent invoices. By using **XGBoost**, a robust gradient boosting algorithm, the system classifies invoices as fraudulent or legitimate based on several features like invoice amount, status, and due date.

The project leverages **Memgraph**, a graph database, to store the relationships between users and invoices. This enables efficient querying, real-time analysis, and fraud detection by analyzing connections between users and invoices. By integrating machine learning and graph databases, the system can detect fraud in a manner that is scalable and efficient.

### Key Features:

- **Machine Learning Model**: The system uses **XGBoost** to classify invoices as fraudulent or legitimate.
  
- **Graph Database Integration**: **Memgraph** stores and analyzes the relationships between invoices and users, allowing for fast querying and fraud detection.
  
- **Synthetic Data Generation**: The project generates synthetic user and invoice data, including fraud labels, for training and simulating real-world fraud detection.
  
- **Real-time Fraud Detection**: New invoices can be processed and classified in real-time, with results stored both in CSV files and Memgraph.
  

## Technologies Used

- **Python**: The primary language used for developing the project.
  
- **XGBoost**: A gradient boosting algorithm used to detect fraud by classifying invoices.
  
- **Pandas**: For data manipulation and preprocessing of the generated synthetic data.
  
- **Faker**: A Python library used to generate synthetic user and invoice data.
  
- **Joblib**: Used to save and load the trained machine learning model.
  
- **Memgraph**: A graph database used to store the relationships between users and invoices, providing an efficient way to analyze the connections.
  
- **Scikit-learn**: Used for preprocessing tasks like encoding categorical variables and splitting data into training and test sets.
  

## Project Structure

The project is divided into several Python files, each serving a specific purpose:

| **File** | **Description** |
| --- | --- |
| `fakedata.py` | Generates synthetic data, including users, invoices, and fraud labels. |
| `memgraph.py` | Loads the generated data into **Memgraph** and establishes relationships between users and invoices. |
| `Traitment.py` | Preprocesses the data and trains the XGBoost model to detect fraudulent invoices. |
| `main.py` | Generates new fraudulent invoices using the trained model and adds them to both **Memgraph** and a CSV file. |

### How the Files Work Together:

1. **`fakedata.py`** generates synthetic data (users, invoices, and fraud labels) and saves it in a CSV file.
  
2. **`memgraph.py`** loads the data from the CSV file and inserts it into **Memgraph**, creating relationships between users and invoices for efficient querying.
  
3. **`Traitment.py`** preprocesses the data, trains the **XGBoost** fraud detection model, and saves the trained model for future use.
  
4. **`main.py`** uses the trained model to classify new invoices as fraudulent or legitimate, stores the results in **Memgraph**, and adds them to the CSV file.
  

## Project Workflow

### 1. **Data Generation**

- **Synthetic Data Creation**: Using the **Faker** library, synthetic data is generated for both users and invoices. Each user has attributes like VAT number, name, email, etc. Invoices have attributes like amount, status, due date, etc.
  
- **Fraud Labels**: Some invoices are flagged as fraudulent based on certain characteristics, such as unusually high amounts or uncommon invoice statuses.
  
- **CSV Output**: The generated data is stored in a CSV file for both training and testing the fraud detection model.
  

### 2. **Data Preprocessing**

- **Data Encoding**: Categorical features such as invoice status are encoded into numerical values.
  
- **Handling Missing Data**: Any missing or null values are addressed to ensure the dataset is ready for machine learning.
  
- **Feature Engineering**: Features that might help the model classify invoices as fraudulent are selected or created.
  

### 3. **Model Training**

- **XGBoost Model**: Using the preprocessed data, an **XGBoost** model is trained. Hyperparameters like **learning_rate**, **n_estimators**, and **max_depth** are tuned to improve the model's performance.
  
- **Model Evaluation**: The trained model is evaluated on test data to ensure it performs well at predicting fraudulent invoices.
  

### 4. **Integration with Memgraph**

- The processed data, including users, invoices, and fraud labels, are stored in **Memgraph**. Relationships between users and invoices are represented as graph edges (e.g., **UPLOADED_BY**, **NEEDS_PAYMENT_FROM**).
  
- This graph representation allows for efficient querying, making it easy to identify and analyze patterns of fraudulent behavior based on user-invoice relationships.
  

### 5. **Real-time Fraud Detection**

- **Model Deployment**: After training, the fraud detection model can classify new invoices as fraudulent or legitimate in real-time.
  
- **Real-time Analysis**: New invoices are processed by the model, and the results (fraud predictions) are stored in both the CSV file and **Memgraph** for further analysis.
  

## Usage

### Real-time Fraud Detection

Once the environment is set up and the system is running, it will automatically:

1. **Generate Synthetic Data**: Synthetic invoice and user data is created and stored.
  
2. **Train the Model**: The system trains the **XGBoost** model based on the synthetic data.
  
3. **Store Results**: The results, including predictions of fraud status, are saved in both **Memgraph** and a CSV file.
  
4. **Classify New Invoices**: The system can classify new invoices as fraudulent or legitimate.
  

### Steps to Use:

1. **Step 1**: Generate synthetic data and train the fraud detection model.
  
2. **Step 2**: Add new invoices for fraud detection. The model will classify them as fraudulent or legitimate.
  
3. **Step 3**: View fraud detection results by querying the data in **Memgraph** or inspecting the CSV file.
  

## Data Generation

The **Faker** library is used to generate synthetic data, including:

- **Users**: Attributes include VAT number, name, email, etc.
  
- **Invoices**: Attributes include invoice ID, amount, status, due date, and tax ID.
  
- **Fraud Labels**: Some invoices are flagged as fraudulent based on certain patterns (e.g., high invoice amounts or rare invoice statuses).
  

The generated data is stored in a **CSV file** and loaded into **Memgraph** for further analysis. This synthetic data allows for realistic simulation of fraud detection in real-world scenarios.