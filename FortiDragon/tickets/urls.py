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
    path("<int:pk>/approve/", views.ApproveTicketView.as_view(), name="approve"),
    path("<int:pk>/assign-to-me/", views.AssignTicketToMeView.as_view(), name="assign_to_me"),
    path("<int:pk>/assign/", views.AssignTicketView.as_view(), name="assign"),
]