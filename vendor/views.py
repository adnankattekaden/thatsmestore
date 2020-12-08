import base64
import json
from tabnanny import check
from urllib import request
import requests
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.base import ContentFile
from django.shortcuts import HttpResponse, redirect, render
from datetime import date


from .models import *
from django.db.models import Sum

# Create your views here.

def admin_login(request):
    if request.session.has_key('username'):
        return redirect(admin_dashboard)

    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret="6LdggOwZAAAAAIgOyrSNRpOYLISII4ADvG1_5ydO"
        cap_data = {"secret":cap_secret,"response":recaptcha_response}
        cap_server_response=requests.post(url=url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)
        if cap_json['success']==False:
            messages.error(request,"Inavalid captcha try again")
            return redirect("adminlogin")
        if user=='admin' and password=='admin':
            request.session['username'] = user
            return redirect(admin_dashboard) 
        else:
            messages.info(request,'invalid credentials')
            return redirect(admin_login)
    else:
        return render(request, 'vendor/adminloginpage.html')


def admin_dashboard(request):
    if request.session.has_key('username'):
        users = User.objects.filter(is_superuser=False)
        products = Product.objects.all()
        orderitem = OrderItem.objects.all()
        length_user = len(users)
        length_products = len(products)
        length_orderitem = len(orderitem)
        context = {'length_user':length_user,'length_products':length_products,'length_orderitem':length_orderitem}
        return render(request, 'vendor/admindashboard.html',context)
    else:
        return redirect(admin_login)


def admin_logout(request):
    request.session.flush()
    return redirect(admin_login) 

#ManageUSers

def manage_users(request):
    if request.session.has_key('username'):
        users = User.objects.filter(is_superuser=False)
        return render(request, 'vendor/manageusers.html',{'users':users})
    else:
        return redirect(admin_login)


def createuser(request):
        if request.session.has_key('username'):
            if request.method == 'POST':
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                password2 = request.POST['password2']
                dic={"firstname":firstname, "lastname":lastname, "email":email, "username":username}

                if password==password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request,'Username Taken')
                        return render(request, 'vendor/createuser.html',dic)

                    elif User.objects.filter(email=email).exists():
                        messages.info(request,'Email Taken')
                        return render(request, 'vendor/createuser.html',dic)

                    else:
                        user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                        user.save()
                        messages.info(request,'User Created') 
                        return redirect(manage_users)
                else:
                    messages.info(request,'Password Not Matching')    
                    return render(request,'vendor/createuser.html',dic)
            else:               
                return render(request,'vendor/createuser.html')
        else:
            return redirect(admin_login)


