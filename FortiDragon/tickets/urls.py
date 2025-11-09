from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("new/", views.TicketCreateView.as_view(), name="create"),
    path("mine/", views.MyTicketsView.as_view(), name="mine"),
    path("list/", views.TicketListView.as_view(), name="list"),
    path("pending/", views.PendingTicketsView.as_view(), name="pending"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="detail"),
    path("<int:pk>/approve/", views.approve_ticket, name="approve"),
    path("<int:pk>/assign/", views.assign_ticket, name="assign"),
]