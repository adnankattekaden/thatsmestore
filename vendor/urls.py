from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin,name='adminlogin'),
    path('dashboard/', views.admindashboard,name='admindashboard'),
    path('manageusers/', views.manageusers,name='manageusers'),
    path('createuser/', views.createuser,name='createuser'),
    path('updateuser/', views.updateuser,name='updateuser'),
    path('adminlogout', views.adminlogout,name='adminlogout'),
    path('admin/edituser/<int:id>/', views.edituser,name='edituser'),
    path('updateuser/<int:id>/', views.updateuser,name='updateuser'),
    path('deleteuser/<int:id>/', views.deleteuser,name='deleteuser'),
    path('blockuser/<int:id>/', views.blockuser,name='blockuser'),
    path('activateuser/<int:id>/', views.activateuser,name='activateuser'),
    #products
    path('manageproduct/',views.manageproduct,name='manageproduct'),
    path('createproduct/',views.createproduct,name='createproduct'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('updateproduct/<int:id>/', views.updateproduct,name='updateproduct'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('managecategory/', views.managecategory,name='managecategory'),
    path('pend/<int:id>/<str:value>/', views.pendingorder,name='pend'),
    path('completeorder/<int:id>/<str:value>/', views.completeorder,name='completeorder'),
    path('canceledorder/<int:id>/<str:value>/', views.cancelorder,name='canceledorder'),
    
    path('createcategory/', views.createcategory,name='createcategory'),
    path('editcategory/<int:id>/', views.editcategory,name='editcategory'),
    path('updatecategory/<int:id>/', views.updatecategory,name='updatecategory'),
    path('deletecategory/<int:id>/', views.deletecategory,name='deletecategory'),
    path('manageorders/', views.manageorders, name='manageorders'),
    path('report/', views.report, name='report'),
    path('salesreport/', views.salesreport,name='salesreport'),
    path('cancelreport/', views.cancelreport,name='cancelreport')
    
]
