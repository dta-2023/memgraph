# Introduction to Cypher

## 1.1 What is a Graph-Oriented Database?

Graph-oriented databases are a type of database designed to store and query complex relationships between data. Unlike relational databases that use tables and joins, they model data as **nodes** (entities) and **relationships** (links between those entities).

This approach is particularly suited for systems where relationships are as important as the data itself, such as social networks, recommendation engines, fraud detection, or logistics management.

## 1.2 Comparison with Relational Databases

Relational databases structure data into tables, with relationships defined through foreign keys. However, as relationships become more complex, relational databases may experience performance drops due to the number of joins required to retrieve linked information.

In contrast, graph databases enable smooth navigation thanks to a native model based on direct connections between data. Queries are often more readable and faster because they directly utilize the relationships recorded in the graph without the need for multiple joins.

## 1.3 Why Use Neo4j and Cypher?

**Neo4j** is one of the most popular graph database management systems. It provides optimized performance for complex relational queries and integrates well with modern technologies.

**Cypher** is the query language used by Neo4j. Its declarative approach, inspired by SQL, allows for readable and intuitive queries to manipulate and interrogate the graph. Unlike traditional languages that require complex nested queries, Cypher simplifies relationship exploration using an expressive and efficient syntax.

With Neo4j and Cypher, it becomes easier to model dynamic and interconnected systems while maintaining good performance—even with large data volumes.

...

# 5. Reading and Querying the Graph

## Basic Query with MATCH

```cypher
MATCH (c:Country)
RETURN c.name, c.balance
```

## Filtering with WHERE

```cypher
MATCH (c:Country)
WHERE c.balance > 0 AND c.total_export_amount > 100000
RETURN c.name, c.balance, c.total_export_amount
```

## Relationships between countries

```cypher
MATCH (c:Country)-[r:EXPORTS]->(s:Country {name: 'Switzerland'})
RETURN c.name, r.amount
```

## Aggregation

```cypher
MATCH (c:Country)
RETURN SUM(c.total_export_amount) AS total_exports
```

## Calculating Trade Balance for Each Country

```cypher
MATCH (c:Country)
RETURN c.name, c.total_export_amount - c.total_import_amount AS balance
```

## Path Exploration

```cypher
MATCH path = (c:Country)-[:EXPORTS*1..3]->(s:Country {name: 'Switzerland'})
RETURN path
```