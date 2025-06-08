"""
URL configuration for credit_approval_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from credit_system.views import (
    register_customer,
    check_eligibility,
    create_loan,
    view_loan,
    view_loans_by_customer
)

def home(request):
    return HttpResponse("Welcome to Credit Approval System!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # API endpoints
    path('api/register/', register_customer, name='register'),
    path('api/check-eligibility/', check_eligibility, name='check-eligibility'),
    path('api/create-loan/', create_loan, name='create-loan'),
    path('api/view-loan/<int:loan_id>/', view_loan, name='view-loan'),
    path('api/view-loans/<int:customer_id>/', view_loans_by_customer, name='view-loans-by-customer'),
]
