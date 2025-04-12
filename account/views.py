# views.py login page
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = "نام کاربری یا رمز عبور اشتباه است."
    return render(request, 'login.html', {'error': error})

# --------------------------------------------
from django.db.models import Sum
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, Transaction, Inventory, Loan, Account

def home(request):
    return render(request, 'index.html')

def needy_menu(request):
    return render(request, 'needy/menu.html')

def org_menu(request):
    return render(request, 'organization/menu.html')

class NeedyDonationAmountView(APIView):
    def get(self, request):
        total_needy_donations = Inventory.objects.filter(inventory_type=Inventory.InventoryType.NEEDY_DONATION).aggregate(total_amount=Sum('amount'))['total_amount']
        if total_needy_donations is None:
            total_needy_donations = 0  # Return 0 if no needy donations are
        return Response({'total_needy_donations': total_needy_donations}, status=status.HTTP_200_OK)

class OrgDonationAmountView(APIView):
    def get(self, request):
        total_org_donations = Inventory.objects.filter(inventory_type=Inventory.InventoryType.ORG_FUNDS).aggregate(total_amount=Sum('amount'))['total_amount']
        if total_org_donations is None:
            total_org_donations = 0  # Return 0 if no org donations are
        return Response({'total_org_donations': total_org_donations}, status=status.HTTP_200_OK)
