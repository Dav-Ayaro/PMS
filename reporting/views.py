from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Report
from communication.models import Message
from fees.models import Payment
from complaints.models import Complaint
from django.utils import timezone

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def generate_report(request):
    report_type = request.GET.get('report_type', 'engagement')
    if report_type == 'engagement':
        messages = Message.objects.filter(sent_at__gte=timezone.now() - timezone.timedelta(days=7))
        data = {'messages_sent': messages.count(), 'by_type': {m.message_type: messages.filter(message_type=m.message_type).count() for m in messages}}
    elif report_type == 'payment':
        payments = Payment.objects.filter(paid_at__gte=timezone.now() - timezone.timedelta(days=30))
        data = {'total_payments': payments.count(), 'total_amount': sum(p.amount for p in payments)}
    elif report_type == 'complaint':
        complaints = Complaint.objects.filter(submitted_at__gte=timezone.now() - timezone.timedelta(days=90))
        data = {'total_complaints': complaints.count(), 'resolved': complaints.filter(status='resolved').count()}
    else:
        data = {'note': 'Academic report data not implemented'}
    Report.objects.create(report_type=report_type, data=data)
    reports = Report.objects.all()
    return render(request, 'reports.html', {'reports': reports, 'report_type': report_type})