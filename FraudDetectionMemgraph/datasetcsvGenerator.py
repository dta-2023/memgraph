import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

num_users = 1000 # Number of users to generate
num_invoices = 1500 # Number of invoices to generate
used_vat_numbers = set() # To keep track of unique VAT numbers
fraud_patterns = {} # Dictionary to track various fraud patterns

# Function to generate a unique VAT ID
def generate_unique_vat_id():
    while True:
        vat_id = f"VAT{random.randint(100000000, 999999999)}"
        if vat_id not in used_vat_numbers:
            used_vat_numbers.add(vat_id)
            return vat_id

# Function to generate a random date within a given year range
def get_random_date(start_year=2020, end_year=2025):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime(year, month, day, hour, minute, second)

# Generate user data
users = []
for user_id in range(1, num_users + 1):
    user_name = fake.name()
    email = fake.unique.email()
    is_fraud_user = 0

    # Randomly introduce fraudulent patterns in email
    if random.random() < 0.15:
        is_fraud_user = 1
        fraud_patterns['suspicious_email'] = fraud_patterns.get('suspicious_email', 0) + 1
        
        # Generate suspicious email patterns for fraud users
        email_pattern = random.choice([
            f"{fake.first_name().lower()}{random.randint(1000, 9999)}@gmail.com",
            f"{user_name.replace(' ', '').lower()}{random.choice(['123', '999', '007'])}@mail.com", 
            f"{fake.word()}{fake.word()}@{random.choice(['freemail.com', 'examplemail.com', 'tempmail.net'])}",
            f"{fake.first_name().lower()}.{random.randint(100, 999)}@{fake.domain_name()}", 
            f"{fake.word()}.{fake.word()}{random.randint(1, 99)}@gmail.com",
        ])
        email = email_pattern
    
    # Randomly introduce fraudulent phone number patterns
    phone_number = fake.phone_number()
    if random.random() < 0.1 and is_fraud_user == 0:
        is_fraud_user = 1
        fraud_patterns['invalid_phone'] = fraud_patterns.get('invalid_phone', 0) + 1
        
        phone_pattern = random.choice([
            "0000000000",
            "1234567890",
            "+00 000 000 0000", 
            "123-456-7890",
            "999-999-9999",
            phone_number[:-5] + "00000" 
        ])
        phone_number = phone_pattern
    
    # Generate registration date and apply suspicious pattern
    registration_date = get_random_date().strftime('%Y-%m-%d %H:%M:%S')
    vat_number = generate_unique_vat_id()
    
    # Randomly introduce fraudulent registration patterns
    if random.random() < 0.08 and is_fraud_user == 0:
        is_fraud_user = 1
        fraud_patterns['suspicious_registration'] = fraud_patterns.get('suspicious_registration', 0) + 1
        
        registration_datetime = datetime.strptime(registration_date, '%Y-%m-%d %H:%M:%S')
        suspicious_hour = random.randint(2, 4)
        registration_datetime = registration_datetime.replace(hour=suspicious_hour, minute=random.randint(0, 59))
        registration_date = registration_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    # Randomly introduce suspicious VAT numbers
    if random.random() < 0.07 and is_fraud_user == 0:
        is_fraud_user = 1
        fraud_patterns['suspicious_vat'] = fraud_patterns.get('suspicious_vat', 0) + 1
        
        last_digits = random.choice(["000", "999", "123", "111", "222"])
        vat_number = f"VAT{vat_number[3:-3]}{last_digits}"
    
    users.append([user_id, user_name, email, phone_number, registration_date, vat_number, is_fraud_user])

# Generate invoice data
invoices = []
recent_invoices = {}

