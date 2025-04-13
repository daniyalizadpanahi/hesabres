from django.urls import path
from .views import (
    login_view,
    NeedyDonationAmountView,
    needy_payment,
    home,
    needy_menu,
    org_payment,
    org_menu,
    OrgDonationAmountView,
    DepositWithdrawAPI,
)

urlpatterns = [
    path("", home, name="home"),
    path("needy", needy_menu, name="needy_menu"),
    path("needy/payment", needy_payment, name="needy_payment"),
    path("organization", org_menu, name="org_menu"),
    path("organization/payment", org_payment, name="org_payment"),
    path(
        "api/needy-donation-amount/",
        NeedyDonationAmountView.as_view(),
        name="needy-donation-amount",
    ),
    path(
        "api/org-donation-amount/",
        OrgDonationAmountView.as_view(),
        name="org-donation-amount",
    ),
    path(
        "api/inventory/<str:action>/",
        DepositWithdrawAPI.as_view(),
        name="deposit_withdraw",
    ),
    path("login/", login_view, name="login"),
]
