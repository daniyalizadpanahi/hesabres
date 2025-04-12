from django import forms
from .models import Loan, Account


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            'borrower',
            'amount',
            'fees',
            'guarantor_account',
            'guarantor_name',
            'paid_by',
            'detail',
        ]

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        fees = cleaned_data.get('fees')
        borrower = cleaned_data.get('borrower')
        paid_by = cleaned_data.get('paid_by')

        # بررسی سقف وام
        if amount > 2_000_000 and not paid_by:
            raise forms.ValidationError("برای وام بیشتر از ۲ میلیون، باید حساب پرداخت‌کننده مشخص شود.")

        return cleaned_data

    def save(self, commit=True):
        loan = super().save(commit=False)

        # محاسبه مبلغ پرداخت‌شده بعد از کسر کارمزد
        loan.disbursed_amount = loan.amount - loan.fees

        # محاسبه مبلغ هر قسط (ده ماهه)
        loan.monthly_installment = loan.amount // 10
        loan.total_months = 10

        # آیا وام از سقف بیشتر بوده؟
        loan.is_above_limit = loan.amount > 2_000_000

        # در صورتی که مبلغ از حساب کسی پرداخت شده
        if loan.paid_by:
            loan.blocked_from_guarantor = True

        if commit:
            loan.save()

        return loan
