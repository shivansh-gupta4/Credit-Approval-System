from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit_system.models import Loan, Customer
from credit_system.serializers import CreateLoanRequestSerializer, CreateLoanResponseSerializer
from credit_system.utils.eligibility import evaluate_eligibility
from datetime import date, timedelta

@api_view(['POST'])
def create_loan(request):
    serializer = CreateLoanRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        resp_data = evaluate_eligibility(data['customer_id'], data['loan_amount'], data['interest_rate'], data['tenure'])
        if resp_data.get("approval") is False:
            loan_id = None
            loan_approved = False
        else:
            today = date.today()
            end_date = today + timedelta(days=30 * data["tenure"])
            
            customer = Customer.objects.get(customer_id=data["customer_id"])

            loan = Loan.objects.create(
                customer=customer,
                loan_amount=data["loan_amount"],
                tenure=data["tenure"],
                interest_rate=data["interest_rate"],
                monthly_installment=resp_data["monthly_installment"],
                emis_paid_on_time=0,
                start_date=today,
                end_date=end_date,
            )
            loan_id = loan.loan_id
            loan_approved = True

        response = {
            "loan_id": loan_id,
            "customer_id": data["customer_id"],
            "loan_approved": loan_approved,
            "message": resp_data["message"],
            "monthly_installment": resp_data["monthly_installment"]
        }
        return Response(CreateLoanResponseSerializer(response).data, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)