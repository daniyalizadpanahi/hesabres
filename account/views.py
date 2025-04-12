# # views.py
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# # from .models import Loan, Fund
# from django.contrib.auth.models import User
# from datetime import date

# @api_view(['POST'])
# def apply_for_loan(request):
#     user = User.objects.get(id=request.data['user_id'])
#     amount = request.data['amount']
    
#     # فرض بر اینکه کاربر تایید شده است
#     if not user.userprofile.is_verified:
#         return Response({"error": "User not verified"}, status=400)

#     loan = Loan.objects.create(user=user, amount=amount, issued_date=date.today())
#     loan.save()

#     # آپدیت موجودی صندوق
#     fund = Fund.objects.first()
#     fund.update_balance()

#     return Response({"message": "Loan applied successfully!", "loan_id": loan.id}, status=201)

# @api_view(['GET'])
# def fund_summary(request):
#     fund = Fund.objects.first()
#     return Response({
#         "total_balance": fund.total_balance,
#         "total_debt": fund.total_debt,
#         "net_balance": fund.total_balance - fund.total_debt
#     })


# # views.py login page
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect

# def login_view(request):
#     error = None
#     if request.method == 'POST':
#         user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#         if user:
#             login(request, user)
#             return redirect('home')
#         else:
#             error = "نام کاربری یا رمز عبور اشتباه است."
#     return render(request, 'login.html', {'error': error})

