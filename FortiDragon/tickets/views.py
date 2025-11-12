from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views import View, generic
from .forms import TicketCreateForm, AssignTicketForm
from .models import Ticket

User = get_user_model()

# Registration view
def register(request):
    """Allow a new user to create an account."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")  # from django.contrib.auth.urls
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

# Ticket dashboard view
class DashboardView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/dashboard.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.select_related("created_by", "assigned_to").order_by("-created_at")

# Create Ticket view
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketCreateForm
    template_name = "tickets/ticket_form.html"
    success_url = reverse_lazy("tickets:dashboard")  # after submit, go to "my tickets"

    def form_valid(self, form):
        # attach the currently logged-in user as the creator
        ticket = form.save(commit=False)
        ticket.created_by = self.request.user
        ticket.save()
        messages.success(self.request, "Your ticket has been submitted and is pending review.")
        return super().form_valid(form)

# My tickets view
class MyTicketsView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user).order_by("-created_at")

# All tickets view
class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.select_related("created_by", "assigned_to").order_by("-created_at")

# Ticket detail view
class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

# Pending ticket view
# class StaffRequiredMixin(UserPassesTestMixin):
#     """Mixin to restrict view to staff or users with specific perms."""
#
#     def test_func(self):
#         user = self.request.user
#         return user.is_staff or user.has_perm("tickets.can_approve_ticket")


class PendingTicketsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/tickets_pending.html"
    context_object_name = "tickets"
    permission_required = "tickets.can_approve_ticket"

    def get_queryset(self):
        return Ticket.objects.filter(status=Ticket.Status.PENDING).select_related("created_by", "assigned_to").order_by("created_at")

# Approve ticket view
# @login_required
# @permission_required("tickets.can_approve_ticket", raise_exception=True)
# def approve_ticket(request, pk):
#     ticket = get_object_or_404(Ticket, pk=pk)
#
#     if ticket.status != Ticket.Status.PENDING:
#         messages.info(request, "This ticket is not in pending status.")
#         return redirect("tickets:detail", pk=pk)
#
#     ticket.status = Ticket.Status.APPROVED
#     ticket.approved_by = request.user
#     ticket.save(update_fields=["status", "approved_by"])
#
#     messages.success(request, "Ticket approved.")
#     return redirect("tickets:detail", pk=pk)

class ApproveTicketView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "tickets.can_approve_ticket"
    raise_exception = True

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)

        if ticket.status != Ticket.Status.PENDING:
            messages.info(request, "This ticket is not in pending status.")
            return redirect("tickets:detail", pk=pk)

        ticket.status = Ticket.Status.APPROVED
        ticket.approved_by = request.user
        ticket.save(update_fields=["status", "approved_by"])

        messages.success(request, "Ticket approved.")
        return redirect("tickets:detail", pk=pk)


# Assign ticket view
# @login_required
# @permission_required("tickets.can_assign_ticket", raise_exception=True)
# def assign_ticket(request, pk):
#     ticket = get_object_or_404(Ticket, pk=pk)
#
#     if request.method == "POST":
#         form = TicketAssignForm(request.POST, instance=ticket)
#         if form.is_valid():
#             ticket = form.save(commit=False)
#             ticket.status = Ticket.Status.ASSIGNED
#             ticket.save(update_fields=["assigned_to", "status"])
#             messages.success(request, "Ticket assigned.")
#             return redirect("tickets:detail", pk=pk)
#     else:
#         form = TicketAssignForm(instance=ticket)
#
#     # Filter assigned_to choices to staff only:
#     form.fields["assigned_to"].queryset = User.objects.filter(is_staff=True)
#
#     return render(request, "tickets/ticket_form.html", {"form": form, "assigning": True})

class AssignTicketToMeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "tickets.can_assign_ticket"
    raise_exception = True

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)

        if ticket.status not in [Ticket.Status.PENDING, Ticket.Status.APPROVED]:
            messages.info(request, "This ticket cannot be assigned from its current status.")
            return redirect("tickets:detail", pk=pk)

        ticket.assigned_to = request.user
        ticket.status = Ticket.Status.ASSIGNED
        ticket.save(update_fields=["assigned_to", "status"])

        messages.success(request, "Ticket assigned to you.")
        return redirect("tickets:detail", pk=pk)

class AssignTicketView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Ticket
    fields = ["assigned_to"]
    context_object_name = "ticket"
    # form_class = AssignTicketForm
    template_name = "tickets/assign_ticket.html"
    permission_required = "tickets.can_assign_ticket"
    raise_exception = True

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the dropdown: only staff users (admins/techs)
        form.fields["assigned_to"].queryset = User.objects.filter(is_staff=True).order_by("username")
        return form

    def form_valid(self, form):
        ticket = form.instance

        # If we selected someone, mark as ASSIGNED
        if ticket.assigned_to:
            ticket.status = Ticket.Status.ASSIGNED
        ticket.save(update_fields=["assigned_to", "status"])

        messages.success(
            self.request,
            f"Ticket #{ticket.pk} assigned to {ticket.assigned_to}."
        )
        return super().form_valid(form)

    def get_success_url(self):
        # After assigning, go back to the ticket detail page
        return reverse_lazy("tickets:detail", kwargs={"pk": self.object.pk})
