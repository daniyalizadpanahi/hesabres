from django.urls import path
from .views import (
    AccountImagesAPIView,
    LoanItemAPIView,
    TransactionDeleteAPIView,
    account,
    account_detail,
    account_image_upload,
    loan_item,
    login_view,
    home,
    totall_balance,
    cash_box_menu,
    loan_menu,
    needy_payment,
    needy_menu,
    needy_report,
    org_payment,
    org_menu,
    org_report,
    account_new,
    loan_request,
    loan_list,
    LoanListAPIView,
    AccountListView,
    NeedyDonationAmountView,
    OrgDonationAmountView,
    DepositWithdrawAPI,
    ReportAPIView,
    InventoryViewSet,
    AccountDetailView,
    UserView,
    # AccountImageUploadView,
)

urlpatterns = [
    path("", home, name="home"),
    path("totall-balance", totall_balance, name="totall-balance"),
    path("loan", loan_menu, name="loan"),
    path("loan/<int:id>", loan_item, name="loan-item-page"),
    path("loan/new", loan_request, name="loan-request"),
    path("loan/list", loan_list, name="loan-list"),
    path("cash_box", cash_box_menu, name="cash-box"),
    path("needy", needy_menu, name="needy-menu"),
    path("needy/report", needy_report, name="needy-report"),
    path("needy/payment", needy_payment, name="needy-payment"),
    path("organization", org_menu, name="org-menu"),
    path("organization/report", org_report, name="org-report"),
    path("organization/payment", org_payment, name="org-payment"),
    path("account", account, name="account-menu"),
    path(
        "account/<str:account_number>/image",
        account_image_upload,
        name="account-image-gallery",
    ),
    path("account/new", account_new, name="new-account"),
    path("account/<str:id>", account_detail, name="account-info"),
    path("api/users", UserView.as_view(), name="users"),
    path("api/loan/", LoanListAPIView.as_view(), name="loan-list"),
    path("api/loan/<int:id>", LoanItemAPIView.as_view(), name="loan-item"),
    path(
        "api/account/<str:national_id>",
        AccountDetailView.as_view(),
        name="account-detail",
    ),
    path("api/account", AccountListView.as_view(), name="account"),
    path(
        "api/account/<str:account_number>/image",
        AccountImagesAPIView.as_view(),
        name="account-images",
    ),
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
        name="deposit-withdraw",
    ),
    path(
        "api/report/<str:action>/",
        ReportAPIView.as_view(),
        name="report",
    ),
    path("api/inventory", InventoryViewSet.as_view({"get": "list"}), name="inventory"),
    path(
        "api/transaction/delete/<int:pk>/",
        TransactionDeleteAPIView.as_view(),
        name="transaction-delete",
    ),
    path("login/", login_view, name="login"),
]
