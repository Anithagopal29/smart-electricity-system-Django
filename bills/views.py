from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Bill
from django.db import connection
from xhtml2pdf import pisa
import json
import io

# -------------------
# ADMIN VIEWS
# -------------------

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'AnithaGopal' and password == 'ani@123':  # ❌ Should use Django authentication
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials.")
            return redirect('admin_login')
    
    return render(request, 'bills/admin_login.html')

@csrf_exempt
def admin_dashboard(request):
    # if not request.session.get('admin_logged_in'):
    #     return redirect('admin_login')

    bills = Bill.objects.all().order_by('id')
    return render(request, 'bills/admin_dashboard.html', {'bills': bills})
# API to Fetch Bills (for JavaScript AJAX calls)
def get_bills(request):
    bills = list(Bill.objects.values())  # Convert QuerySet to list
    return JsonResponse(bills, safe=False)
@csrf_exempt

def add_bill(request):
    if request.method == "POST":
        account_number = request.POST.get("account_number")
        customer_name = request.POST.get("customer_name")
        phone_number = request.POST.get("phone_number")
        amount_due = request.POST.get("amount_due")

        # Check if account number already exists
        if Bill.objects.filter(account_number=account_number).exists():
            messages.error(request, "Account number already exists! Please use a different one.")
            return redirect("add_bill")  # Redirect to form page with error message

        # Create and save new bill
        new_bill = Bill.objects.create(
            account_number=account_number,
            customer_name=customer_name,
            phone_number=phone_number,
            amount_due=amount_due,
            status="Pending"
        )
        new_bill.save()
        messages.success(request, "Bill added successfully!")
        return redirect('admin_dashboard')  # Change this to your actual view name

    return render(request, "bills/add_bill.html")


# def delete_bill(request, bill_id):
#     try:
#         bill = Bill.objects.get(id=bill_id)
#         bill.delete()
#         messages.success(request, "Bill deleted successfully.")
#     except Bill.DoesNotExist:
#         messages.error(request, "Bill not found.")
#     return redirect('admin_dashboard')

# Delete Bill
@csrf_exempt  # Remove this if using CSRF token
def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.delete()
    return redirect('admin_dashboard')  # Redirect to admin dashboard or any page you want
    
def admin_logout(request):
    logout(request)
    return redirect('admin_dashboard')  # Replace 'admin_login' with your actual login URL name

# -------------------
# USER VIEWS
# -------------------

def user_login(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        phone_number = request.POST.get('phone_number')

        bill = Bill.objects.filter(account_number=account_number, phone_number=phone_number).first()
        if bill:
            request.session['user_bill_id'] = bill.id
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid account number or phone number.")
            return redirect('user_login')
    
    return render(request, 'bills/user_login.html')

def user_dashboard(request):
    bill_id = request.session.get('user_bill_id')
    if not bill_id:
        return redirect('user_login')
    
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'bills/user_dashboard.html', {'bill': bill})

def pay_bill(request):
    bill_id = request.session.get('user_bill_id')
    if not bill_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('user_login')

    bill = get_object_or_404(Bill, id=bill_id)
    bill.status = 'Paid'
    bill.save()

    messages.success(request, "Bill paid successfully!")
    return redirect('user_dashboard')

def download_bill_pdf(request):
    bill_id = request.session.get('user_bill_id')
    if not bill_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('user_login')

    bill = get_object_or_404(Bill, id=bill_id)
    
    html = render_to_string('bills/bill_template.html', {'bill': bill})
    buffer = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Bill_{bill.account_number}.pdf")

def user_logout(request):
    request.session.flush()
    return redirect('user_login')

# -------------------
# BILL MANAGEMENT VIEWS
# -------------------

def bill_management(request):
    return render(request, 'bills/bill_management.html')

@csrf_exempt
def save_bill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_bill = Bill.objects.create(
            account_number=data['accountNumber'],
            customer_name=data['customerName'],
            phone_number=data['phoneNumber'],
            amount_due=data['amountDue'],
            status=data['status']
        )
        return JsonResponse({'message': 'Bill saved successfully'})

def get_bills(request):
    bills = Bill.objects.all().values()
    return JsonResponse(list(bills), safe=False)

def delete_bill_api(request, id):
    try:
        bill = Bill.objects.get(id=id)
        bill.delete()
        return JsonResponse({'message': 'Bill deleted successfully'})
    except Bill.DoesNotExist:
        return JsonResponse({'message': 'Bill not found'}, status=404)

def pay_bill(request):
    bill_id = request.GET.get('id')
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == "POST":
        bill.status = "Paid"
        bill.save()
        return redirect('/user/dashboard/')

    return render(request, 'bills/pay_bill.html', {'bill': bill})
