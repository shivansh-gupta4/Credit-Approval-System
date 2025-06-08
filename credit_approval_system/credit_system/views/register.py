from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit_system.models import Customer
from credit_system.serializers import RegisterRequestSerializer, RegisterResponseSerializer

@api_view(['POST'])
def register_customer(request):     
    serializer = RegisterRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        approved_limit = round(data['monthly_income'] * 36 / 100000) * 100000
        
        customer = Customer.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=str(data['phone_number']),
            age=data['age'],
            monthly_salary=data['monthly_income'],
            approved_limit=approved_limit
        )
        
        response_data = {
            'customer_id': customer.customer_id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': data['age'],
            'monthly_income': customer.monthly_salary,
            'approved_limit': customer.approved_limit,
            'phone_number': int(customer.phone_number)
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)