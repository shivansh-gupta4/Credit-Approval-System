from datetime import date
from django.db.models import Sum
from credit_system.models import Customer, Loan

def months_between(start, end):
    """Returns the number of months between two dates, inclusive of the start month."""
    if end < start:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month) + 1

def calculate_credit_score(customer):
    """
    1. Past Loans Paid on Time (35%)
    2. No. of Loans Taken in Past (15%)
    3. Loan Activity in Current Year (10%)
    4. Loan Approved Volume (40%)
    """
    today = date.today()
    all_loans = Loan.objects.filter(customer=customer)
    active_loans = all_loans.filter(start_date__lte=today, end_date__gte=today)

    # 1. Past Loans Paid on Time (35%)
    total_emis_due = 0
    paid_emis = 0
    for loan in all_loans:
        if today < loan.start_date:
            due = 0
        elif today > loan.end_date:
            due = loan.tenure
        else:
            due = months_between(loan.start_date, today)
            due = min(due, loan.tenure)
        total_emis_due += due
        paid_emis += loan.emis_paid_on_time
    payment_ratio = min(paid_emis / total_emis_due if total_emis_due > 0 else 0, 1.0)
    payment_score = 35 * payment_ratio

    # 2. No. of Loans Taken in Past (15%)
    loan_count = all_loans.count()
    loan_count_score = max(0, 15 - 5 * (loan_count - 1))

    # 3. Loan Activity in Current Year (10%)
    current_year_loans = all_loans.filter(start_date__year=today.year).count()
    recent_loan_score = max(0, 10 - 5 * current_year_loans)

    # 4. Loan Approved Volume (40%)
    total_outstanding = sum(loan.loan_amount for loan in active_loans)
    utilization_ratio = total_outstanding / customer.approved_limit if customer.approved_limit > 0 else 1.0
    if utilization_ratio <= 0.3:
        utilization_score = 40
    elif utilization_ratio < 1.0:
        utilization_score = 40 * (1 - (utilization_ratio - 0.3) / 0.7)
    else:
        utilization_score = 0

    final_score = round(payment_score + loan_count_score + recent_loan_score + utilization_score)

    return {
        'score': final_score
    } 