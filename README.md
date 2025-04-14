# Memgraph

- [Memgraph](#memgraph)
- [Environment Setup](#environment-setup)
- [Running the Examples](#running-the-examples)
  - [Title - Example 1](#title---example-1)
  - [Title - Example 2](#title---example-2)
  - [Fraud Detection with XGBOOST](#fraud-detection-with-xgboost)
    - [Code Overview](#code-overview)
    - [Steps to Run the Project](#steps-to-run-the-project)
      - [Generate Synthetic Data](#generate-synthetic-data)
    - [Conclusion ](#conclusion)
  - [Fraud Detection with Memgraph](#fraud-detection-with-memgraph)
    - [Code Overview](#code-overview-1)
    - [Steps to run Project](#steps-to-run-project)
      - [Generate Sample Data](#generate-sample-data)
      - [Load Data into Memgraph and Train Model](#load-data-into-memgraph-and-train-model)
      - [Run Web Dashboard](#run-web-dashboard)
  

# Environment Setup

To run the examples and use Memgraph with the various integrations.

Follow these steps:

1. Clone the Repository
  
  First, clone this repository to your local machine
  
  ```bash
  git clone https://github.com/dta-2023/memgraph.git
  ```

2. Create a Virtual Environment with python 3.8 too 3.10 and activate it
  
  ```bash
  python -m venv .venv
  .venv\Scripts\activate # On Windows
  # source .venv/bin/activate  # On macOS/Linux
  ```
  
3. Install Dependencies
  
  ```bash
  pip install -r requirements.txt
  ```
  
4. Create & run Docker Memgraph Mage
  
  ```bash
  docker run -p 7687:7687 -p 7444:7444 --name memgraph -v "YOUR\\PATH\\TO\\FOLDER:/memgraph" memgraph/memgraph-mage
  ```
  
5. Create Docker Memgraph Lab
  
  ```bash
  docker run -d -p 3000:3000  --name lab memgraph/lab
  ```
  
  1. **Issues when connecting to Memgraph Lab to Memgraph**
    
    1. Remove the Docker Memgraph Lab and run this command
      
  
  ```bash
  docker run -d -p 3000:3000 -e QUICK_CONNECT_MG_HOST=host.docker.internal --name lab memgraph/lab
  ```
  

# Running the Examples

## Title - Example 1

TODO

## Title - Example 2

TODO

## Fraud Detection with XGBOOST

This project aims to detect fraudulent invoices using the Memgraph database and a machine learning model. It generates synthetic data, loads it into Memgraph, and trains a model to predict whether an invoice is fraudulent.

### Code Overview

Here’s an overview of the main files in the project and their purposes:

| **File** | **Purpose** |
| --- | --- |
| `fakedata.py` | Generates fake user and invoice data with fraud labels. |
| `memgraph.py` | Loads the generated data into Memgraph and creates relationships between users and invoices. |
| `Traitment.py` | Processes the data and trains a fraud detection model using XGBoost. |
| `main.py` | Generates new fraudulent invoices using the trained model and adds them to Memgraph and the CSV file. |

### Steps to Run the Project

Dependencies
Here are the main libraries required to run this project:

gqlalchemy : For interacting with the Memgraph database.

xgboost : For training the fraud detection model.

scikit-learn : For data preprocessing and splitting the data into training and testing sets.

pandas : For data manipulation.

Faker : For generating synthetic data.

joblib : For saving and loading the trained model.

You can install them using pip if necessary:

```bash
pip install gqlalchemy xgboost scikit-learn pandas faker joblib
```

#### Generate Synthetic Data

Run the following script to generate fake data for users and invoices with fraud labels:

```bash
python fakedata.py
```

This will create the file invoice_with_fraud2.csv containing synthetic data with embedded fraud patterns.

2. Load Data into Memgraph
  Run the following script to load the generated data into Memgraph and create relationships between users and invoices:

```bash
python memgraph.py
```

3. Process Data and Train the Fraud Detection Model
  Run the following script to preprocess the data, train a machine learning model (XGBoost), and save it:
  

```bash
python Traitment.py
```

This script trains a fraud detection model based on the invoice data.

4. Generate New Fraudulent Invoices
  Run the following script to generate new fraudulent invoices using the trained model and add them to Memgraph and the CSV file:

```bash
python main.py
```

This script creates new fraudulent invoices, saves them in the CSV file, and adds them to Memgraph.

Access Memgraph
The project uses Memgraph to store users and invoices. Make sure Memgraph is installed and running on your machine. You can verify connections to Memgraph via Memgraph's management interface or a tool like Cypher.

### Conclusion 

This project allows you to simulate invoice data with fraudulent behaviors, load it into Memgraph, and use a machine learning model to detect fraud. You can extend this project by adding more features like data visualization or integration with other databases.

## Fraud Detection with Memgraph

To see and run the full project, go to the folder: **`FraudDetectionMemgraph`**

### Code Overview

Here’s a quick overview of the main example scripts provided in this project:

| **File** | **Purpose** |
| --- | --- |
| `DatasetGenerator.py` | Generates synthetic invoice data with embedded fraud patterns. |
| `MemgraphLoad.py` | Loads the generated dataset into Memgraph and runs graph algorithms. |
| `dashboard.py` | Flask-based web dashboard to interact with data and predictions. |

### Steps to run Project

#### Generate Sample Data

```bash
python DatasetGenerator.py
```

This will create `InvoicesFraud.csv` with synthetic data containing fraud patterns.

#### Load Data into Memgraph and Train Model

```bash
python MemgraphLoad.py
```

#### Run Web Dashboard

```bash
python dashboard.py
```

Access the dashboard at `http://127.0.0.1:5000` to:

- Generate new sample data
  
- Upload CSV files
  
- Get fraud predictions on new invoices