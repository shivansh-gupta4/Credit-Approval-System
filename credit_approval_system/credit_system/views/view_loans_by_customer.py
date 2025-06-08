from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit_system.models import Loan, Customer
from credit_system.serializers import ViewLoansByCustomerResponseSerializer

@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)

    loan_data = []
    for loan in loans:
        repayments_left = loan.tenure - loan.emis_paid_on_time
        loan_data.append({
            "loan_id": loan.loan_id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "repayments_left": repayments_left
        })

    serializer = ViewLoansByCustomerResponseSerializer(loan_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
