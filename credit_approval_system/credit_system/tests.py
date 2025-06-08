from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from credit_system.models import Customer, Loan
from datetime import date, timedelta

class APITests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Adena",
            last_name="Serrano",
            phone_number="9850668363",
            monthly_salary=108000,
            approved_limit=2400000,
            age=43
        )
        self.loan1 = Loan.objects.create(
            customer=self.customer,
            loan_amount=900000,
            tenure=153,
            interest_rate=15.77,
            monthly_installment=34096,
            emis_paid_on_time=109,
            start_date=date(2013, 7, 9),
            end_date=date(2026, 4, 9)
        )
        self.loan2 = Loan.objects.create(
            customer=self.customer,
            loan_amount=100000,
            tenure=54,
            interest_rate=12.09,
            monthly_installment=2923,
            emis_paid_on_time=27,
            start_date=date(2019, 5, 27),
            end_date=date(2023, 11, 27)
        )

    def test_register_customer(self):
        response = self.client.post("/api/register/", {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "monthly_income": 80000,
            "phone_number": "9998887770"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("customer_id", response.data)

    def test_check_eligibility_reject_due_to_emi_burden(self):
        Loan.objects.create(
            customer=self.customer,
            loan_amount=300000,
            tenure=36,
            interest_rate=12.5,
            monthly_installment=60000,
            emis_paid_on_time=20,
            start_date=date(2024, 1, 1),
            end_date=date(2026, 1, 1)
        )

        response = self.client.post("/api/check-eligibility/", {
            "customer_id": self.customer.customer_id,
            "loan_amount": 50000,
            "interest_rate": 10.0,  
            "tenure": 12
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["approval"])

    def test_check_eligibility_approve(self):
        response = self.client.post("/api/check-eligibility/", {
            "customer_id": self.customer.customer_id,
            "loan_amount": 50000,
            "interest_rate": 10.0,
            "tenure": 12
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["approval"])

    def test_create_loan_success(self):
        response = self.client.post("/api/create-loan/", {
            "customer_id": self.customer.customer_id,
            "loan_amount": 60000,
            "interest_rate": 11.0,
            "tenure": 12
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["loan_approved"])

    def test_view_loans_for_customer(self):
        new_loan = Loan.objects.create(
            customer=self.customer, 
            loan_amount=100000,
            tenure=24,
            interest_rate=10.0,
            monthly_installment=4700,
            emis_paid_on_time=20,
            start_date=date(2023, 1, 1),
            end_date=date(2025, 1, 1)
        )
        
        response = self.client.get(f"/api/view-loans/{self.customer.customer_id}/")
        self.assertEqual(response.status_code, 200)
        response_loan_ids = {loan["loan_id"] for loan in response.data}
        expected_loan_ids = {self.loan1.loan_id, self.loan2.loan_id, new_loan.loan_id}
        self.assertEqual(response_loan_ids, expected_loan_ids)
