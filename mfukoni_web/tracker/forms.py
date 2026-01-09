"""
Forms for Mfukoni tracker application.
"""

from django import forms
from .db_manager import get_db


class TransactionForm(forms.Form):
    """Form for adding/editing transactions."""
    
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    trans_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Type",
        required=True,
        initial='income'  # Set default value
    )
    category_id = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Category",
        required=True
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Amount (KES)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
    )
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction description'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db = get_db()
        categories = db.get_all_categories()
        
        # Group categories by type
        income_cats = [(str(c['id']), c['name']) for c in categories if c.get('type') == 'income']
        expense_cats = [(str(c['id']), c['name']) for c in categories if c.get('type') == 'expense']
        
        # Set initial category choices (will be updated by JavaScript)
        # Use all categories initially, JavaScript will filter based on type
        all_cats = [('', 'Select a category...')] + income_cats + expense_cats
        self.fields['category_id'].choices = all_cats


class FilterForm(forms.Form):
    """Form for filtering transactions."""
    
    category_id = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Category"
    )
    trans_type = forms.ChoiceField(
        choices=[('', 'All'), ('income', 'Income'), ('expense', 'Expense')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Type"
    )
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search...', 'class': 'form-control'}),
        label="Search"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db = get_db()
        categories = db.get_all_categories()
        # Convert IDs to strings for ChoiceField compatibility
        choices = [('', 'All Categories')] + [(str(c['id']), c['name']) for c in categories]
        self.fields['category_id'].widget.choices = choices


class CategoryForm(forms.Form):
    """Form for adding categories."""
    
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
        label="Category Name"
    )
    cat_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Type"
    )


# SQLConsoleForm removed - CRUD operations automatically execute SQL queries


class DateRangeForm(forms.Form):
    """Form for date range filtering - used to filter transaction list, not part of transaction itself."""
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'From date'}),
        required=False,
        label="Date From",
        help_text="Filter transactions from this date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'To date'}),
        required=False,
        label="Date To",
        help_text="Filter transactions until this date"
    )


class BudgetForm(forms.Form):
    """Form for setting budgets."""
    
    category_id = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Category"
    )
    monthly_limit = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        label="Monthly Limit (KES)"
    )
    month = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'form-control'}),
        label="Month"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db = get_db()
        categories = db.get_all_categories(cat_type='expense')
        # Convert IDs to strings for ChoiceField
        self.fields['category_id'].choices = [(str(c['id']), c['name']) for c in categories]
