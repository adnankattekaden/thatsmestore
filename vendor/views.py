import base64
import json
from tabnanny import check
from urllib import request

import requests
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.base import ContentFile
from django.shortcuts import HttpResponse, redirect, render

from .models import *

# Create your views here.



def adminlogin(request):
    if request.session.has_key('username'):
        return redirect(admindashboard)

    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        print(user)
        print(password)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        print(recaptcha_response)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret="6LdggOwZAAAAAIgOyrSNRpOYLISII4ADvG1_5ydO"
        cap_data = {"secret":cap_secret,"response":recaptcha_response}
        cap_server_response=requests.post(url=url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)
        print(cap_json)
        if cap_json['success']==False:
            messages.error(request,"Inavalid captcha try again")
            return redirect("adminlogin")
        if user=='admin' and password=='admin':
            request.session['username'] = user
            return redirect(admindashboard) 

        else:
            messages.info(request,'invalid credentials')
            return redirect(adminlogin)
    else:
        return render(request, 'vendor/adminloginpage.html')


def admindashboard(request):
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
        return redirect(adminlogin)


def adminlogout(request):
    request.session.flush()
    return redirect(adminlogin) 

#ManageUSers

def manageusers(request):
    if request.session.has_key('username'):
        users = User.objects.filter(is_superuser=False)
        return render(request, 'vendor/manageusers.html',{'users':users})
    else:
        return redirect(adminlogin)


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
                        return redirect(admindashboard)
                else:
                    messages.info(request,'Password Not Matching')    
                    return render(request,'vendor/createuser.html',dic)
            else:               
                return render(request,'vendor/createuser.html')
        else:
            return redirect(adminlogin)


