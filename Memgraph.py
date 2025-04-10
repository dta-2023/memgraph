from gqlalchemy import Memgraph

# Connexion à la base de données Memgraph
memgraph = Memgraph("127.0.0.1", 7687)

# Si vous souhaitez nettoyer la base avant de charger de nouvelles données
memgraph.drop_database()

# Charger les données à partir du fichier CSV en ajoutant le label 'fraud'
memgraph.execute("""
    LOAD CSV FROM "/mnt/data/invoice_with_fraud2.csv" WITH HEADER AS row
    MERGE (u:User {VATNumber: row.vat_number, userName: row.user_name, email: row.email, phoneNumber: row.phone_number, registrationDate: row.registration_date})
    MERGE (i:Invoice {invoiceID: row.invoice_id, invoiceDate: row.invoice_date, totalAmount: row.total_amount, supplierIBAN: row.supplier_iban, status: row.status, dueDate: row.due_date, supplierTAXID: row.supplier_tax_id, fraud: toInteger(row.fraud)})
    MERGE (u2:User {VATNumber: row.supplier_tax_id})
    MERGE (u)-[:UPLOADED_BY]->(i)
    MERGE (i)-[:NEEDS_PAYMENT_FROM]->(u2);
""")

print("Data loaded into Memgraph successfully.")






