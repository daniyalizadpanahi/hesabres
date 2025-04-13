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
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, Transaction, Inventory, Loan, Account
from .serializers import CreateInventorySerializer


def home(request):
    return render(request, "index.html")


def needy_menu(request):
    return render(request, "needy/menu.html")


def org_menu(request):
    return render(request, "organization/menu.html")


def needy_payment(request):
    return render(request, "needy/payment.html")


def org_payment(request):
    return render(request, "organization/payment.html")


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
        account_id = request.data.get("account", 1)
        description = request.data.get("description", "")

        amount = int("".join(amount.split(",")))

        inventory = get_object_or_404(Inventory, inventory_type=inventory_type)

        if account_id:
            account = get_object_or_404(Account, id=account_id)

        if action == "deposit":
            inventory.deposit(amount, account, description)
            return Response(
                {"status": "Deposit successful"}, status=status.HTTP_201_CREATED
            )

        elif action == "withdraw":
            try:
                inventory.withdraw(amount, account, description)
                return Response(
                    {"status": "Withdraw successful"}, status=status.HTTP_200_OK
                )
            except ValueError:
                return Response(
                    {"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
