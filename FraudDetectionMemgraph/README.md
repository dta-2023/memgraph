# Fraud Detection System using Memgraph

This project demonstrates how to implement a graph-based fraud detection system using Memgraph. The system generates synthetic invoice and user data with various fraud patterns, loads this data into a graph database, and offers a web interface for analyzing and detecting fraudulent transactions.

- [Fraud Detection System using Memgraph](#fraud-detection-system-using-memgraph)
  - [Overview](#overview)
  - [Theoretical Background](#theoretical-background)
    - [Why Graph Databases for Fraud Detection?](#why-graph-databases-for-fraud-detection)
    - [Node Embeddings and Node Classification](#node-embeddings-and-node-classification)
  - [Technical Implementation](#technical-implementation)
    - [Data Generation and Fraud Patterns](#data-generation-and-fraud-patterns)
    - [Graph Data Model](#graph-data-model)
    - [Node2Vec for Feature Extraction](#node2vec-for-feature-extraction)
      - [Parameters Used:](#parameters-used)
    - [Node Classification with Memgraph](#node-classification-with-memgraph)
      - [Model Workflow:](#model-workflow)
  - [Components](#components)
  - [Fraud Patterns](#fraud-patterns)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Generate Sample Data](#generate-sample-data)
    - [Load Data into Memgraph and Train Model](#load-data-into-memgraph-and-train-model)
    - [Run Web Dashboard](#run-web-dashboard)
  - [Algorithms Used](#algorithms-used)
  - [Troubleshooting](#troubleshooting)
  - [Acknowledgements](#acknowledgements)

## Overview

The system uses graph database technology to identify complex relationships between users and invoices that may indicate fraudulent activity. By leveraging Memgraph's built-in machine learning capabilities (through MAGE), the system can learn patterns of fraud and apply them to new data.

## Theoretical Background

### Why Graph Databases for Fraud Detection?

Traditional fraud detection systems often analyze transactions in isolation, which can miss sophisticated fraud schemes involving networks of users and interactions. Graph databases are well-suited for fraud detection because:

1. **Relationship-centric modeling**: Graphs naturally represent the complex relationships between entities, such as users and invoices.
  
2. **Pattern discovery**: Fraud schemes often form recognizable patterns (e.g., duplicate invoices, circular payments) that can be spotted as subgraphs.
  
3. **Network analysis**: Graph algorithms can highlight suspicious structures or connections between entities.
  
4. **Context preservation**: Unlike flat tables, graphs maintain the surrounding context of each transaction.
  
5. **Path analysis**: You can trace indirect relationships (e.g., shared attributes or multiple hops in payment flows) to reveal hidden fraud links.
  

### Node Embeddings and Node Classification

To enable machine learning on the graph, we apply:

1. **Node2Vec**  
  A graph embedding algorithm that performs biased random walks to generate a numeric vector (embedding) for each node. These embeddings capture both structural and neighborhood features of the graph, making them usable as input to machine learning models.
  
2. **Node Classification (Memgraph MAGE)**  
  Memgraph’s built-in `node_classification` algorithm uses the node embeddings from `node2vec` to predict labels (fraudulent or legitimate) for each node. The system is trained using a portion of labeled data and then used to classify new or unlabeled nodes.
  

## Technical Implementation

### Data Generation and Fraud Patterns

The synthetic data generator (`DatasetGenerator.py`) creates realistic but simulated financial data with embedded fraud patterns:

- **Identity-based fraud indicators**:
  - Email addresses with suspicious patterns (random numbers, temporary domains)
  - Phone numbers with recognizable patterns (all zeros, sequential numbers)
  - User registrations during suspicious hours (2-4 AM)
  - VAT numbers with suspicious patterns (repeating digits, sequential numbers)
- **Transaction-based fraud indicators**:
  - Unusually small or large transaction amounts
  - Round number amounts (exactly $100.00, $1000.00)
  - Specific repeating amounts (e.g., $1111.11, $9999.99)
  - Invalid IBAN formats or suspicious patterns
  - Temporal anomalies (multiple invoices in short timeframes)
  - Due dates preceding invoice dates
  - Split invoices (dividing one payment into multiple smaller ones)
  - Duplicate invoices with slight variations

The fraud patterns are strategically injected with varying probabilities to create a realistic dataset for training and testing.

### Graph Data Model

The system uses a property graph model with:

- **Node types**:
  - `User`: Represents individuals or companies with attributes like name, email, phone, registration date, and VAT number
  - `Invoice`: Represents financial transactions with attributes including date, amount, IBAN, status, due date, and tax ID
- **Relationship types**:
  - `UPLOADED_BY`: Connects invoices to the users who created them
  - `NEEDS_PAYMENT_FROM`: Connects invoices to the users who need to pay them

This graph structure enables the identification of complex patterns like circular payments, unusual transaction frequencies, and suspicious user behaviors.

### Node2Vec for Feature Extraction

The system uses Memgraph’s MAGE `node2vec` algorithm to generate embeddings (vector representations) of each node in the graph. These embeddings are used as features in the classification step.

#### Parameters Used:

- `p = 1.0`: Return parameter (controls backtracking in walks)
  
- `q = 1.0`: In-out parameter (balances breadth/depth)
  
- `walk_length = 5`: Length of each walk
  
- `num_walks = 20`: Number of walks per node
  
- `dimensions = 64`: Size of the embedding vector
  
- `window_size = 5`: Context window for embedding
  

These embeddings encode both **node structure** and **neighborhood information**, enabling fraud detection that’s aware of surrounding context in the graph.

### Node Classification with Memgraph

After generating embeddings, the system uses Memgraph’s `node_classification` module to train a model that can classify nodes (invoices) as either **fraudulent** or **legitimate**.

#### Model Workflow:

1. **Label assignment**: A portion of invoice nodes are labeled based on the injected fraud patterns.
  
2. **Train/test split**: Typically 80% of labeled nodes for training, 20% for evaluation.
  
3. **Classifier training**: Uses the embeddings to learn patterns distinguishing fraud.
  
4. **Prediction**: Assigns fraud probabilities to previously unlabeled invoice nodes.
  

This process allows the system to **generalize from known fraud** and make predictions on new or unseen data points.

## Components

1. **Data Generator**: Creates synthetic invoice and user data with embedded fraud patterns
2. **Graph Database**: Memgraph for storing and querying connected data
3. **Web Dashboard**: Flask application for visualizing results and loading new data
4. **Machine Learning**: Node classification for fraud prediction

## Fraud Patterns

The system simulates several fraud patterns:

- Suspicious email patterns
- Invalid phone numbers
- Registration at unusual hours (2-4 AM)
- Suspicious VAT numbers (with patterns like "000", "999")
- Anomalous invoice amounts
- Invalid IBAN patterns
- Date inconsistencies (due date before invoice date)
- Duplicate invoices
- Temporal patterns (multiple invoices in short timeframes)
- Round amount invoices

## Prerequisites

- Docker
- Python 3.8 - 3.10
- Memgraph with MAGE extensions

## Installation

1. Clone this repository
  
2. Install dependencies:
  
  ```bash
  pip install -r requirements.txt
  ```
  
3. Start Memgraph:
  
  ```bash
  docker run -p 7687:7687 -p 7444:7444 --name memgraph -v "YOUR\\PATH\\TO\\WEBSITE\\FOLDER:/memgraph" memgraph/memgraph-mage
  ```
  

## Usage

### Generate Sample Data

```bash
python DatasetGenerator.py
```

This will create `InvoicesFraud.csv` with synthetic data containing fraud patterns.

### Load Data into Memgraph and Train Model

```bash
python MemgraphLoad.py
```

This script will:

1. Clear existing data
2. Load the CSV data into Memgraph
3. Create appropriate relationships
4. Generate embeddings using node2vec
5. Train and save a fraud detection model

### Run Web Dashboard

```bash
python dashboard.py
```

Access the dashboard at `http://127.0.0.1:5000` to:

- Generate new sample data
- Upload CSV files
- Get fraud predictions on new invoices

## Algorithms Used

The system uses the following Memgraph MAGE algorithms:

- `node2vec`: For generating node embeddings
- `node_classification`: For training and making predictions

## Troubleshooting

- **Cannot connect to Memgraph**: Ensure Docker is running and the container is up
- **CSV loading errors**: Check file path in Docker container (`/memgraph/InvoicesFraud.csv`)
- **Model training errors**: Make sure MAGE is available in your Memgraph instance

## Acknowledgements

- [Memgraph](https://memgraph.com/)
- [MAGE - Memgraph Advanced Graph Extensions](https://memgraph.com/docs/advanced-algorithms/install-mage)
- [Node2Vec Algorithm Documentation](https://memgraph.com/docs/advanced-algorithms/available-algorithms/node2vec)
- [GNN Node Classification Documentation](https://memgraph.com/docs/advanced-algorithms/available-algorithms/gnn_node_classification)