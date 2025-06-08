from .register import register_customer
from .check_eligibility import check_eligibility
from .create_loan import create_loan
from .view_loan import view_loan
from .view_loans_by_customer import view_loans_by_customer

__all__ = [
    'register_customer',
    'check_eligibility',
    'create_loan',
    'view_loan',
    'view_loans_by_customer',
] 