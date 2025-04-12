from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import os
import csv
import random
from faker import Faker
from datetime import datetime, timedelta
from gqlalchemy import Memgraph
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Setup folders for file upload (host vs. container paths)
host_upload_folder = './'
container_upload_folder = '/memgraph'
os.makedirs(host_upload_folder, exist_ok=True)

# Connect to Memgraph database
memgraph = Memgraph("127.0.0.1", 7687)

app.secret_key = 'supersecretkey'

fake = Faker()

# Parameters for data generation
num_users = 2
num_invoices = 5
used_vat_numbers = set()

# Helper to generate a unique VAT ID

def generate_unique_vat_id():
    while True:
        vat_id = f"VAT{random.randint(100000000, 999999999)}"
        if vat_id not in used_vat_numbers:
            used_vat_numbers.add(vat_id)
            return vat_id

# Helper to generate a random datetime object
def get_random_date(start_year=2020, end_year=2025):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime(year, month, day, hour, minute, second)


# Fetch and update global last invoice ID from Memgraph
last_invoice_id = 2000

def get_last_invoice_id():
    global last_invoice_id
    try:
        query = "MATCH (i:Invoice) RETURN MAX(i.invoiceID) AS max_invoice_id"
        result = memgraph.execute_and_fetch(query)
        max_id = next(result, {}).get("max_invoice_id", 0)
        last_invoice_id = max_id if max_id is not None else 0
    except Exception as e:
        logger.error(f"Error fetching last invoice ID: {str(e)}")
        last_invoice_id = 0


# Generate synthetic CSV data for users and invoices
def generate_csv_data(num_invoices_to_generate=num_invoices):
    global last_invoice_id

    get_last_invoice_id()

    users = []
    for user_id in range(1, num_users + 1):
        user_name = fake.name()
        email = fake.unique.email()
        phone_number = fake.phone_number()
        registration_date = get_random_date().strftime('%Y-%m-%d %H:%M:%S')
        vat_number = generate_unique_vat_id()
        users.append([user_id, user_name, email, phone_number, registration_date, vat_number])


    # Create fake invoices linked to users
    invoices = []
    for _ in range(num_invoices_to_generate):
        last_invoice_id += 1  

        user_id = random.randint(1, num_users)
        invoice_date = get_random_date(2023, 2025).strftime('%Y-%m-%d %H:%M:%S')
        total_amount = round(random.uniform(50, 5000), 2)
        supplier_name = fake.company()
        supplier_iban = fake.iban()
        status_weights = [0.7, 0.2, 0.1]
        status = random.choices(['paid', 'pending', 'overdue'], weights=status_weights)[0]
        due_date = (datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(14, 60))).strftime('%Y-%m-%d %H:%M:%S')
        supplier_tax_id = random.choice(users)[5]

        invoices.append([last_invoice_id, user_id, invoice_date, total_amount, supplier_iban, supplier_name, status, due_date, supplier_tax_id])


    # Combine user and invoice data into a final dataset
    output_data = []
    for invoice in invoices:
        invoice_id, user_id, invoice_date, total_amount, supplier_iban, supplier_name, status, due_date, supplier_tax_id = invoice
        user = next((u for u in users if u[0] == user_id), None)
        if user:
            user_id, user_name, email, phone_number, registration_date, vat_number = user
            output_data.append([user_id, user_name, email, phone_number, registration_date, vat_number, invoice_id, invoice_date, total_amount, supplier_iban, supplier_name, status, due_date, supplier_tax_id])

    return output_data


# Load existing node classification model into Memgraph (for fraud detection)
def load_fraud_model():
    try:
        cypher_query = """
            CALL node_classification.load_model()
            YIELD path
            RETURN path;
        """
        result = memgraph.execute_and_fetch(cypher_query)
        model_path = next(result, {}).get("path", None)

        if model_path:
            logger.info(f"Model loaded from: {model_path}")
        else:
            logger.warning("No model found, make sure to train one first.")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")

# Load model at app startup
load_fraud_model()

