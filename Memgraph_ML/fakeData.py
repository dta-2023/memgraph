# Import necessary libraries
import random
from faker import Faker
import csv
from datetime import datetime, timedelta
import os

# Initialize the Faker library to generate fake data
fake = Faker()

# Define the number of users and invoices to generate
num_users = 1000
num_invoices = 1000

# Lists to store generated users and invoices
users = []
invoices = []
used_vat_numbers = set()  # Set to ensure VAT IDs are unique

# Function to generate a unique VAT ID for each user
def generate_unique_vat_id():
    while True:
        vat_id = f"VAT{random.randint(100000000, 999999999)}"
        if vat_id not in used_vat_numbers:
            used_vat_numbers.add(vat_id)  # Add the generated VAT ID to the set
            return vat_id  # Return the unique VAT ID

# Generate 1000 fake users with random information
for _ in range(num_users):
    user_name = fake.name()  # Generate a random name
    email = fake.unique.email()  # Generate a unique email address
    phone_number = fake.phone_number()  # Generate a random phone number
    
    # Randomly change 5% of emails to fake ones for variety
    if random.random() < 0.05:
        email = f"fake{random.randint(1000, 9999)}@example.com"
    
    # Randomly change 5% of phone numbers to a placeholder value
    if random.random() < 0.05:
        phone_number = "0000000000"
    
    # Generate a random registration date within the last decade
    registration_date = fake.date_this_decade().strftime('%Y-%m-%d %H:%M:%S')
    vat_number = generate_unique_vat_id()  # Generate a unique VAT number for each user
    
    # Add the user to the users list
    users.append([user_name, email, phone_number, registration_date, vat_number])

# Function to generate a fraud label for an invoice based on its total amount
def generate_fraud_label(row):
    # If the total amount is above 5000, consider the invoice fraudulent
    if row['total_amount'] > 5000:
        return 1  # Fraudulent
    
    # If the total amount is less than 50, consider the invoice fraudulent
    if row['total_amount'] < 50:
        return 1  # Fraudulent
    
    return 0  # Legitimate invoice (not fraudulent)

# Generate 1000 fake invoices with fraud labels
for i in range(num_invoices):
    user_id = random.randint(1, num_users)  # Randomly select a user ID
    invoice_id = i + 1  # Invoice ID is sequential starting from 1
    invoice_date = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')  # Generate a random invoice date
    
    # Randomly generate a total amount between 50 and 5000
    total_amount = round(random.uniform(50, 5000), 2)
    
    # 20% chance to adjust the invoice amount based on the user's previous invoices
    if random.random() < 0.2:
        user_invoices = [invoice for invoice in invoices if invoice[1] == user_id]  # Get invoices for the selected user
        if user_invoices:
            avg_amount = sum([invoice[3] for invoice in user_invoices]) / len(user_invoices)  # Calculate the user's average invoice amount
            if random.random() < 0.5:
                total_amount = round(avg_amount + random.randint(1000, 5000), 2)  # Increase the amount based on average
            else:
                total_amount = round(avg_amount - random.randint(1000, 5000), 2)  # Decrease the amount based on average
    
    # Generate a random IBAN for the supplier
    supplier_iban = fake.iban()
    status = random.choice(['paid', 'pending', 'overdue'])  # Randomly choose an invoice status
    
    # Randomly adjust the due date by subtracting or adding up to 60 days from the invoice date
    if random.random() < 0.05:
        due_date = (datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S') - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S')
    else:
        due_date = (datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S')
    
    # Randomly choose a supplier's tax ID from the users
    supplier_tax_id = random.choice(users)[4]

    # Add the generated invoice to the invoices list
    invoices.append([invoice_id, user_id, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id])

# Define the output directory and ensure it exists
output_dir = r'C:\Users\filip\Desktop\S4_DTA\Memgraph_ML'
os.makedirs(output_dir, exist_ok=True)

# Define the output file path for the CSV file
output_file_path = os.path.join(output_dir, 'invoice_with_fraud2.csv')

# Write the generated data into a CSV file
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row for the CSV file
    writer.writerow([ 
        'id', 'user_name', 'email', 'phone_number', 'registration_date', 'vat_number',
        'invoice_id', 'user_id', 'invoice_date', 'total_amount', 
        'supplier_iban', 'status', 'due_date', 'supplier_tax_id', 'fraud'
    ])
    
    # Write each invoice with the generated fraud label
    for invoice in invoices:
        invoice_id, user_id, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id = invoice
        user = users[user_id - 1]  # Get the user data for this invoice
        
        # Generate the fraud label based on the invoice details
        fraud_label = generate_fraud_label({
            'total_amount': total_amount,
            'status': status,
            'invoice_date': invoice_date,
            'due_date': due_date,
            'supplier_tax_id': supplier_tax_id
        })
        
        # Write the invoice data and fraud label to the CSV file
        writer.writerow([user_id] + user + [invoice_id, user_id, invoice_date, total_amount, supplier_iban, status, due_date, supplier_tax_id, fraud_label])

# Print confirmation message that the CSV file has been created
print(f"CSV file 'invoice_with_fraud.csv' created successfully in the {output_dir} directory.")
