from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit_system.models import Loan
from credit_system.serializers import ViewLoanResponseSerializer

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        try:
            loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ViewLoanResponseSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)