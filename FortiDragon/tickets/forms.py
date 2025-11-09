from django import forms
from .models import Ticket

class TicketCreateForm(forms.ModelForm):
    """Form for regular users to submit a new ticket."""

    class Meta:
        model = Ticket
        # Users only fill these out; the rest is handled in code
        fields = ["title", "description", "priority"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

class TicketAssignForm(forms.ModelForm):
    """Form for staff/admin to assign a ticket to a user."""

    class Meta:
        model = Ticket
        fields = ["assigned_to"]