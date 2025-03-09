from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'frontend'

urlpatterns = [
    
   
    path('home/',views.index, name="index"),
  
   
    path('staff/create/', views.StaffCreateView.as_view(), name='create_staff'),
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('staff/edit/<int:pk>/', views.StaffCreateView.as_view(), name='edit_staff'), 

   ### Url for logout, login, change password
   path('', views.login_view, name='login'),
   path('logout/', views.userlogout, name="logout"),
   path('change-password/', views.change_password, name="change_password"),


   ### customer
   path('customers/', views.customer_list, name='customers_list'),
   path('add-customer/', views.add_customer, name='add_customer'),
   path('edit-customer/<int:pk>/', views.edit_customer, name='edit_customer'),
   path('delete-customer/<int:pk>/', views.delete_customer, name='delete_customer'),


   ###  excel for customer
   
   path('export/excel/', views.export_customers_excel, name='export_customers_excel'),
   

   ### purchases
   path('purchases/', views.purchase_list, name='purchase_list'),
   path('purchases/add/', views.add_purchase, name='add_purchase'),
   path('purchases/edit/<int:pk>/', views.edit_purchase, name='edit_purchase'),
   path('purchases/delete/<int:pk>/', views.delete_purchase, name='delete_purchase'),


   path('items/', views.item_list, name='item_list'),
   path('items/add/', views.add_item, name='add_item'),
   path('items/edit/<int:item_id>/', views.edit_item, name='edit_item'),
   path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),

   path('categories/', views.category_list, name='category_list'),
   path('categories/add/', views.category_create, name='category_create'),
   path('categories/edit/<int:pk>/', views.category_update, name='category_update'),
   path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),


   path('expenses/', views.expense_list, name='expense_list'),
   path('expenses/add/', views.expense_create, name='expense_create'),
   path('expenses/edit/<int:pk>/', views.expense_update, name='expense_update'),
   path('expenses/delete/<int:pk>/', views.expense_delete, name='expense_delete'),


   path('expense-categories/', views.expense_category_list, name='expense_category_list'),
   path('expense-categories/add/', views.expense_category_add, name='expense_category_add'),
   path('expense-categories/edit/<int:pk>/', views.expense_category_edit, name='expense_category_edit'),
   path('expense-categories/delete/<int:pk>/', views.expense_category_delete, name='expense_category_delete'),
   

   path("search-customer/", views.search_customer, name="search_customer"),
   path("create-customer/", views.create_customer, name="create_customer"),


   path('pos/', views.pos_page, name='pos_page'),

   path('generate-item-code/', views.generate_item_code, name='generate_item_code'),

   path('about/', views.organization_setting_view, name='organization_setting'),

   path('save/sale/', views.save_sale, name='save_sale'),
   path('sale/list/', views.sale_list, name='sale_list'),
   path('sale/detail/<int:sale_id>/', views.sale_detail, name='sale_detail'),


   path('export/sales/excel/', views.export_sales_excel, name='export_sales_excel'),

   path("export-items-excel/", views.export_items_excel, name="export_items_excel"),


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

