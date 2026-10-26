from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Employee


def employee_list(request):
    query = request.GET.get("q", "").strip()

    employees = Employee.objects.all().order_by("-id")

    if query:
        employees = employees.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query)
        )

    context = {
        "employees": employees,
        "query": query,
        "total_employees": Employee.objects.count(),
    }

    return render(request, "employees/employee_list.html", context)


def dashboard(request):
    return render(
        request,
        "employees/dashboard.html",
        {"total_employees": Employee.objects.count()},
    )

from .forms import EmployeeForm


def employee_add(request):
    form = EmployeeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("employee_list")

    return render(
        request,
        "employees/employee_form.html",
        {"form": form, "title": "Add Employee"},
    )


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(
        request.POST or None,
        instance=employee
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("employee_list")

    return render(
        request,
        "employees/employee_form.html",
        {"form": form, "title": "Edit Employee"}
    )


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")

    return render(
        request,
        "employees/employee_confirm_delete.html",
        {"employee": employee},
    )



@login_required
def profile(request):
    return render(request, "employees/profile.html")