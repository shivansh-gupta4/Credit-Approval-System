import math
from datetime import date
from credit_system.models import Customer, Loan
from credit_system.utils.credit_score import calculate_credit_score

def evaluate_eligibility(customer_id, loan_amount, interest_rate, tenure):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return {"error": "Customer not found"}

    today = date.today()
    active_loans = Loan.objects.filter(
        customer=customer,
        start_date__lte=today,
        end_date__gte=today
    )

    total_emi = sum(loan.monthly_installment for loan in active_loans)
    monthly_emi_requested_loan = loan_amount * interest_rate / 12 / 100 * ((1 + interest_rate / 12 / 100) ** tenure) / (((1 + interest_rate / 12 / 100) ** tenure) - 1)
    total_emi = total_emi + monthly_emi_requested_loan
    if total_emi > 0.5 * customer.monthly_salary:
        return build_response(False, customer_id, loan_amount, interest_rate, tenure, corrected_rate=16, message="EMI exceeds 50% of monthly salary")

    total_outstanding = sum(loan.loan_amount for loan in active_loans)
    total_outstanding = total_outstanding + loan_amount
    if total_outstanding > customer.approved_limit:
        return build_response(False, customer_id, loan_amount, interest_rate, tenure, corrected_rate=16, message="Outstanding loan amount exceeds approved limit")

    credit_score_data = calculate_credit_score(customer)
    credit_score = credit_score_data['score']

    if credit_score > 50:
        threshold = interest_rate
    elif credit_score > 30:
        threshold = 12.0
    elif credit_score > 10:
        threshold = 16.0
    else:
        return build_response(False, customer_id, loan_amount, interest_rate, tenure, corrected_rate=16, message="Credit score is too low")

    if interest_rate < threshold:
        return build_response(False, customer_id, loan_amount, interest_rate, tenure, corrected_rate=threshold, message="Interest rate is too low")
    
    return build_response(True, customer_id, loan_amount, interest_rate, tenure, corrected_rate=threshold, message="Loan approved")

def build_response(approval, customer_id, loan_amount, interest_rate, tenure, corrected_rate=None, message=None):
    r = (corrected_rate or interest_rate) / 12 / 100
    n = tenure
    P = loan_amount
    if r > 0:
        emi = P * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    else:
        emi = P / n
    return {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_rate,
        "tenure": tenure,
        "monthly_installment": round(emi, 2),
        "message": message
    }
