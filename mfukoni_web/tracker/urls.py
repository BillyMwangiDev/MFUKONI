"""
URL configuration for tracker app.
"""

from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transactions/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/<int:budget_id>/delete/', views.delete_budget, name='delete_budget'),
    path('reports/', views.reports, name='reports'),
    path('export/transactions/', views.export_transactions, name='export_transactions'),
    path('export/reports/', views.export_reports, name='export_reports'),
    path('api/categories/', views.get_categories_ajax, name='get_categories_ajax'),
]
