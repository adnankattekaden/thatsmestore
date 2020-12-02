from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('dashboard/', views.dashboard_overview,name='dashboard'),
    path('store/', views.store,name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.update_item,name='update_item'),
    path('process_order/', views.process_order,name='process_order'),
    path('userlogin/', views.user_login, name='userlogin'),
    path('usersignup/', views.user_signup,name='usersignup'),
    path('logout/', views.logout,name='logout'),
    path('mobilelogin/', views.mobile_login,name='mobilelogin'),
    path('verifyotp/', views.verify_otp, name='verifyotp'),
    path('profile/', views.edit_user,name='edituser'),
    path('myaddress/', views.my_address,name='myaddress'),
    path('updated/<int:id>', views.update_profile,name='updateprofile'),
    path('orderhistory/', views.order_history,name='orderhistory'),
    path('productview/<int:id>/', views.product_view,name='productview'),
    path('category/<int:id>/', views.category,name='category'),

]
