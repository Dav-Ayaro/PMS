from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Complaint
from users.models import CustomUser
from onboarding.models import Parent
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

def is_receptionist_or_admin(user):
    return user.role in ['receptionist', 'admin']

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_receptionist_or_admin)
def submit_complaint(request):
    if request.method == 'POST':
        parent_id = request.POST['parent']
        description = request.POST['description']
        parent = Parent.objects.get(id=parent_id)
        Complaint.objects.create(
            parent=parent,
            description=description
        )
        return redirect('dashboard')
    parents = Parent.objects.all()
    return render(request, 'complaints.html', {'parents': parents})

@login_required
@user_passes_test(is_admin)
def assign_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        assigned_to_id = request.POST['assigned_to']
        complaint.assigned_to = CustomUser.objects.get(id=assigned_to_id)
        complaint.status = 'in_progress'
        complaint.save()
        return redirect('dashboard')
    users = CustomUser.objects.all()
    return render(request, 'complaints.html', {'complaint': complaint, 'users': users})

@login_required
def resolve_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.user == complaint.assigned_to or request.user.role == 'admin':
        complaint.status = 'resolved'
        complaint.resolved_at = timezone.now()
        complaint.save()
        send_mail(
            'Complaint Resolved',
            f'Your complaint has been resolved: {complaint.description}',
            settings.EMAIL_HOST_USER,
            [complaint.parent.email],
            fail_silently=False,
        )
    return redirect('dashboard')