from gqlalchemy import Memgraph

# Connect to the Memgraph database
memgraph = Memgraph("127.0.0.1", 7687)

# If you want to clean the database before loading new data
memgraph.drop_database()

# Load data from the CSV file and add the 'fraud' label
memgraph.execute("""
    LOAD CSV FROM "/mnt/data/invoice_with_fraud2.csv" WITH HEADER AS row
    MERGE (u:User {VATNumber: row.vat_number, userName: row.user_name, email: row.email, phoneNumber: row.phone_number, registrationDate: row.registration_date})
    MERGE (i:Invoice {invoiceID: row.invoice_id, invoiceDate: row.invoice_date, totalAmount: row.total_amount, supplierIBAN: row.supplier_iban, status: row.status, dueDate: row.due_date, supplierTAXID: row.supplier_tax_id, fraud: toInteger(row.fraud)})
    MERGE (u2:User {VATNumber: row.supplier_tax_id})
    MERGE (u)-[:UPLOADED_BY]->(i)
    MERGE (i)-[:NEEDS_PAYMENT_FROM]->(u2);
""")

print("Data loaded into Memgraph successfully.")