def update_user(request, id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']

            user_data = User.objects.get(id=id)
            user_data.first_name = first_name
            user_data.last_name = last_name
            user_data.username = username
            user_data.email = email
            user_data.save()
            return redirect(manage_users)  
        else:
            return render(request, 'vendor/updateuser.html')
    else:
        redirect(admin_login)

def edit_user(request, id):
    if request.session.has_key('username'):
        con = User.objects.get(id=id)
        return render(request, 'vendor/updateuser.html',{"con":con})
    else:
        return redirect(admin_login)

def delete_user(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.delete()
        return redirect(manage_users)
    else:
        return redirect(admin_login)

def block_user(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.is_active = False
        print(u.is_active)
        u.save()
        return redirect(manage_users)
    else:
        return redirect(admin_login)

def activate_user(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.is_active = True
        print(u.is_active)
        u.save()
        return redirect(manage_users)
    else:
        return redirect(admin_login)

#ManageProducts

def manage_product(request):
    if request.session.has_key('username'):
        products = Product.objects.all()
        return render(request, 'vendor/manageproduct.html',{'products':products})
    else:
        return redirect(admin_login)


def create_product(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            productname = request.POST['productname']
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST['description']
            image = request.POST['pro_img']
            category = Category.objects.get(id=request.POST['category'])
            if image is not '':
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=request.user.username + '.' + ext)
                
            product_data = Product.objects.create(productname=productname,price=price,stock=stock,description=description,category=category,image=data)
            product_data.save()
            messages.info(request,'Product Created')
            return redirect(manage_product)
        else:
            category = Category.objects.all()            
            return render(request,'vendor/createproduct.html',{'category':category})
    else:
        return redirect(admin_login)

def edit_product(request, id):
    if request.session.has_key('username'):
        con = Product.objects.get(id=id)
        category = Category.objects.all() 
        return render(request, 'vendor/updateproduct.html',{"con":con, 'category':category})
    else:
        return redirect(admin_login)

def update_product(request, id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            productname = request.POST['productname']
            price = request.POST['price']
            stock = request.POST['stock']
            image = request.POST['pro_img']
            description = request.POST['description']
            category = Category.objects.get(id=request.POST['category'])
            

            product_data = Product.objects.get(id=id)
            product_data.productname = productname
            product_data.price = price
            product_data.stock = stock
            product_data.description = description
            product_data.category = category

            if image is not '':
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=request.user.username + '.' + ext)
                product_data.image = data

            product_data.save()
            return redirect(manage_product)  
        else:
            return render(request, 'vendor/updateproduct.html')
    else:
        redirect(admin_login)

def delete_product(request,id):
    if request.session.has_key('username'):
        u = Product.objects.get(id=id)
        u.delete()
        return redirect(manage_product)
    else:
        return redirect(admin_login)

def manage_category(request):
    if request.session.has_key('username'):
        category = Category.objects.all()

        return render(request, 'vendor/managecategory.html',{'category':category})
    else:
        return redirect(admin_login)

def create_category(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            categories = request.POST['category']
            category = Category.objects.create(categoryname=categories)
            messages.info(request,'Category Created')
            return redirect(manage_category)
        else:               
            return render(request,'vendor/createcategory.html')
    else:
        return redirect(admin_login)

def edit_category(request, id):
    if request.session.has_key('username'):
        con = Category.objects.get(id=id)
        return render(request, 'vendor/updatecategory.html',{"con":con})
    else:
        return redirect(admin_login)

def update_category(request, id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            category = request.POST['category']
            category_data = Category.objects.get(id=id)
            category_data.categoryname = category
            category_data.save()
            return redirect(manage_category)  
        else:
            return render(request, 'vendor/updatecategory.html')
    else:
        redirect(admin_login)

def delete_category(request,id):
    if request.session.has_key('username'):
        deletecategory = Category.objects.get(id=id)
        deletecategory.delete()
        return redirect(manage_category)
    else:
        return redirect(admin_login)

#manage Orders
def manage_orders(request):
    orders = Order.objects.filter(complete=True)
    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def pending_order(request,id,value):
    order = Order.objects.get(id=id)
    order.status = value
    order.save()
    orders = Order.objects.filter(complete=True)
    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def complete_order(request,id,value):
    orders = Order.objects.filter(complete=True)
    order = Order.objects.get(id=id)
    order.status = value
    order.save()
    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def cancel_order(request,id,value):
    orders = Order.objects.filter(complete=True)
    order = Order.objects.get(id=id)
    order.status = value
    order.save()
    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def report(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        complete =  Order.objects.filter(date_ordered__range=[start_date, end_date], status='complete').count()
        pending = Order.objects.filter(date_ordered__range=[start_date, end_date], status='pending').count()
        canceled = Order.objects.filter(status='cancelled').count()
        context =  {'complete':complete,'pending':pending,'canceled':canceled}
        return render(request, 'vendor/report.html',context)
    else:
        today = date.today()
        complete =  Order.objects.filter(date_ordered = today, status='complete').count()
        pending = Order.objects.filter(date_ordered = today, status='pending').count()
        canceled = Order.objects.filter(status='cancelled').count()
        context =  {'complete':complete,'pending':pending,'canceled':canceled}
        return render(request, 'vendor/report.html',context)

def sales_report(request):
    
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        orders = Order.objects.filter(date_ordered__range=[start_date, end_date], status='complete').order_by('date_ordered')
        dict = {}
        count = 1
        for order in orders:
            if not order.date_ordered in dict.keys():
                dict[order.date_ordered] = order
                dict[order.date_ordered].total= order.get_cart_total
                dict[order.date_ordered].count= count
                print(order.get_cart_total)
            else:
                dict[order.date_ordered].total += order.get_cart_total
                dict[order.date_ordered].count += count
        context = {'dict':dict}
        return render(request, 'vendor/salesreport.html',context)
    else:
        today = date.today()
        orders = Order.objects.filter(date_ordered=today, status='complete').order_by('date_ordered')
        dict = {}
        count = 1
        for order in orders:
            if not order.date_ordered in dict.keys():
                dict[order.date_ordered] = order
                dict[order.date_ordered].total= order.get_cart_total
                dict[order.date_ordered].count= count
            else:
                dict[order.date_ordered].total += order.get_cart_total
                dict[order.date_ordered].count += count
        context = {'dict':dict}
        return render(request, 'vendor/salesreport.html',context)

def cancel_report(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        orders = Order.objects.filter(date_ordered__range=[start_date, end_date], status='cancelled').order_by('date_ordered')
        dict = {}
        count = 1
        for order in orders:
            if not order.date_ordered in dict.keys():
                dict[order.date_ordered] = order
                dict[order.date_ordered].total= order.get_cart_total
                dict[order.date_ordered].count= count
                print(order.get_cart_total)
            else:
                dict[order.date_ordered].total += order.get_cart_total
                dict[order.date_ordered].count += count
        context = {'dict':dict}
        return render(request, 'vendor/cancelreport.html',context)
    else:
        today = date.today()
        orders = Order.objects.filter(date_ordered=today, status='cancelled').order_by('date_ordered')
        print(orders)
        dict = {}
        count = 1
        for order in orders:
            if not order.date_ordered in dict.keys():
                dict[order.date_ordered] = order
                dict[order.date_ordered].total= order.get_cart_total
                dict[order.date_ordered].count= count
                print(order.get_cart_total)
            else:
                dict[order.date_ordered].total += order.get_cart_total
                dict[order.date_ordered].count += count
        context = {'dict':dict}
        return render(request, 'vendor/cancelreport.html',context)
