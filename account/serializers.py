from rest_framework import serializers
from .models import Account, CustomUser, Image, Inventory, Loan, Transaction


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["inventory_type", "amount", "prev_amount"]


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ["account", "amount", "type", "description", "created_at"]


class CreateInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["inventory_type", "amount", "updated_at"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "amount",
            "type",
            "created_at",
            "description",
        ]


class TotallInventorySerializer(serializers.Serializer):
    MOSQUE_DONATION_amount = serializers.IntegerField()
    NEEDY_DONATION_amount = serializers.IntegerField()
    ORG_FUNDS_amount = serializers.IntegerField()
    LOAN_FUNDS_amount = serializers.IntegerField()

    def to_representation(self, instance):
        mosque_donation = Inventory.objects.filter(
            inventory_type="MOSQUE_DONATION"
        ).first()
        needy_donation = Inventory.objects.filter(
            inventory_type="NEEDY_DONATION"
        ).first()
        org_funds = Inventory.objects.filter(inventory_type="ORG_FUNDS").first()
        loan_funds = Inventory.objects.filter(inventory_type="LOAN_FUNDS").first()

        return {
            "MOSQUE_DONATION_amount": mosque_donation.amount if mosque_donation else 0,
            "NEEDY_DONATION_amount": needy_donation.amount if needy_donation else 0,
            "ORG_FUNDS_amount": org_funds.amount if org_funds else 0,
            "LOAN_FUNDS_amount": loan_funds.amount if loan_funds else 0,
        }


class AccountListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")
    last_name = serializers.CharField(source="user.last_name")
    national_id = serializers.CharField(source="user.national_id")

    class Meta:
        model = Account
        fields = [
            "account_number",
            "name",
            "last_name",
            "created_at",
            "national_id",
            "balance",
            "is_active",
        ]


class AccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "last_name",
            "fathers_name",
            "national_id",
            "phone_number",
            "birthday",
            "address",
            "postal_code",
            "created_at",
            "detail",
        ]


class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "last_name", "national_id"]

class AccountDetailSerializer(serializers.ModelSerializer):
    user = AccountUserSerializer()
    transactions = AccountTransactionSerializer(
        source="trans_account", many=True, read_only=True
    )
    loans = LoanSerializer(source="loan_borrower", many=True, read_only=True)
    signature = CustomUserSerializer()

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "signature",
            "account_number",
            "system_message",
            "detail",
            "created_at",
            "balance",
            "is_active",
            "transactions",
            "loans",
        ]
class ImageSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source="image")
    class Meta:
        model = Image
        fields = ['id', 'created_at', 'url']
