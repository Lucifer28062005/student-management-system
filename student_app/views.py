from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')


# LOGIN
def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('student_list')
    return render(request, 'student_app/login.html', {'form': form})


# LIST + SEARCH + PAGINATION
@login_required
def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )

    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render(request, 'student_app/student_list.html', {'students': students})


# ADD
@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Student Added!")
        return redirect('student_list')
    return render(request, 'student_app/student_form.html', {'form': form})


# EDIT
@login_required
def student_edit(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Student Updated!")
        return redirect('student_list')
    return render(request, 'student_app/student_form.html', {'form': form})


# DELETE
@login_required
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student Deleted!")
    return redirect('student_list')