from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Invoice, Payment
from onboarding.models import Parent
from django.core.mail import send_mail
from django.conf import settings
import uuid

def is_accountant_or_admin(user):
    return user.role in ['accountant', 'admin']

@login_required
@user_passes_test(is_accountant_or_admin)
def create_invoice(request):
    if request.method == 'POST':
        parent_id = request.POST['parent']
        amount = request.POST['amount']
        term = request.POST['term']
        due_date = request.POST['due_date']
        parent = Parent.objects.get(id=parent_id)
        Invoice.objects.create(
            parent=parent,
            amount=amount,
            term=term,
            due_date=due_date
        )
        send_mail(
            'New Invoice',
            f'Invoice for {term} amounting to {amount} is due by {due_date}.',
            settings.EMAIL_HOST_USER,
            [parent.email],
            fail_silently=False,
        )
        return redirect('dashboard')
    parents = Parent.objects.all()
    return render(request, 'fees.html', {'parents': parents})

@login_required
@user_passes_test(is_accountant_or_admin)
def record_payment(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        receipt = str(uuid.uuid4())
        Payment.objects.create(
            invoice=invoice,
            amount=amount,
            receipt=receipt
        )
        invoice.paid = True
        invoice.save()
        send_mail(
            'Payment Receipt',
            f'Payment of {amount} received. Receipt: {receipt}',
            settings.EMAIL_HOST_USER,
            [invoice.parent.email],
            fail_silently=False,
        )
        return redirect('dashboard')
    return render(request, 'fees.html', {'invoice': invoice})