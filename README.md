# Memgraph

- [Memgraph](#memgraph)
- [Environment Setup](#environment-setup)
- [Running the Examples](#running-the-examples)
  - [Title - Example 1](#title---example-1)
  - [Title - Example 2](#title---example-2)
  - [Title - Example 3](#title---example-3)
  - [Fraud Detection with Memgraph](#fraud-detection-with-memgraph)
    - [Code Overview](#code-overview)
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

## Title - Example 3

TODO

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