# views.py login page
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    error = None
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user:
            login(request, user)
            return redirect("home")
        else:
            error = "نام کاربری یا رمز عبور اشتباه است."
    return render(request, "login.html", {"error": error})


# --------------------------------------------
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from .models import CustomUser, Image, Transaction, Inventory, Loan, Account
from .serializers import (
    ImageSerializer,
    LoanSerializer,
    TransactionSerializer,
    AccountListSerializer,
    AccountDetailSerializer,
    CustomUserSerializer,
    # AccountImageUploadSerializer,
)


def home(request):
    return render(request, "index.html")


def needy_menu(request):
    return render(request, "needy/menu.html")


def needy_payment(request):
    return render(request, "needy/payment.html")


def needy_report(request):
    return render(request, "needy/report.html")


def org_menu(request):
    return render(request, "organization/menu.html")


def org_payment(request):
    return render(request, "organization/payment.html")


def org_report(request):
    return render(request, "organization/report.html")


def totall_balance(request):
    return render(request, "totall_balance/balance.html")


def cash_box_menu(request):
    return render(request, "cash_box/menu.html")


def loan_menu(request):
    return render(request, "loan/menu.html")


def account(request):
    return render(request, "cash_box/account.html")


def account_detail(request, id):
    return render(request, "cash_box/account_detail.html", {"national_code": id})


def account_image_upload(request, account_number):
    return render(request, "cash_box/account-document-image.html",  {"account_number": account_number})


def account_new(request):
    return render(request, "cash_box/new.html")


def loan_request(request):
    return render(request, "loan/request.html")


def loan_list(request):
    return render(request, "loan/active.html")

class NeedyDonationAmountView(APIView):
    def get(self, request):
        total_needy_donations = Inventory.objects.filter(
            inventory_type=Inventory.InventoryType.NEEDY_DONATION
        ).aggregate(total_amount=Sum("amount"))["total_amount"]
        if total_needy_donations is None:
            total_needy_donations = 0
        return Response(
            {"total_needy_donations": total_needy_donations}, status=status.HTTP_200_OK
        )


class OrgDonationAmountView(APIView):
    def get(self, request):
        total_org_donations = Inventory.objects.filter(
            inventory_type=Inventory.InventoryType.MOSQUE_DONATION
        ).aggregate(total_amount=Sum("amount"))["total_amount"]
        if total_org_donations is None:
            total_org_donations = 0
        return Response(
            {"total_org_donations": total_org_donations}, status=status.HTTP_200_OK
        )


