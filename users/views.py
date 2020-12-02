from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
import json
import datetime
from vendor.models import Product, Userdetails,Order,OrderItem,ShippingAddress,Category
import razorpay
from django.views.decorators.csrf import csrf_exempt
import requests


import base64
from django.core.files.base import ContentFile
#starts 

def usersignup(request):
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
                messages.info(request, 'username taken')
                return render(request, 'user/userregister.html',dic)

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is Taken')
                return render(request, 'user/userregister.html',dic)
            else:
                user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                user.save()
                messages.info(request,'User Created') 
                return redirect(userlogin)
        else:
            messages.info(request,'Password Not Matching')    
            return render(request,'user/userregister.html',dic)
    else:
        return render(request, 'user/userregister.html')


def userlogin(request):
    if request.user.is_authenticated:
        return redirect(index)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user:
            auth.login(request,user)
            return redirect(index)
        else:
            messages.info(request, 'invalid credentials') 
            return redirect(userlogin)
    else:
        return render(request, 'user/userlogin.html')

def logout(request):
    auth.logout(request)
    return redirect(index)

def mobilelogin(request):
    if request.method == 'POST':
        phones = request.POST['phone']
        if User.objects.filter(last_name=phones).exists():
            url = "https://d7networks.com/api/verifier/send"

            payload = {'mobile': str(+91)+phones,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '9000'}
            files = [

            ]
            headers = {
            'Authorization': 'Token fcdf198d8c96dc240b9edc2401f5a8a65389def3'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            dict = json.loads(data.decode('utf8'))
            otp_id = dict['otp_id']
            request.session['otp_id'] = otp_id
            request.session['phone'] = phones
            return redirect(verifyotp)
        else:
            messages.error(request, 'NUmber Not Registered')
            return render(request, 'user/mobilelogin.html')
    else:
        return render(request, 'user/mobilelogin.html')

def verifyotp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        otp_id = request.session['otp_id']
        phones = request.session['phone']
        


        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': otp_id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token fcdf198d8c96dc240b9edc2401f5a8a65389def3'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data = response.text.encode('utf8')
        dict = json.loads(data.decode('utf8'))
        status = dict['status']
        print('hai')
        print(status)
        if status == 'success':
            user = User.objects.filter(last_name=phones).first()
            if user:
                if user.is_active == False:
                    messages.info(request, 'User Is Blocked')
                    return redirect(userlogin)
                else:
                    auth.login(request, user)
                    return redirect(index)
            else:
                messages.info(request, 'User Not Available')
                return redirect(userlogin)
        else:
            messages.info(request, 'Otp Invalid')
            return render(request, 'user/verifyotp.html')
    else:
        return render(request, 'user/verifyotp.html')

#corestuffs
def index(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        
        
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0} 
        cartitems = order['get_cart_items']

    category = Category.objects.all()
    products = Product.objects.all()
    context = {'products':products,'cartitems':cartitems,'category':category}
    return render(request, 'user/index.html',context)

def category(request, id):
    product = Product.objects.filter(category=id)
    category = Category.objects.all()
    
    context = {'product':product,'category':category}
    return render(request,'user/category.html',context)

def store(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0} 
        cartitems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products,'cartitems':cartitems}
    return render(request, 'user/store.html',context)


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
        cartitems = order['get_cart_items']
    context = {'items':items,'order':order,'cartitems':cartitems}
    return render(request, 'user/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        ship = ShippingAddress.objects.filter(user=user)

        client = razorpay.Client(auth=("rzp_test_P9QI5lhnHOuMk7", "42Vsw0omw3ZbXYbROCoF7SYt"))
        order_amount =  float(order.get_cart_total)
        order_amount *= 100
        order_currency = 'USD'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address':'kattekaden' 'kearla'}
        response = client.order.create(dict(amount=order_amount,currency=order_currency,receipt=order_receipt,notes=notes,payment_capture='0'))

        order_id = response['id']
        order_status = response['status']
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0} 
        cartitems = order['get_cart_items']

    context = {'items':items,'order':order,'cartitems':cartitems, 'ship':ship,'order_id':order_id}
    return render(request, 'user/checkout.html',context)


def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(productId)
    print(action)

    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0 :
        orderItem.delete()
    return JsonResponse('item Was Added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('hello', data)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save() 
        ad=data['shipping']['address']
        
        if ShippingAddress.objects.filter(user=user,address=ad).exists():
            add = 'addressnotsaved'
        else:
            ShippingAddress.objects.create(user=user,order=order,address=data['shipping']['address'],city=data['shipping']['city'],state=data['shipping']['state'],zipcode=data['shipping']['zipcode'],country=data['shipping']['country'],payment_status=data['shipping']['payment_status'])
            add = 'itemsaved'
    else:
        print('user not logged in')
    return JsonResponse(add, safe=False)

#additional

def productview(request,id):
    products = Product.objects.get(id=id)
    context = {'products':products}
    return render(request, 'user/productviewpage.html',context)

def dashboardoverview(request):
    user = request.user
    if Userdetails.objects.filter(user_id=user).exists():
        img=Userdetails.objects.get(user_id=user)
        return render(request, 'user/userdashboard.html',{'img':img})
    else:
        return render(request, 'user/userdashboard.html')



def edituser(request):   
    user = request.user.id
    if Userdetails.objects.filter(user_id=user).exists():
        con = User.objects.get(id=user)
        if Userdetails.objects.filter(user_id=user).exists():
            img=Userdetails.objects.get(user_id=user)
        print(img.image.url)
        return render(request, 'user/userprofile.html',{'con':con, 'img':img})
    else:
        con = User.objects.get(id=user)
        return render(request, 'user/userprofile.html',{'con':con})


def updateprofile(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            # image = request.FILES.get('image')
            image = request.POST['pro_img']

            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name=request.user.username + '.' + ext)

            z = User.objects.get(id=id)
            z.first_name = firstname
            z.last_name = lastname
            z.username = username
            z.email = email
            z.save()
            user=request.user
            if Userdetails.objects.filter(user_id=user).exists():
                img = Userdetails.objects.get(user_id=user)
                if image is not None:
                    img.image = data
                    img.save()
            else:
                if image is not None:
                    img = Userdetails.objects.create(image=data, user_id=user)
            return redirect(edituser)
        else:
            return render(request, 'user/userprofile.html')
    else:
        return redirect(index)


def orderhistory(request):
    user = request.user
    orders = Order.objects.filter(user=user, complete=True)
    items = []

    for order in orders:
        orderItems = OrderItem.objects.filter(order=order)
        for orderItem in orderItems:
            items.append(orderItem)
            
    context = {'items':items, 'orderItems':orderItems,'orders':orders}
    return render(request, 'user/orderhistory.html',context)

def myaddress(request):
    return render(request, 'user/myaddress.html')