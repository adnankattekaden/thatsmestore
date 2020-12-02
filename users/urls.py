from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('dashboard/', views.dashboardoverview,name='dashboard'),
    path('store/', views.store,name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateitem,name='update_item'),
    path('process_order/', views.processOrder,name='process_order'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('usersignup/', views.usersignup,name='usersignup'),
    path('logout/', views.logout,name='logout'),
    path('mobilelogin/', views.mobilelogin,name='mobilelogin'),
    path('verifyotp/', views.verifyotp, name='verifyotp'),
    path('profile/', views.edituser,name='edituser'),
    path('myaddress/', views.myaddress,name='myaddress'),
    path('updated/<int:id>', views.updateprofile,name='updateprofile'),
    path('orderhistory/', views.orderhistory,name='orderhistory'),
    path('productview/<int:id>/', views.productview,name='productview'),
    path('category/<int:id>/', views.category,name='category'),

]
