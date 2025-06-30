from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Parent, Student

def is_receptionist_or_admin(user):
    return user.role in ['receptionist', 'admin']

@login_required
@user_passes_test(is_receptionist_or_admin)
def onboard_parent(request):
    if request.method == 'POST':
        parent = Parent.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone']
        )
        student_name = request.POST['student_name']
        if student_name:
            student, _ = Student.objects.get_or_create(name=student_name)
            student.parents.add(parent)
        return redirect('dashboard')
    return render(request, 'onboarding.html')