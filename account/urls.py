from django.urls import path
from django.views.generic import TemplateView
from .views import login_view, NeedyDonationAmountView, home, needy_menu, org_menu, OrgDonationAmountView

urlpatterns = [
    path('', home, name='home'),
    path('needy', needy_menu, name='needy_menu'),
    path('organization', org_menu, name='org_menu'),
    path('api/needy-donation-amount/', NeedyDonationAmountView.as_view(), name='needy-donation-amount'),
    path('api/org-donation-amount/', OrgDonationAmountView.as_view(), name='org-donation-amount'),
    path('login/', login_view, name='login'),

]