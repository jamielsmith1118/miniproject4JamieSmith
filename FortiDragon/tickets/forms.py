from django import forms
from django.contrib.auth import get_user_model
from .models import Ticket

User = get_user_model()

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

# class AssignTicketForm(forms.ModelForm):
#     class Meta:
#         model = Ticket
#         fields = ["assigned_to"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Only allow assigning to staff users (admins/techs)
#         self.fields["assigned_to"].queryset = (
#            # User.objects.filter(groups__name__in=["Admins", "Technicians"]).order_by("username").distinct()
#             User.objects.filter(is_staff=True).order_by("username").distinct()
#            #User.objects.all()
#         )
#         self.fields["assigned_to"].label = "Assign to"
#         self.fields["assigned_to"].widget = forms.Select(
#             attrs={"class": "form-select"}
#         )

from django import forms
from .models import Ticket


class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["assigned_to"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ask Django: what model does assigned_to point to?
        user_model = Ticket._meta.get_field("assigned_to").remote_field.model

        # For now, show ALL users of that model so we can confirm it works
        self.fields["assigned_to"].queryset = (
            user_model.objects.all().order_by("username")
        )

        self.fields["assigned_to"].label = "Assign to"
        self.fields["assigned_to"].widget = forms.Select(
            attrs={"class": "form-select"}
        )