def updateuser(request, id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']

            z = User.objects.get(id=id)
            z.first_name = firstname
            z.last_name = lastname
            z.username = username
            z.email = email
            z.save()
            return redirect(admindashboard)  
        else:
            return render(request, 'vendor/updateuser.html')
    else:
        redirect(adminlogin)


def edituser(request, id):
    if request.session.has_key('username'):
        con = User.objects.get(id=id)
        return render(request, 'vendor/updateuser.html',{"con":con})
    else:
        return redirect(adminlogin)


def deleteuser(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.delete()
        return redirect(admindashboard)
    else:
        return redirect(adminlogin)

def blockuser(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.is_active = False
        print(u.is_active)
        u.save()
        return redirect(manageusers)
    else:
        return redirect(adminlogin)

def activateuser(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.is_active = True
        print(u.is_active)
        u.save()
        return redirect(manageusers)
    else:
        return redirect(adminlogin)


#ManageProducts

def manageproduct(request):
    if request.session.has_key('username'):
        products = Product.objects.all()
        return render(request, 'vendor/manageproduct.html',{'products':products})
    else:
        return redirect(adminlogin)


def createproduct(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            productname = request.POST['productname']
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST['description']
            # image = request.FILES['image']
            image = request.POST['pro_img']
            category = Category.objects.get(id=request.POST['category'])

            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name=request.user.username + '.' + ext)


            j = Product.objects.create(productname=productname,price=price,stock=stock,description=description,category=category,image=data)
            j.save()
            messages.info(request,'Product Created')
            return redirect(manageproduct)
        else:
            category = Category.objects.all()            
            return render(request,'vendor/createproduct.html',{'category':category})
    else:
        return redirect(adminlogin)



def editproduct(request, id):
    if request.session.has_key('username'):
        con = Product.objects.get(id=id)
        category = Category.objects.all() 
        return render(request, 'vendor/updateproduct.html',{"con":con, 'category':category})
    else:
        return redirect(adminlogin)

def updateproduct(request, id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            productname = request.POST['productname']
            price = request.POST['price']
            stock = request.POST['stock']
            # image = request.FILES['image']
            image = request.POST['pro_img']
            description = request.POST['description']
            category = Category.objects.get(id=request.POST['category'])

            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name=request.user.username + '.' + ext)

            z = Product.objects.get(id=id)
            
            z.productname = productname
            z.price = price
            z.stock = stock
            z.image = data
            z.description = description
            z.category = category
            z.save()
            return redirect(admindashboard)  
        else:
            return render(request, 'vendor/updateproduct.html')
    else:
        redirect(adminlogin)


def deleteproduct(request,id):
    if request.session.has_key('username'):
        u = Product.objects.get(id=id)
        u.delete()
        return redirect(manageproduct)
    else:
        return redirect(adminlogin)

def managecategory(request):
    if request.session.has_key('username'):
        category = Category.objects.all()

        return render(request, 'vendor/managecategory.html',{'category':category})
    else:
        return redirect(adminlogin)

def createcategory(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            categories = request.POST['category']
            category = Category.objects.create(categoryname=categories)
            messages.info(request,'Category Created')
            return redirect(managecategory)
        else:               
            return render(request,'vendor/createcategory.html')
    else:
        return redirect(adminlogin)


def editcategory(request, id):
    if request.session.has_key('username'):
        con = Category.objects.get(id=id)
        return render(request, 'vendor/updatecategory.html',{"con":con})
    else:
        return redirect(adminlogin)



def updatecategory(request, id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            category = request.POST['category']
            image = request.FILES['image']

            z = Category.objects.get(id=id)
            z.categoryname = category
            z.categoryimage = image
            z.image = image
            z.save()
            return redirect(managecategory)  
        else:
            return render(request, 'vendor/updatecategory.html')
    else:
        redirect(adminlogin)


def deletecategory(request,id):
    if request.session.has_key('username'):
        u = Category.objects.get(id=id)
        u.delete()
        return redirect(managecategory)
    else:
        return redirect(adminlogin)
#manage Orders

def manageorders(request):
    orders = Order.objects.filter(complete=True)
    # adress=orders.shippingaddress_set.all()
    # print("hello",adress)
    # dic={}
    # for order in orders:
    #     print(order)
    #     try:
    #         adress=ShippingAddress.objects.get(order=order)
    #         print("hhhe",adress)
    #         dic[order.id]=adress.

    #     except:
    #         pass
   
    # print("hello",dic)

    # print(order)
    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def pendingorder(request,id,value):
    order = Order.objects.get(id=id)
    order.status = value
    order.save()
    print(order.status)
    orders = Order.objects.filter(complete=True)
    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def completeorder(request,id,value):
    orders = Order.objects.filter(complete=True)
    order = Order.objects.get(id=id)
    order.status = value
    order.save()

    context = {'orders':orders}
    return render(request, 'vendor/manageorder.html',context)

def cancelorder(request,id,value):
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
        print(start_date)
        print(end_date)
        complete =  Order.objects.filter(date_ordered__range=[start_date, end_date], status='complete').count()
        pending = Order.objects.filter(date_ordered__range=[start_date, end_date], status='pending').count()
        canceled = Order.objects.filter(status='cancelled').count()
        print(canceled)
        return render(request, 'vendor/report.html', {'complete':complete,'pending':pending,'canceled':canceled})
    else:
        return render(request, 'vendor/report.html')

def salesreport(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        lists = []
        orders = Order.objects.filter(date_ordered__range=[start_date, end_date], status='complete')

        context = {'orders':orders}
        return render(request, 'vendor/salesreport.html',context)
    else:
        return render(request, 'vendor/salesreport.html')

def cancelreport(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        orderdates =  Order.objects.filter(date_ordered__range=[start_date, end_date]).count()
        pending = Order.objects.filter(date_ordered__range=[start_date, end_date], complete=True).count()
        return render(request, 'vendor/cancelreport.html', {'orderdates':orderdates,'pending':pending})
    else:
        return render(request, 'vendor/cancelreport.html')
