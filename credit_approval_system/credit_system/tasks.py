import os
import pandas as pd
from celery import shared_task
from .models import Customer, Loan

@shared_task
def import_customer_data(path='/app/credit_approval_system/credit_system/utils/customer_data.xlsx'):
    if Customer.objects.exists():
        import_loan_data.delay()
        return "Customer data already exists. Skipping."
        
    df = pd.read_excel(path)

    for _, row in df.iterrows():
        Customer.objects.create(
            first_name=row['First Name'],
            last_name=row['Last Name'],
            age=row['Age'],
            phone_number=row['Phone Number'],
            monthly_salary=row['Monthly Salary'],
            approved_limit=row['Approved Limit'],
            current_debt=0
        )

    # ✅ Trigger loan data import after customers are loaded
    import_loan_data.delay()
    return "Customer data imported. Loan task started."

@shared_task
def import_loan_data(path='/app/credit_approval_system/credit_system/utils/loan_data.xlsx'):
    if Loan.objects.exists():   
        return "Loan data already exists. Skipping."

    df = pd.read_excel(path)

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            Loan.objects.create(
                customer=customer,
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_installment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=pd.to_datetime(row['Date of Approval']),
                end_date=pd.to_datetime(row['End Date']),
            )
        except Customer.DoesNotExist:
            print(f"Customer with ID {row['Customer ID']} not found. Skipping loan import.")
            continue

    return "Loan data imported."
