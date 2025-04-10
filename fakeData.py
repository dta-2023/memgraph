import random
from faker import Faker
import csv
from datetime import datetime, timedelta
import os

fake = Faker()

num_users = 1000
num_invoices = 1000

users = []
invoices = []
used_vat_numbers = set()


def generate_unique_vat_id():
    while True:
        vat_id = f"VAT{random.randint(100000000, 999999999)}"
        if vat_id not in used_vat_numbers:
            used_vat_numbers.add(vat_id)
            return vat_id


for _ in range(num_users):
    user_name = fake.name()
    email = fake.unique.email()
    phone_number = fake.phone_number()
    
    if random.random() < 0.05:
        email = f"fake{random.randint(1000, 9999)}@example.com"
    
    if random.random() < 0.05:
        phone_number = "0000000000"
    
    registration_date = fake.date_this_decade().strftime('%Y-%m-%d %H:%M:%S')
    vat_number = generate_unique_vat_id()
    
    users.append([user_name, email, phone_number, registration_date, vat_number])

# Générer des factures avec une colonne 'fraud'
def generate_fraud_label(row):
    
    if row['total_amount'] > 5000:
        return 1 
    
  
    if row['total_amount'] < 50:
        return 1 
    
    return 0 


for i in range(num_invoices):
    user_id = random.randint(1, num_users)
    invoice_id = i + 1
    invoice_date = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')
    

    total_amount = round(random.uniform(50, 5000), 2)
    
    
    if random.random() < 0.2:
        user_invoices = [invoice for invoice in invoices if invoice[1] == user_id]
        if user_invoices:
            avg_amount = sum([invoice[3] for invoice in user_invoices]) / len(user_invoices)
            if random.random() < 0.5:
                total_amount = round(avg_amount + random.randint(1000, 5000), 2)
            else:
                total_amount = round(avg_amount - random.randint(1000, 5000), 2)
    
    supplier_iban = fake.iban()
    status = random.choice(['paid', 'pending', 'overdue'])
    
    
    if random.random() < 0.05:
        due_date = (datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S') - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S')
    else:
        due_date = (datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S')
    
    supplier_tax_id = random.choice(users)[4]

    invoices.append([invoice_id, user_id, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id])


output_dir = r'C:\Users\filip\Desktop\S4_DTA\Memgraph_ML'
os.makedirs(output_dir, exist_ok=True)

output_file_path = os.path.join(output_dir, 'invoice_with_fraud2.csv')

with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([ 
        'id', 'user_name', 'email', 'phone_number', 'registration_date', 'vat_number',
        'invoice_id', 'user_id', 'invoice_date', 'total_amount', 
        'supplier_iban', 'status', 'due_date', 'supplier_tax_id', 'fraud'
    ])
    
    for invoice in invoices:
        invoice_id, user_id, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id = invoice
        user = users[user_id - 1]
        
        
        fraud_label = generate_fraud_label({
            'total_amount': total_amount,
            'status': status,
            'invoice_date': invoice_date,
            'due_date': due_date,
            'supplier_tax_id': supplier_tax_id
        })
        
      
        writer.writerow([user_id] + user + [invoice_id, user_id, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id, fraud_label])

print(f"CSV file 'invoice_with_fraud.csv' created successfully in the {output_dir} directory.")
