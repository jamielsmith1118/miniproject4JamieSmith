from django import forms
from .models import Ticket

class TicketCreateForm(forms.ModelForm):
    """Form for regular users to submit a new ticket."""

    class Meta:
        model = Ticket
        # Fields the user fills in
        fields = ["title", "description", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }

class TicketAssignForm(forms.ModelForm):
    """Form for staff/admin to assign a ticket to a user."""

    class Meta:
        model = Ticket
        fields = ["assigned_to"]