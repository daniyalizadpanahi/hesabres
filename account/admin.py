from django.contrib import admin
from .models import CustomUser, Account, Inventory, Transaction, Loan


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "national_id",
        "name",
        "last_name",
        "phone_number",
        "is_active",
        "is_staff",
        "created_at",
    )
    search_fields = ("national_id", "phone_number", "name")
    list_filter = ("is_active", "is_staff")


class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "user", "balance", "is_active", "created_at")
    search_fields = ("account_number", "user__national_id")
    list_filter = ("is_active",)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("inventory_type", "amount", "updated_at")
    list_filter = ("inventory_type",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "amount", "type", "created_at", "description")
    search_fields = ("account__account_number", "type")
    list_filter = ("type",)


class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "borrower",
        "guarantor",
        "amount",
        "monthly_installment",
        "total_months",
        "paid_months",
        "is_active",
        "created_at",
    )
    search_fields = (
        "borrower__account_number",
        "guarantor__account_number",
        "guarantor_info",
    )
    list_filter = ("is_active",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Loan, LoanAdmin)
