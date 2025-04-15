# 🧠 Memgraph – Multi-Part Interactive Guide

This repository brings together four practical tutorials on using **Memgraph** with Python and graph theory concepts. Each folder represents one part of the project, and contains a dedicated guide and exercises.

---

## 📚 Table of Contents

1. [Cypher and Memgraph Introduction](#1-cypher-and-memgraph-introduction)
2. [Memgraph Python Guide](#2-memgraph-python-guide)
3. [Memgraph + Machine Learning](#3-memgraph--machine-learning)
4. [Full Fraud Detection Project](#4-full-fraud-detection-project)
5. [Environment Setup](#5-environment-setup)

---

## 1. Cypher and Memgraph Introduction

This part introduces the basics of the **Cypher query language** and how it is used with **Memgraph Lab**.  
You'll learn how to create nodes, relationships, and run queries directly using Cypher syntax.

📁 Folder: [`Cypher_and_memgraph_introduction`](./Cypher_and_memgraph_introduction)

---

## 2. Memgraph Python Guide

This tutorial focuses on using Memgraph with **Python**, via the `gqlalchemy` library.  
You'll build and query a graph through Python code and understand how to manipulate graph structures programmatically.

📁 Folder: [`Memgraph_Python_Guide`](./Memgraph_Python_Guide)

---

## 3. Memgraph + Machine Learning

This part integrates **graph data with machine learning**, using `xgboost`, `scikit-learn`, and more.  
It simulates fraudulent invoice detection with labeled data, training a predictive model.

📁 Folder: [`Memgraph_ML`](./Memgraph_ML)

---

## 4. Full Fraud Detection Project

This is a complete use case combining **graph database logic** with **interactive visualizations** and **dashboards** using `Flask`.  
It includes data generation, graph loading, algorithm execution, and results presentation.

📁 Folder: [`FraudDetectionMemgraph`](./FraudDetectionMemgraph)

---

## 5. Environment Setup

Follow these steps to set up your environment and run any of the four tutorials.

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/dta-2023/memgraph.git
cd memgraph
```

---

### 🐍 2. Create a Virtual Environment (Python 3.8 to 3.10)

```bash
python -m venv .venv
```

#### ✅ Activate it

- On **Windows**:

```bash
.venv\Scripts\activate
```

- On **macOS/Linux**:

```bash
source .venv/bin/activate
```

---

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🐳 4. Start Memgraph with Docker (Mage Version)

```bash
docker run -p 7687:7687 -p 7444:7444 --name memgraph ^
-v "YOUR\\PATH\\TO\\FOLDER:/memgraph" memgraph/memgraph-mage
```

---

### 🧪 5. Start Memgraph Lab (GUI)

```bash
docker run -d -p 3000:3000 --name lab memgraph/lab
```

---

### ⚠️ Optional – If Memgraph Lab Doesn’t Connect Properly

```bash
docker rm -f lab
docker run -d -p 3000:3000 -e QUICK_CONNECT_MG_HOST=host.docker.internal --name lab memgraph/lab
```

---

### ℹ️ Notes

- 🧠 Replace `"YOUR\\PATH\\TO\\FOLDER"` with the path where your files are located.
- 📍 Memgraph Lab is accessible at [http://localhost:3000](http://localhost:3000)
- 🧪 Memgraph runs on port `7687` using the **Bolt** protocol.
