# 🧠 Memgraph + Python – Interactive Guide

Welcome to this interactive guide on using **Memgraph with Python** via the `gqlalchemy` library.  
This project demonstrates how to build, query, and manipulate a graph database for real-world use cases like **invoice fraud detection**.

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Setting up Python to use Memgraph with GQLAlchemy](#2-setting-up-python-to-use-memgraph-with-gqlalchemy)
3. [Building and Querying a Graph in Memgraph with Python (gqlalchemy)](#3-building-and-querying-a-graph-in-memgraph-with-python-gqlalchemy)
4. [Working with Graph Data using gqlalchemy](#4-working-with-graph-data-using-gqlalchemy)
5. [Practice Exercises](#5-practice-exercises)


---

# 1. Introduction


In this tutorial, you will learn how to interact with a graph database using **Memgraph** and **Python**.  
The goal is to understand how to model and query data in the form of nodes and relationships, while applying this knowledge to a realistic use case: **fraud detection through invoice analysis**.

This documentation is intended for beginners in graph databases, but assumes basic familiarity with Python.

---

## 🌐 What is Memgraph?

**Memgraph** is a high-performance, **in-memory graph database** that supports the **Cypher** query language (just like Neo4j).  
It is especially suited for real-time graph analysis and use cases such as:

- Recommendation systems (personalized suggestions)
- Fraud detection
- Social network analysis
- Transport/logistics graph modeling

---

## 🐍 Why use Python with Memgraph?

Cypher allows you to interact directly with Memgraph through the command line or visual tools like **Memgraph Lab**.  
But **Python** offers additional advantages:

- Automate interactions with the database
- Write graph analysis scripts
- Integrate Memgraph into web applications or data pipelines
- Visualize data using libraries like `networkx` or `matplotlib`

---

## 🧪 What will we build?

We will simulate a system where:
- **drivers** send **invoices**
- which are paid into **bank accounts**

The goal is to build a simple graph of these entities and then:
- learn to create and query it using Python,
- and eventually, **detect suspicious patterns** like multiple drivers using the same IBAN number.

👉 The purpose of this documentation is to teach you how to interact with Memgraph **through Python**, using step-by-step tutorials and practical exercises.

---

# 2. Setting up Python to use Memgraph with GQLAlchemy

> GQLAlchemy is an open-source Python library developed by Memgraph.  
> It works as an **Object Graph Mapper (OGM)**, meaning it lets you manipulate graph data using Python objects instead of manually writing Cypher queries.  
> It is compatible with **Memgraph** and **Neo4j**.

---

## ⚠️ Compatibility

- ❌ **Python 3.11 on Windows**: Not supported with GQLAlchemy  
- ✅ Recommended versions: **Python 3.8 to 3.10**  
- 🧪 Recommended environment: `venv` or `conda`

---

## 🛠️ Installation Steps

### 1. Create your project folder

```bash
mkdir memgraph_python
cd memgraph_python
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # on Windows
```

### 3. Install GQLAlchemy via pip

```bash
pip install gqlalchemy
```

---

## 🚀 Simple connection to Memgraph

Create a file named `program.py` with the following content:

```python
from gqlalchemy import Memgraph

# Connect to Memgraph (make sure port 7687 is exposed)
memgraph = Memgraph(host="127.0.0.1", port=7687)

# Delete existing data (optional)
memgraph.execute("MATCH (n) DETACH DELETE n")

# Create a test node
query = """
CREATE (n:FirstNode)
SET n.message = '{message}'
RETURN 'Node ' + id(n) + ': ' + n.message AS result
""".format(message="Hello, World!")

# Execute the query
results = memgraph.execute_and_fetch(query)

# Display the result
print(list(results)[0]['result'])
```

Run the script:

```bash
python program.py
```

---

## 💡 If the connection fails (common with Docker)

> Docker may assign a different internal IP instead of `127.0.0.1`.

To get the actual container IP address:

```bash
docker ps  # Get the CONTAINER_ID of your Memgraph container
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER_ID
```

Then update your script:

```python
memgraph = Memgraph(host="172.17.0.2", port=7687)  # Example IP
```

---

## 🧠 Learn More

- 📘 [GQLAlchemy How-To Guides](https://memgraph.github.io/gqlalchemy/) 
- ⭐ [GQLAlchemy GitHub Repository](https://github.com/memgraph/gqlalchemy)

---

## 📌 Important Notes

- Memgraph uses **port 7687** with the **Bolt** protocol  
- You can write raw Cypher queries directly in Python with `gqlalchemy`  
- You can also use **Memgraph Lab** at http://localhost:3000 to visualize your graph data

---

## 🔁 Alternatives to `gqlalchemy`

Before diving deeper into GQLAlchemy, it’s useful to know other tools that can also interact with graph databases like Memgraph or Neo4j.

---

### 🧩 Other Python libraries for graph databases

| Tool                     | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| **`gqlalchemy`**         | Official Memgraph library. Includes a query builder, OGM, and native support. |
| **`neo4j` Python driver**| Official Neo4j driver. Allows Cypher queries in Python. Compatible with Memgraph for basic usage. |

---

### 📊 Quick comparison: `gqlalchemy` vs `neo4j` Python driver

| Feature                    | `gqlalchemy`                             | `neo4j` Python driver                  |
|----------------------------|------------------------------------------|----------------------------------------|
| Compatibility              | ✅ Optimized for **Memgraph**            | ✅ Optimized for **Neo4j**, works with Memgraph |
| Object-oriented syntax     | ✅ Query builder                         | ❌ Raw Cypher strings only             |
| Cypher query execution     | ✅ `execute()` / `execute_and_fetch()`   | ✅ `.run()`                            |
| Learning curve             | 🟢 Easy for Python devs                  | 🟠 Requires Cypher fluency             |
| Built-in OGM               | ✅ Yes                                   | ❌ No                                  |
| Memgraph documentation     | 🟢 Official and focused                  | 🔶 Compatible but not emphasized       |
| Best use case              | Structured Memgraph projects             | Demos or Neo4j compatibility           |

---

## 🧩 Why Memgraph shows the Neo4j driver first

Memgraph’s official Quick Start starts with the Neo4j driver because:

- It’s widely recognized by Python developers  
- It allows you to quickly run Cypher queries  
- It demonstrates that **Memgraph is fully Cypher-compatible**

However, for production-ready Python projects that require clarity, structure, and maintainability,  
**`gqlalchemy` is the preferred tool**.

---
# 3. Building and Querying a Graph in Memgraph with Python (`gqlalchemy`)

---

## 🌟 What you’ll learn in this section

In this section, you will learn how to:

- Use `gqlalchemy`'s **query builder** methods: `create()`, `match()`, `to()`, `from_()`, etc.
- Create **nodes** and **relationships** in your graph using Python
- Use the `Memgraph` object to send queries
- Use the methods `execute()` and `execute_and_fetch()`
- Build a small invoice fraud scenario
- Perform **fraud detection**: e.g. multiple drivers using the same IBAN

> ⚠️ This section assumes you already understand the basics of the Cypher language (covered in your teammate’s section).  
> Here, we focus on **how to implement those queries in Python using `gqlalchemy`**.

---

## 📘 Core concepts of `gqlalchemy`

`gqlalchemy` allows you to write Cypher queries using a **Pythonic syntax**, known as a **DSL (Domain-Specific Language)**. This makes your queries more readable and structured.

| Method                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `Memgraph()`               | Creates a connection to the Memgraph database                               |
| `.execute()`               | Runs a Cypher query **without returning data**                              |
| `.execute_and_fetch()`     | Runs a Cypher query **with RETURN**, and fetches the results as a Python dict |
| `create()`                 | Starts a Cypher `CREATE` query                                              |
| `match()`                  | Starts a `MATCH` clause to find existing nodes/relationships                 |
| `.node()`                  | Adds a node to your query (can include labels, properties, variable)         |
| `.to()` / `.from_()`       | Defines a directed relationship between two nodes                           |
| `return_()`                | Defines what variables to return                                            |
| `limit()`, `order_by()`    | Filters or sorts query results                                              |

---

## 📂 Connecting to Memgraph

```python
from gqlalchemy import Memgraph

memgraph = Memgraph(host="127.0.0.1", port=7687)
```

> Make sure Memgraph is running on port 7687 (via Docker or locally).

---

## 🧹 Wipe the graph (optional)

```python
memgraph.execute("MATCH (n) DETACH DELETE n")
```

> This deletes all nodes and relationships in the graph.  
> It's useful when testing or resetting your data.

---

## 🏗️ Creating nodes with `create().node()`

### 🧠 Syntax Overview

The method `create().node()` lets you define a new node by passing:

- A **label** (e.g. `"Person"`, `"Invoice"`, `"Driver"`)
- One or more **properties** using keyword arguments

#### 🧾 General syntax:

```python
create().node(labels="Label", key1=value1, key2=value2).execute()
```

This is equivalent to the following Cypher query:

```cypher
CREATE (:Label {key1: value1, key2: value2})
```

---

### 💡 Examples: Creating nodes

```python
from gqlalchemy import create

# Create drivers
create().node(labels="Driver", name="John Doe", id="D001").execute()
create().node(labels="Driver", name="Jane Smith", id="D002").execute()
create().node(labels="Driver", name="Fake Driver", id="D003").execute()

# Create invoices
create().node(labels="Invoice", invoice_id="F001", amount=9500).execute()
create().node(labels="Invoice", invoice_id="F002", amount=9700).execute()
create().node(labels="Invoice", invoice_id="F003", amount=9500).execute()

# Create a bank account
create().node(labels="Bank", iban="CH93-0000-0000-0000-0001").execute()
```

---

## 🔗 Creating relationships with `match()` + `.to()` / `.from_()`

### 🧠 Syntax Overview

To create a relationship **between existing nodes**, you should:

1. Use `match()` to find both nodes  
2. Use `create()` to define the relationship between them

#### 🧾 General syntax:

```python
match()
  .node(labels="LabelA", property="value", variable="a")
  .match()
  .node(labels="LabelB", property="value", variable="b")
  .create()
  .node(variable="a").to("RELATIONSHIP").node(variable="b")
  .execute()
```

This creates a directed Cypher relationship:

```cypher
MATCH (a:LabelA {property: value}), (b:LabelB {property: value})
CREATE (a)-[:RELATIONSHIP]->(b)
```

---

### 💡 Example: Create a `SENT` relationship

```python
from gqlalchemy import match

match()
  .node(labels="Driver", name="John Doe", variable="driver")
  .match()
  .node(labels="Invoice", invoice_id="F001", variable="invoice")
  .create()
  .node(variable="driver").to("SENT").node(variable="invoice")
  .execute()
```

---

## 🔍 Fetching data with `execute_and_fetch()`

### 🧠 Syntax Overview

Use `execute_and_fetch()` when your query includes a `RETURN` clause.  
It allows you to retrieve results as Python dictionaries.

#### 🧾 General syntax:

```python
result = memgraph.execute_and_fetch("""
  YOUR CYPHER QUERY HERE
""")

for row in result:
    print(row["your_variable"])
```

---

### 💡 Example: fraud detection query

```python
results = memgraph.execute_and_fetch("""
MATCH (d:Driver)-[:SENT]->(:Invoice)-[:PAID_INTO]->(b:Bank)
WITH b.iban AS iban, collect(DISTINCT d.name) AS drivers, count(DISTINCT d.name) AS nb
WHERE nb > 1
RETURN iban, drivers, nb
""")

for row in results:
    print(f"⚠️ IBAN {row['iban']} used by {row['nb']} drivers: {row['drivers']}")
```

### ✅ Expected output:

```text
⚠️ IBAN CH93-0000-0000-0000-0001 used by 3 drivers: ['John Doe', 'Jane Smith', 'Fake Driver']
```

---

## 📊 Recap

By now, you should be able to:

- Connect to Memgraph using Python
- Create nodes and relationships using the query builder
- Execute Cypher queries from Python
- Fetch and print results from the graph
- Build a basic fraud detection script using graph patterns

---

👉 Want to go further?  
Check out the full documentation for more use cases and advanced features:  
📎 [GQLAlchemy How-To Guides](https://memgraph.github.io/gqlalchemy/)

## 4. Working with Graph Data using `gqlalchemy`

> ℹ️ Note: Some operations shown here (like updating or deleting nodes) are done using **raw Cypher executed via Python** (`memgraph.execute("...")`).  
> This is normal — the `gqlalchemy` query builder doesn’t cover all use cases yet. It’s common practice to use raw Cypher when it simplifies your logic or increases flexibility.

---

### 🧠 Goal of this section

In this section, you’ll learn how to manipulate graph data in Memgraph using Python and `gqlalchemy`. This includes:

- Reading existing nodes and relationships
- Updating node properties
- Deleting nodes or relationships
- Filtering data using `WHERE` and conditional queries

> These operations are essential when refining your graph to reflect business needs (e.g., invoice updates, bank account deletion, etc.)

---

### 🔍 Reading nodes and relationships

#### General syntax

```python
match()
  .node(labels="Label", variable="n")
  .return_()
  .execute()
```

#### Example: read all drivers

```python
from gqlalchemy import match

results = match().node(labels="Driver", variable="d").return_().execute()
for r in results:
    print(r["d"])
```

---

### ✏️ Updating a property

> Use a raw Cypher query through `execute()` to update an existing node.

#### Example: change a driver's name

```python
memgraph.execute("""
MATCH (d:Driver {id: 'D001'})
SET d.name = 'John Updated'
""")
```

---

### 🗑 Deleting a node or relationship

#### Delete a node (and its relationships)

```python
memgraph.execute("""
MATCH (n:Bank {iban: 'CH93-0000-0000-0000-0001'})
DETACH DELETE n
""")
```

#### Delete only a relationship

```python
memgraph.execute("""
MATCH (:Driver {name: 'John Doe'})-[r:SENT]->(:Invoice {invoice_id: 'F001'})
DELETE r
""")
```

> `DETACH DELETE` removes the node and all its connected relationships.

---

### 🔍 Filtering with `WHERE`

#### Example: list all invoices greater than 9000 CHF

```python
results = memgraph.execute_and_fetch("""
MATCH (i:Invoice)
WHERE i.amount > 9000
RETURN i.invoice_id, i.amount
""")
for r in results:
    print(r)
```

#### Example: find all drivers whose name starts with "J"

```python
results = memgraph.execute_and_fetch("""
MATCH (d:Driver)
WHERE d.name STARTS WITH 'J'
RETURN d.name
""")
for r in results:
    print(r)
```

---

### ✅ Summary

By now, you should be able to:

- Read nodes using labels or filters
- Update existing data in your graph
- Delete nodes or specific relationships
- Use `WHERE` to refine your queries

These techniques make your graph dynamic and adaptable to real-world business logic.

---

## 5. Practice Exercises

> ℹ️ For each exercise, you can rely on the examples and theory presented in **Section 3**.  
> You are encouraged to draw inspiration from them, but avoid copy-pasting.  
> Try adapting the structure to new data or contexts.

---

### Exercise 1 – Creating simple nodes

🎯 **Goal**: Create 3 nodes representing drivers.

- Create three nodes of type `Driver` with properties `name` and `id`.
- Use a query to check their presence in the database.

**Expected result**: A list containing the 3 created `Driver` nodes.

---

### Exercise 2 – Creating a minimal invoice graph

🛠 **Bonus**: Delete one of the created drivers or invoices using a `DETACH DELETE` query, as shown in the manipulation section.

🎯 **Goal**: Create relationships in a small invoice graph.

- Create two drivers, two invoices, and one bank account.
- Create the relationships `SENT` and `PAID_INTO` as demonstrated.

**Expected result**: A graph with 5 nodes and 4 relationships.

---

### Exercise 3 – List invoices sent by a driver

🎯 **Goal**: Use a query with `execute_and_fetch()`.

- Retrieve the name of a driver and the list of invoices they sent.
- Display the pairs `Driver.name` → `Invoice.invoice_id`.

**Expected result**: One line per `SENT` relationship showing both values.

---

### Exercise 4 – Basic fraud detection

🎯 **Goal**: Detect IBANs used by more than one driver.

- Use the analysis code provided in Section 3.
- Add a new `Driver` node that uses the same IBAN as others.

**Expected result**: An alert listing the IBAN and the names of the drivers involved.

---

### Exercise 5 – Bonus: Create a `detect_fraud()` Python function

🛠 **Bonus**: Add a filter to only return cases where more than **2** drivers use the same IBAN (using `WHERE`).

🎯 **Goal**: Transform the fraud detection logic into a reusable function.

- Create a `detect_fraud()` function that encapsulates the `MATCH`/`RETURN` logic.
- Return a list of formatted alerts.

**Expected result**: The function can be reused in any Python analysis script.

---

### Exercise 6 – Full node manipulation cycle

🎯 **Goal**: Practice graph operations (read, update, delete).

1. Create a `Driver` node named `"Temp User"` with a unique ID (e.g. `id="TEMP123"`).
2. Read the node from the database and print its name and ID.
3. Update the `name` property to `"Temp Updated"`.
4. Read the node again to verify the update.
5. Delete the node using `DETACH DELETE`.
6. Check that it no longer exists in the graph.

**Expected result**:

- The node is created and visible with its initial name.
- After the update, the name has changed.
- After deletion, the node no longer appears in results.

---

### ▶️ How to run the exercises

All exercises can be completed inside a single Python file or a Jupyter notebook.  
It is recommended to start with a clean graph before each run using:

```python
memgraph.execute("MATCH (n) DETACH DELETE n")
```
📂 **You can find the full solutions in the file** [`main.py`](./main.py) **at the root of this repository**.

💡 **Don't forget to import the necessary libraries** at the top of your file:

```python
from gqlalchemy import Memgraph, create, match