# Route to generate and download fake invoice CSV
@app.route('/generate_csv', methods=['GET'])
def generate_csv():

    output_data = generate_csv_data()

    filename = 'InvoicesNoFraud.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'user_id', 'user_name', 'email', 'phone_number', 'registration_date', 'vat_number',
            'invoice_id', 'invoice_date', 'total_amount', 'supplier_iban', 'supplier_name',
            'status', 'due_date', 'supplier_tax_id'
        ])
        for row in output_data:
            writer.writerow(row)

    logger.info(f"CSV file '{filename}' created successfully")

    return send_file(filename, as_attachment=True)

# Route to handle file upload and trigger graph import + model prediction
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file:
        filepath = os.path.join(host_upload_folder, file.filename)
        file.save(filepath)

        try:
            print(f"{container_upload_folder}/{file.filename}")
            cypher_query = f"""
                LOAD CSV FROM "{container_upload_folder}/{file.filename}" WITH HEADER AS row
                CREATE (i:Invoice {{invoiceID: toInteger(row.invoice_id)}})
                SET
                    i.invoiceDate = row.invoice_date,
                    i.totalAmount = toFloat(row.total_amount),
                    i.supplierIBAN = row.supplier_iban,
                    i.status = row.status,
                    i.dueDate = row.due_date,
                    i.supplierTAXID = row.supplier_tax_id,
                    i.fraud = COALESCE(toInteger(row.fraud), -1)
                MERGE (u:User {{userID: toInteger(row.user_id)}})
                ON CREATE SET
                    u.VATNumber = row.vat_number,
                    u.userName = row.user_name,
                    u.email = row.email,
                    u.phoneNumber = row.phone_number,
                    u.registrationDate = row.registration_date,
                    u.fraud = COALESCE(toInteger(row.fraud), -1)
                CREATE (i)-[:UPLOADED_BY]->(u)
                WITH i, u, row
                MATCH (user_to_pay:User {{VATNumber: i.supplierTAXID}})
                WHERE user_to_pay.VATNumber IS NOT NULL AND i.supplierTAXID IS NOT NULL
                CREATE (i)-[:NEEDS_PAYMENT_FROM]->(user_to_pay);
            """

            try:
                memgraph.execute(cypher_query)
            except Exception as e:
                print(f"Error executing the Cypher query: {str(e)}")
                flash(f'Error executing the Cypher query: {str(e)}')
                return redirect(url_for('index'))
            try:
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
            except Exception as e:
                print(f"Error executing the Cypher query: {str(e)}")
                flash(f'Error executing the Cypher query: {str(e)}')
                return redirect(url_for('index'))
            
            
            fetch_new_invoice_ids_query = """
                MATCH (i:Invoice)
                WHERE i.fraud = -1
                RETURN i.invoiceID AS invoiceID;
            """
            new_invoices = memgraph.execute_and_fetch(fetch_new_invoice_ids_query)
            invoice_ids = [invoice['invoiceID'] for invoice in new_invoices]

            if not invoice_ids:
                logger.warning("No new invoices found for prediction.")
                return redirect(url_for('index'))

            fraud_results = []
            for invoice_id in invoice_ids:
                prediction_query = f"""
                    MATCH (n:Invoice {{invoiceID: {invoice_id}}})
                    CALL node_classification.predict(n)
                    YIELD predicted_class
                    SET n.fraud = predicted_class
                    RETURN n.invoiceID AS invoiceID, predicted_class;
                """
                prediction_result = memgraph.execute_and_fetch(prediction_query)
                fraud_results.extend(prediction_result)

            session['fraud_results'] = fraud_results

            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('index'))

# Main dashboard route
@app.route('/')
def index():
    fraud_results = session.pop('fraud_results', [])
    return render_template('index.html', fraud_results=fraud_results)
        

@app.route('/clear', methods=['POST'])
def clear_data():
    try:
        cypher_query = """
        MATCH (n)
        DETACH DELETE n
        """
        
        memgraph.execute(cypher_query)
        
        flash('All data successfully removed from Memgraph!')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Error while clearing data: {str(e)}')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
