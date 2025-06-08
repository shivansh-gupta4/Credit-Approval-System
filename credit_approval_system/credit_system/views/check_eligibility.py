from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit_system.serializers import CheckEligibilityRequestSerializer, CheckEligibilityResponseSerializer
from credit_system.utils.eligibility import evaluate_eligibility

@api_view(['POST'])
def check_eligibility(request):
        req_serializer = CheckEligibilityRequestSerializer(data=request.data)
        if req_serializer.is_valid():
            data = req_serializer.validated_data
            resp_data = evaluate_eligibility(data['customer_id'], data['loan_amount'], data['interest_rate'], data['tenure'])
            if 'message' in resp_data:
                del resp_data['message']
            resp_serializer = CheckEligibilityResponseSerializer(resp_data)
            return Response(resp_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
