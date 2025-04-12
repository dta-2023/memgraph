from gqlalchemy import Memgraph

# Establish a connection to the Memgraph instance
memgraph = Memgraph("127.0.0.1", 7687)

# Drop the existing database to start fresh
memgraph.drop_database()

# Load data for Invoices nodes and create the nodes in the graph
memgraph.execute("""
LOAD CSV FROM "/memgraph/InvoicesFraud.csv" WITH HEADER AS row
MERGE (i:Invoice {invoiceID: toInteger(row.invoice_id)})
ON CREATE SET
    i.invoiceDate = row.invoice_date,
    i.totalAmount = row.total_amount,
    i.supplierIBAN = row.supplier_iban,
    i.status = row.status,
    i.dueDate = row.due_date,
    i.supplierTAXID = row.supplier_tax_id,
    i.fraud = toInteger(row.fraud)
RETURN i;
""")

# Load data for User nodes and create the nodes in the graph
memgraph.execute("""
LOAD CSV FROM "/memgraph/InvoicesFraud.csv" WITH HEADER AS row
MERGE (u:User {userID: toInteger(row.user_id)})
ON CREATE SET
    u.id = id(u),
    u.VATNumber = row.vat_number,
    u.userName = row.user_name,
    u.email = row.email,
    u.phoneNumber = row.phone_number,
    u.registrationDate = row.registration_date,
    u.fraud = toInteger(row.fraud)
RETURN u;
""")

# Create relationships between Invoices and Users based on the uploaded invoice data
memgraph.execute("""
LOAD CSV FROM "/memgraph/InvoicesFraud.csv" WITH HEADER AS row
MATCH (i:Invoice {invoiceID: toInteger(row.invoice_id)})
MATCH (u:User {userID: toInteger(row.user_id)})
MERGE (i)-[:UPLOADED_BY]->(u)
RETURN i, u;
""")

# Create relationships between Invoices and Users based on the supplier's TAX ID
memgraph.execute("""
LOAD CSV FROM "/memgraph/InvoicesFraud.csv" WITH HEADER AS row
MATCH (i:Invoice {invoiceID: toInteger(row.invoice_id)})
WHERE i.supplierTAXID IS NOT NULL
MATCH (user_to_pay:User {VATNumber: i.supplierTAXID})
WHERE user_to_pay.VATNumber IS NOT NULL
MERGE (i)-[:NEEDS_PAYMENT_FROM]->(user_to_pay)
RETURN i, user_to_pay;
""")

# Perform the node2vec algorithm for graph embedding to create vector representations of nodes
memgraph.execute("""
 CALL node2vec.set_embeddings(
                    False,        
                    1.0,            
                    1.0,            
                    5,             
                    20,             
                    64,            
                    0.025,          
                    5,             
                    1,             
                    1,             
                    4,             
                    0.0001,         
                    1,             
                    0,             
                    5,             
                    5,             
                    "weight"        
                )
                YIELD *;
""")

# Set model parameters for node classification, targeting fraud detection as the classification task
memgraph.execute("""
  CALL node_classification.set_model_parameters(
    {layer_type: "GATJK", learning_rate: 0.001, hidden_features_size: [16,16], class_name: "fraud", features_name: "embedding"}
  ) YIELD aggregator, metrics
  RETURN aggregator, metrics;
""")

# Train the node classification model using the data and embeddings
memgraph.execute("""
CALL node_classification.train(80) PROCEDURE MEMORY UNLIMITED YIELD *;
""")

# Save the trained model for future use
memgraph.execute("""
  CALL node_classification.save_model() 
  YIELD *
  RETURN *
""")

print("Data loaded successfully!")