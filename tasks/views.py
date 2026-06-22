from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Max, Count
from .models import Student
from .forms import StudentForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

def student_list(request):
    students = Student.objects.all()
    dashboard_stats = students.aggregate(
        total_students=Count('id'),
        highest_marks=Max('marks'),
        average_marks=Avg('marks'),
    )
    return render(
        request,
        'tasks/student_list.html',
        {
            'students': students,
            'total_students': dashboard_stats['total_students'] or 0,
            'highest_marks': dashboard_stats['highest_marks'] or 0,
            'average_marks': dashboard_stats['average_marks'] or 0,
        },
    )

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'tasks/student_form.html', {'form': form})

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'tasks/student_form.html', {'form': form})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'tasks/student_confirm_delete.html', {'student': student})

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Authenticated successfully!'}
        return Response(content)
