from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Message
from onboarding.models import Parent
from twilio.rest import Client
from django.core.mail import send_mail
from django.conf import settings
import requests

def is_teacher_receptionist_or_admin(user):
    return user.role in ['teacher', 'receptionist', 'admin']

@login_required
@user_passes_test(is_teacher_receptionist_or_admin)
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST['recipient']
        message_type = request.POST['message_type']
        content = request.POST['content']
        recipient = Parent.objects.get(id=recipient_id)
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            message_type=message_type,
            content=content
        )
        if message_type == 'sms':
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=content,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=recipient.phone
            )
            message.delivered = True
            message.save()
        elif message_type == 'email':
            send_mail(
                'School Update',
                content,
                settings.EMAIL_HOST_USER,
                [recipient.email],
                fail_silently=False,
            )
            message.delivered = True
            message.save()
        return redirect('dashboard')
    parents = Parent.objects.all()
    return render(request, 'communication.html', {'parents': parents})

@login_required
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST['message']
        headers = {'Authorization': f'Bearer {settings.XAI_API_KEY}'}
        response = requests.post(
            'https://api.x.ai/grok3/chat',
            json={'message': user_message},
            headers=headers
        )
        if response.status_code == 200:
            bot_response = response.json().get('response', 'Sorry, I could not process your request.')
        else:
            bot_response = 'Error connecting to chatbot.'
        return render(request, 'communication.html', {
            'bot_response': bot_response,
            'parents': Parent.objects.all()
        })
    return render(request, 'communication.html', {'parents': Parent.objects.all()})