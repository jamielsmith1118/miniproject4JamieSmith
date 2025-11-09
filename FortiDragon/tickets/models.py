from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Create your models here.

# Create Ticket model
class Ticket(models.Model):

    # Create status model
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        ASSIGNED = "assigned", "Assigned"
        CLOSED = "closed", "Closed"

    # Create Priority model
    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        URGENT = 4, "Urgent"

    # Ticket fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # User information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_created")
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_assigned"
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_approved"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.pk} {self.title} [{self.get_status_display()}]"

    # Add permissions to approve and assign tickets
    class Meta:
        permissions = [
            ("can_approve_ticket", "Can approve tickets"),
            ("can_assign_ticket", "Can assign tickets"),
        ]