from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login,name='adminlogin'),
    path('dashboard/', views.admin_dashboard,name='admindashboard'),
    path('manageusers/', views.manage_users,name='manageusers'),
    path('createuser/', views.createuser,name='createuser'),
    path('edituser/<int:id>/', views.edit_user,name='edituser'),
    path('adminlogout', views.admin_logout,name='adminlogout'),
    path('edituser/<int:id>/', views.edit_user,name='edituser'),
    path('updateuser/<int:id>/', views.update_user,name='updateuser'),
    path('deleteuser/<int:id>/', views.delete_user,name='deleteuser'),
    path('blockuser/<int:id>/', views.block_user,name='blockuser'),
    path('activateuser/<int:id>/', views.activate_user,name='activateuser'),
    #products
    path('manageproduct/',views.manage_product,name='manageproduct'),
    path('createproduct/',views.create_product,name='createproduct'),
    path('editproduct/<int:id>/',views.edit_product,name='editproduct'),
    path('updateproduct/<int:id>/', views.update_product,name='updateproduct'),
    path('deleteproduct/<int:id>/',views.delete_product,name='deleteproduct'),
    path('managecategory/', views.manage_category,name='managecategory'),
    path('pend/<int:id>/<str:value>/', views.pending_order,name='pend'),
    path('completeorder/<int:id>/<str:value>/', views.complete_order,name='completeorder'),
    path('canceledorder/<int:id>/<str:value>/', views.cancel_order,name='canceledorder'),
    
    path('createcategory/', views.create_category,name='createcategory'),
    path('editcategory/<int:id>/', views.edit_category,name='editcategory'),
    path('updatecategory/<int:id>/', views.update_category,name='updatecategory'),
    path('deletecategory/<int:id>/', views.delete_category,name='deletecategory'),
    path('manageorders/', views.manage_orders, name='manageorders'),
    path('report/', views.report, name='report'),
    path('salesreport/', views.sales_report,name='salesreport'),
    path('cancelreport/', views.cancel_report,name='cancelreport')
    
]
