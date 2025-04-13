from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, national_id, phone_number, password=None, **extra_fields):
        if not national_id:
            raise ValueError("The National ID must be set")
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        user = self.model(
            national_id=national_id, phone_number=phone_number, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, national_id, phone_number, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(national_id, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    fathers_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15)
    birthday = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "national_id"

    def __str__(self):
        return f"{self.name} {self.last_name} ({self.national_id})"


class Account(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="acc_user"
    )
    signature = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="acc_signature"
    )  # حق امضا
    account_number = models.CharField(max_length=200, unique=True)
    balance = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(null=True, blank=True)
    system_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"Account {self.account_number} for {self.user.name} {self.user.last_name}"
        )


class Inventory(models.Model):
    class InventoryType(models.TextChoices):
        MOSQUE_DONATION = "MOSQUE_DONATION", "Donation for Mosque"  # کمک به مسجد
        NEEDY_DONATION = "NEEDY_DONATION", "Donation for Needy"  # کمک به فقرا
        ORG_FUNDS = "ORG_FUNDS", "Organization Funds"  # صندوق مسجد
        LOAN_FUNDS = "LOAN_FUNDS", "Loan Funds"  # صندوق های وام

    inventory_type = models.CharField(max_length=20, choices=InventoryType.choices)
    amount = models.BigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def deposit(self, amount, account=None, description=""):
        self.amount += amount
        self.save()

        if not account:
            account = None

        Transaction.objects.create(
            account=account,
            amount=amount,
            type=Transaction.TransactionType.DEPOSIT,
            description=description,
        )

    def withdraw(self, amount, account=None, description=""):
        if self.amount >= amount:
            self.amount -= amount
            self.save()

            if not account:
                account = None

            Transaction.objects.create(
                account=account,
                amount=amount,
                type=Transaction.TransactionType.WITHDRAW,
                description=description,
            )
        else:
            raise ValueError("Insufficient funds")

    def __str__(self):
        return f"Inventory {self.inventory_type} - Amount: {self.amount}"


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"  # واریز
        WITHDRAW = "WITHDRAW", "Withdraw"  # برداشت
        LOAN_DISBURSE = "LOAN_DISBURSE", "Loan Disbursement"  # پرداخت وام
        LOAN_REPAYMENT = "LOAN_REPAYMENT", "Loan Repayment"  # بازپرداخت وام
        DONATION = "DONATION", "Donation"  # اهدا / کمک مالی
        FEE = "FEE", "Fee"  # هزینه / کارمزد

    account = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="trans_account",
    )
    amount = models.BigIntegerField()
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.type} of {self.amount} for account {self.account.account_number}"


class Loan(models.Model):
    borrower = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, related_name="loan_borrower"
    )  # حساب وام‌گیرنده
    guarantor = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="loan_guarantor",
    )  # حساب ضامن وام
    guarantor_info = models.TextField(blank=True, null=True)
    amount = models.BigIntegerField()  # مبلغ کل وام
    total_paid_amount = models.BigIntegerField(default=0)
    blocked_from_guarantor = models.BooleanField(
        default=False
    )  # آیا این مبلغ از حساب ضامن مسدود شده یا نه
    monthly_installment = models.BigIntegerField()  # مبلغ هر قسط ماهانه
    total_months = models.PositiveIntegerField(default=10)  # تعداد کل ماه‌های بازپرداخت
    paid_months = models.PositiveIntegerField(default=0)  # تعداد ماه‌هایی که پرداخت شده
    fees = models.BigIntegerField(default=0)  # هزینه‌ها یا کارمزدهای وام
    disbursed_amount = models.BigIntegerField()  # مبلغ پرداخت‌شده به وام‌گیرنده
    is_active = models.BooleanField(default=True)  # وضعیت فعال بودن وام
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد وام
    detail = models.TextField(blank=True, null=True)
    system_message = models.TextField(null=True, blank=True)

    def remaining_balance(self):
        return (self.amount // self.total_months) * (
            self.total_months - self.paid_months
        )  # محاسبه مانده بدهی

    def __str__(self):
        return f"Loan for {self.borrower.account_number} - Amount: {self.amount} (Paid: {self.total_paid_amount})"