class DepositWithdrawAPI(APIView):
    def post(self, request, action):
        inventory_type = request.data.get("inventory_type")
        amount = request.data.get("amount")
        account_id = request.data.get("account", None)
        description = request.data.get("description", "")
        type = request.data.get("type", None)

        amount = int("".join(amount.split(",")))

        inventory = get_object_or_404(Inventory, inventory_type=inventory_type)
            
        if action == "deposit":
            inventory.deposit(amount, type, account_id, description)
            return Response(
                {"status": "Deposit successful"}, status=status.HTTP_201_CREATED
            )

        elif action == "withdraw":
            try:
                inventory.withdraw(amount, type, account_id, description)
                return Response(
                    {"status": "Withdraw successful"}, status=status.HTTP_200_OK
                )
            except ValueError:
                return Response(
                    {"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class ReportAPIView(APIView):
    def get(self, request, action):
        if action == "donation":
            reports = Transaction.objects.filter(mosque_donation=True)
        elif action == "needy":
            reports = Transaction.objects.filter(needy_donation=True)
        elif action == "loan":
            reports = Transaction.objects.filter(loan=True)
        else:
            reports = []
        serialized_reports = TransactionSerializer(reports, many=True)

        return Response({"reports": serialized_reports.data}, status=status.HTTP_200_OK)


class InventoryViewSet(viewsets.ViewSet):
    def list(self, request):
        mosque_donation = Inventory.objects.filter(
            inventory_type="MOSQUE_DONATION"
        ).first()
        needy_donation = Inventory.objects.filter(
            inventory_type="NEEDY_DONATION"
        ).first()
        org_funds = Inventory.objects.filter(inventory_type="ORG_FUNDS").first()
        loan_funds = Inventory.objects.filter(inventory_type="LOAN_FUNDS").first()

        data = {
            "mosque_donation_amount": mosque_donation.amount if mosque_donation else 0,
            "needy_donation_amount": needy_donation.amount if needy_donation else 0,
            "org_funds_amount": org_funds.amount if org_funds else 0,
            "loan_funds_amount": loan_funds.amount if loan_funds else 0,
        }

        return Response(data)


class AccountListView(APIView):
    def get(self, request):
        accounts = Account.objects.select_related("user").all()
        serializer = AccountListSerializer(accounts, many=True)
        return Response(serializer.data)


class AccountDetailView(APIView):
    def get(self, request, national_id):
        account = (
            Account.objects.select_related("user")
            .prefetch_related("loan_borrower", "trans_account")
            .filter(user__national_id=national_id)
            .first()
        )
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data)

    def put(self, request, national_id):
        account = (
            Account.objects.select_related("user")
            .filter(user__national_id=national_id)
            .first()
        )
        if not account:
            return Response({"error": "Account not found"}, status=404)

        user_data = request.data.get("user", {})
        new_national_id = user_data.get("national_id")

        if new_national_id and new_national_id != account.user.national_id:
            if CustomUser.objects.filter(national_id=new_national_id).exists():
                return Response({"error": "کد ملی تکراری است."}, status=400)

        for field in [
            "name",
            "last_name",
            "fathers_name",
            "national_id",
            "phone_number",
            "birthday",
            "address",
            "postal_code",
            "detail",
        ]:
            if field in user_data:
                setattr(account.user, field, user_data[field])
        account.user.save()

        for field in ["signature", "account_number", "detail"]:
            if field in request.data:
                if field == "signature":
                    signature = get_object_or_404(CustomUser, pk=request.data.get("signature"))
                    setattr(account, field, signature)
                    continue
                setattr(account, field, request.data[field])
        account.save()

        serializer = AccountDetailSerializer(account)
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request):
        users = CustomUser.objects.filter(is_active=True)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_data = request.data.get("user", {})
        national_id = user_data.get("national_id")
        if CustomUser.objects.filter(national_id=national_id).exists():
            return Response({"error": "کد ملی تکراری است."}, status=400)

        try:
            with transaction.atomic():
                user = CustomUser.objects.create(
                    name=user_data.get("name"),
                    last_name=user_data.get("last_name"),
                    fathers_name=user_data.get("father_name"),
                    national_id=national_id,
                    phone_number=user_data.get("phone"),
                    birthday=user_data.get("birthdate"),
                    address=user_data.get("address"),
                    postal_code=user_data.get("postal_code"),
                    detail=user_data.get("personal_details"),
                )
                signature = CustomUser.objects.all().first()
                account = Account.objects.create(
                    user=user,
                    signature=signature,
                    account_number=user_data.get("account_number"),
                    detail=user_data.get("account_details"),
                    system_message=user_data.get("system_message"),
                )
                balance = int(user_data.get("balance"))
                inventory_type = Inventory.InventoryType.ORG_FUNDS
                inventory = get_object_or_404(Inventory, inventory_type=inventory_type)
                inventory.deposit(balance, Transaction.TransactionType.DEPOSIT, account.pk, "موجودی اولیه")
                
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=201)

class LoanListAPIView(APIView):
    def get(self, request):
        loans = Loan.objects.all().order_by('-created_at')
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    
class AccountImagesAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)

            images = Image.objects.filter(field_id=account.id, reason='account_info')

            serializer = ImageSerializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)

            if 'image' in request.FILES:
                images = request.FILES.getlist('image')
                model_name = "Account"
                reason = "account_info"
                field_id = account.id

                image_instances = []
                for img in images:
                    image_instance = Image.objects.create(
                        model_name=model_name,
                        reason=reason,
                        field_id=field_id,
                        image=img
                    )
                    image_instances.append(image_instance)

                serializer = ImageSerializer(image_instances, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            image_ids = request.data.get("image_ids", [])

            if image_ids:
                images_to_delete = Image.objects.filter(pk__in=image_ids, field_id=account.id, reason='account_info')
                deleted_count = images_to_delete.count()
                images_to_delete.delete()

                return Response({"detail": f"{deleted_count} image(s) deleted."}, status=status.HTTP_200_OK)
            
            return Response({"detail": "No action provided."}, status=status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)

class TransactionDeleteAPIView(APIView):
    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)

        if transaction.mosque_donation:
            inventory_type = Inventory.InventoryType.MOSQUE_DONATION
        elif transaction.needy_donation:
            inventory_type = Inventory.InventoryType.NEEDY_DONATION
        elif transaction.loan:
            inventory_type = Inventory.InventoryType.LOAN_FUNDS
        elif transaction.account:
            account = transaction.account
            if transaction.type == "DEPOSIT":
                account.balance -= transaction.amount
            elif transaction.type == "WITHDRAW":
                account.balance += transaction.amount
            account.save()
            transaction.delete()
            return Response({"message": "Transaction deleted and account updated."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Transaction has no valid category."}, status=status.HTTP_400_BAD_REQUEST)

        inventory = get_object_or_404(Inventory, inventory_type=inventory_type)

        if transaction.type == "DEPOSIT":
            inventory.amount -= transaction.amount
        elif transaction.type == "WITHDRAW":
            inventory.amount += transaction.amount

        inventory.save()
        transaction.delete()

        return Response({"message": "Transaction deleted and inventory updated."}, status=status.HTTP_200_OK)