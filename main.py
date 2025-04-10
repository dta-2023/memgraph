import random
import csv
from datetime import datetime
import xgboost as xgb
import joblib
from faker import Faker
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from gqlalchemy import Memgraph

fake = Faker()

# Function to generate a unique VAT ID
def generate_unique_vat_id(used_vat_numbers):
    while True:
        vat_id = f"VAT{random.randint(100000000, 999999999)}"
        if vat_id not in used_vat_numbers:
            used_vat_numbers.add(vat_id)
            return vat_id

# Load the pre-trained model
model = joblib.load('fraud_detection_model.pkl')

# Load the label encoder for the status
label_encoder = LabelEncoder()
label_encoder.fit(['paid', 'pending', 'overdue'])  # You can adjust according to possible statuses

# Define the number of invoices to generate
num_invoices = 5  # Adjust the number of fraudulent invoices you want to create for the same user

# Generate a set of VAT numbers (for supplier)
used_vat_numbers = set()

# Generate a user for whom invoices will be uploaded
user_name = fake.name()
email = fake.unique.email()
phone_number = fake.phone_number()
registration_date = fake.date_this_decade().strftime('%Y-%m-%d %H:%M:%S')

# Generate a unique VAT ID for the user
vat_number = generate_unique_vat_id(used_vat_numbers)

# Add the user to the CSV and Memgraph in the next steps
file_path = r'C:\Users\filip\Desktop\S4_DTA\Memgraph_ML\invoice_with_fraud2.csv'

# Connect to Memgraph
memgraph = Memgraph("127.0.0.1", 7687)

# Add the user to Memgraph (only once)
memgraph.execute("""
    MERGE (u:User {VATNumber: $vat_number, userName: $user_name, email: $email, phoneNumber: $phone_number, registrationDate: $registration_date})
""", parameters={
    'vat_number': vat_number,
    'user_name': user_name,
    'email': email,
    'phone_number': phone_number,
    'registration_date': registration_date
})

# Generate and process each invoice
for _ in range(num_invoices):
    # Generate invoice details
    invoice_id = random.randint(1000, 9999)
    invoice_date = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')
    total_amount = random.randint(100000, 5000000)  # A very high amount to simulate a fraudulent invoice
    supplier_iban = fake.iban()
    status = random.choice(['paid', 'pending', 'overdue'])
    due_date = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')
    supplier_tax_id = generate_unique_vat_id(used_vat_numbers)

    # Create a dictionary with the invoice details
    new_invoice = {
        'invoice_id': invoice_id,
        'user_name': user_name,
        'email': email,
        'phone_number': phone_number,
        'registration_date': registration_date,
        'vat_number': vat_number,
        'invoice_date': invoice_date,
        'total_amount': total_amount,
        'supplier_iban': supplier_iban,
        'status': status,
        'due_date': due_date,
        'supplier_tax_id': supplier_tax_id
    }

    # Convert invoice data for prediction
    new_invoice_data = pd.DataFrame([{
        'total_amount': total_amount,
        'status': label_encoder.transform([status])[0],
        'due_date': pd.to_datetime(due_date).timestamp()
    }])

    # Convert data to DMatrix format for XGBoost
    new_data = xgb.DMatrix(new_invoice_data)

    # Predict whether the invoice is fraudulent
    prediction = model.predict(new_data)

    # Display prediction result
    fraud_label = 1 if prediction[0] > 0.5 else 0
    if fraud_label == 1:
        print(f"The invoice {invoice_id} is fraudulent (High amount).")
    else:
        print(f"The invoice {invoice_id} is legitimate.")

    # Add the invoice to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([invoice_id, user_name, email, phone_number, registration_date, vat_number,
                         invoice_id, user_name, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id, fraud_label])

    print(f"Invoice {invoice_id} added to the CSV file at {file_path}.")

    # Add the invoice and relationships to Memgraph
    memgraph.execute("""
        MERGE (i:Invoice {invoiceID: $invoice_id, invoiceDate: $invoice_date, totalAmount: $total_amount, supplierIBAN: $supplier_iban, status: $status, dueDate: $due_date, supplierTAXID: $supplier_tax_id, fraud: $fraud_label}) 
        MERGE (u:User {VATNumber: $vat_number, userName: $user_name, email: $email, phoneNumber: $phone_number, registrationDate: $registration_date}) 
        MERGE (u2:User {VATNumber: $supplier_tax_id}) 
        MERGE (u)-[:UPLOADED_BY]->(i) 
        MERGE (i)-[:NEEDS_PAYMENT_FROM]->(u2) 
    """, parameters={ 
        'vat_number': vat_number, 
        'user_name': user_name, 
        'email': email, 
        'phone_number': phone_number, 
        'registration_date': registration_date, 
        'invoice_id': invoice_id, 
        'invoice_date': invoice_date, 
        'total_amount': total_amount, 
        'supplier_iban': supplier_iban, 
        'status': status, 
        'due_date': due_date, 
        'supplier_tax_id': supplier_tax_id, 
        'fraud_label': fraud_label 
    })

    print(f"Invoice {invoice_id} and its relationships added to Memgraph.")

print("All invoices uploaded to Memgraph.")