# Generate a list of invoices for users
for i in range(num_invoices):
    invoice_id = i + 1
    user_id = random.randint(1, num_users)
    invoice_date = get_random_date(2023, 2025).strftime('%Y-%m-%d %H:%M:%S')
    total_amount = round(random.uniform(50, 5000), 2)
    is_fraud_invoice = 0
    
    user = next((u for u in users if u[0] == user_id), None)
    
    # Randomly introduce fraudulent invoice patterns (amount)
    if random.random() < 0.12:
        is_fraud_invoice = 1
        fraud_patterns['suspicious_amount'] = fraud_patterns.get('suspicious_amount', 0) + 1
        
        amount_pattern = random.choice([
            round(random.uniform(9900, 10100), 2), 
            round(random.uniform(15000, 25000), 2), 
            round(random.uniform(1, 10), 2), 
            round(float(random.choice([1111.11, 2222.22, 3333.33, 4444.44, 5555.55])), 2), 
            round(random.choice([99.99, 199.99, 299.99, 399.99, 499.99]), 2)
        ])
        total_amount = amount_pattern
    
    supplier_name = fake.company()
    supplier_iban = fake.iban()
    
    # Randomly introduce fraudulent IBAN patterns
    if random.random() < 0.08 and is_fraud_invoice == 0:
        is_fraud_invoice = 1
        fraud_patterns['suspicious_iban'] = fraud_patterns.get('suspicious_iban', 0) + 1
        
        country_code = random.choice(["XX", "YY", "ZZ", "00"])
        check_digits = random.choice(["00", "99", "01"])
        rest_of_iban = ''.join(random.choices("0123456789", k=20))
        supplier_iban = f"{country_code}{check_digits}{rest_of_iban}"
    
    status_weights = [0.7, 0.2, 0.1]
    status = random.choices(['paid', 'pending', 'overdue'], weights=status_weights)[0]
    
    invoice_datetime = datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S')
    
    # Randomly introduce date inconsistencies
    if random.random() < 0.07 and is_fraud_invoice == 0:
        is_fraud_invoice = 1
        fraud_patterns['date_inconsistency'] = fraud_patterns.get('date_inconsistency', 0) + 1
        
        days_before = random.randint(1, 60)
        due_date = (invoice_datetime - timedelta(days=days_before)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        days_after = random.randint(14, 60)
        due_date = (invoice_datetime + timedelta(days=days_after)).strftime('%Y-%m-%d %H:%M:%S')
    
    if is_fraud_invoice == 1 and random.random() < 0.5:
        supplier_tax_id = f"VAT{random.choice(['000000000', '123456789', '999999999'])}"
    else:
        supplier_tax_id = random.choice(users)[5]
    
    # Track recent invoices for potential duplicate fraud patterns
    if user_id not in recent_invoices:
        recent_invoices[user_id] = []
    
    invoice_record = [invoice_id, user_id, invoice_date, total_amount, supplier_iban, supplier_name, 
                      status, due_date, supplier_tax_id, is_fraud_invoice]
    
    invoices.append(invoice_record)
    recent_invoices[user_id].append(invoice_record)
    
    # Introduce fraudulent duplicate invoices randomly
    if random.random() < 0.06:
        fraud_patterns['duplicate_invoice'] = fraud_patterns.get('duplicate_invoice', 0) + 1
        
        duplicate_invoice_id = len(invoices) + 1
        
        time_shift = random.randint(1, 72)
        duplicate_invoice_date = (invoice_datetime + timedelta(hours=time_shift)).strftime('%Y-%m-%d %H:%M:%S')
        
        dup_strategy = random.randint(1, 4)
        if dup_strategy == 1:
            duplicate_total_amount = total_amount
        elif dup_strategy == 2:
            duplicate_total_amount = round(total_amount * random.uniform(0.95, 1.05), 2)
        elif dup_strategy == 3:
            split_factor = random.uniform(0.3, 0.7)
            duplicate_total_amount = round(total_amount * split_factor, 2)
            total_amount = round(total_amount * (1 - split_factor), 2)
            invoices[-1][3] = total_amount
        else:
            duplicate_total_amount = round(total_amount)
        
        duplicate_record = [duplicate_invoice_id, user_id, duplicate_invoice_date, duplicate_total_amount, 
                           supplier_iban, supplier_name, status, due_date, supplier_tax_id, 1]
        
        invoices.append(duplicate_record)
        recent_invoices[user_id].append(duplicate_record)
    
    # Check for temporal patterns in recent invoices
    if len(recent_invoices[user_id]) >= 3:
        recent_three = recent_invoices[user_id][-3:]
        
        # Calculate time differences between consecutive invoices
        date1 = datetime.strptime(recent_three[0][2], '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(recent_three[1][2], '%Y-%m-%d %H:%M:%S')
        date3 = datetime.strptime(recent_three[2][2], '%Y-%m-%d %H:%M:%S')
        
        time_diff1 = abs((date2 - date1).total_seconds() / 3600)  
        time_diff2 = abs((date3 - date2).total_seconds() / 3600)  
        
     
        if time_diff1 < 2 and time_diff2 < 2 and random.random() < 0.8:
            fraud_patterns['temporal_pattern'] = fraud_patterns.get('temporal_pattern', 0) + 1
            
           
            if invoices[-1][9] == 0:
                invoices[-1][9] = 1 
    
    # Add a fraudulent round amount if certain conditions are met
    if is_fraud_invoice == 0 and total_amount == round(total_amount) and random.random() < 0.4:
        fraud_patterns['round_amount'] = fraud_patterns.get('round_amount', 0) + 1
        invoices[-1][9] = 1 

# Prepare the final output data and write to a CSV file
output_data = []
for invoice in invoices:
    invoice_id, user_id, invoice_date, total_amount, supplier_iban, supplier_name, status, due_date, supplier_tax_id, is_fraud_invoice = invoice
    
    user = next((u for u in users if u[0] == user_id), None)
    if user:
        user_id, user_name, email, phone_number, registration_date, vat_number, is_fraud_user = user
        
        fraud_label = 1 if is_fraud_user == 1 or is_fraud_invoice == 1 else 0
        
        output_data.append([
            user_id, user_name, email, phone_number, registration_date, vat_number, 
            invoice_id, invoice_date, total_amount, supplier_iban, supplier_name, 
            status, due_date, supplier_tax_id, fraud_label
        ])

# Write the output data to CSV
with open('InvoicesFraud.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow([
        'user_id', 'user_name', 'email', 'phone_number', 'registration_date', 'vat_number',
        'invoice_id', 'invoice_date', 'total_amount', 'supplier_iban', 'supplier_name',
        'status', 'due_date', 'supplier_tax_id', 'fraud'
    ])
    
    for row in output_data:
        writer.writerow(row)

print(f"Generated {num_users} users and {len(invoices)} invoices")
print(f"Total fraudulent entries: {sum(1 for row in output_data if row[14] == 1)}")
print("\nFraud pattern distribution (internal reference only):")
for pattern, count in fraud_patterns.items():
    print(f"- {pattern}: {count} instances")

print("\nCSV file 'EnhancedInvoiceFraud.csv' created successfully")