from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('changepass', views.changep),
    path('change_pass', views.changepassword),
    path('admin/', views.admin, name='admin'),
    path('main_app_admin/', admin.site.urls),
    path('admin/view', views.view),
    path('admin/save', views.save),
    path('admin/delete', views.delete),
    path('admin/block', views.block),
    path('admin/logout', views.adminlogout),
    path('admin/create', views.create),
    path('admin/admin_invoices', views.admin_invoices, name='admin_invoices'),
    path('admin/admin_create_invoice', views.admin_create_invoice),
    path('admin_update_invoice/<int:invoice_id>/', views.admin_update_invoice, name='admin_update_invoice'),
    path('admin_delete_invoice/<int:invoice_id>/', views.admin_delete_invoice, name='admin_delete_invoice'),
    path('show_invoice_history/<int:invoice_id>/', views.show_invoice_history, name='show_invoice_history'),

    path('create_invoice', views.create_invoice),
    path('update_invoice/<int:invoice_id>/', views.update_invoice, name='update_invoice'),
    path('delete_invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('pdf_view/<int:invoice_id>', views.pdf_view, name="pdf_view"),
    path('send_email/<int:invoice_id>', views.send_email, name="send_email"),
    path('send_email_to_admin/<int:invoice_id>', views.send_email_to_admin, name="send_email_to_admin"),
    path('email_verification', views.email_verification, name="email_verification"),
    path('email_verified/reset_password', views.reset_password, name="reset_password"),
    path('pdf_history_view/<int:invoice_id>', views.pdf_history_view, name="pdf_history_view"),                     
    path('get_customer_data/<int:customer_id>/', views.get_customer_data, name="get_customer_data")
]