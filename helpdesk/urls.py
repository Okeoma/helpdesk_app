
from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),  
    path("register", views.register, name="register"),    
    path("logout", views.logout_view, name="logout"),
    path("account/<str:username>", views.account, name="account"),
    path("edit_ticket/<int:id>", views.edit_ticket, name="edit_ticket"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("ticketrank/<int:id>", views.ticketrank, name="ticketrank"),
    path("ticket_view/<str:ticket>", views.ticket_view, name="ticket_view"),	
    path("super", views.super, name="super"),
	path("view_reports", views.view_reports, name="view_reports"),
	path("view_reports/<str:reports>/<str:period>", views.reports, name="reports"),
	path("customer_reports/<str:customer>", views.customer_reports, name="customer_reports"),
	path("customer_reports/<str:customer>/<str:reports>/<str:period>", views.customer_periods, name="customer_periods"),
	path("user_reports/<str:username>", views.user_reports, name="user_reports"),
	path("user_reports/<str:username>/<str:reports>/<str:period>", views.user_periods, name="user_periods"),
    path("post_ticket", views.post_ticket, name="post_ticket"),
    path("admin_ticket", views.admin_ticket, name="admin_ticket"), 
    path("admin_control/<str:username>", views.admin_control, name="admin_control"),
    path("supervise/<int:id>", views.supervise, name="supervise"),
    path("supervisor/<str:username>", views.supervisor, name="supervisor"),
    path("subordinate/<str:username>", views.subordinate, name="subordinate"),
    path("profile_ticket/<str:username>", views.profile_ticket, name="profile_ticket"),
    path("add_image", views.add_image, name="add_image"),
    path("escalate", views.escalate, name="escalate"),
    path("user_view", views.user_view, name="user_view"),
    path("customer_view", views.customer_view, name="customer_view"),
    path("add_customer", views.add_customer, name="add_customer"),
    path("edit_customer/<int:id>", views.edit_customer, name="edit_customer"),
    path("close_ticket/<str:ticket>", views.close_ticket, name="close_ticket"),
	path("add_comment/<str:ticket>", views.add_comment, name="add_comment"),
	path("delete_comment/<str:comment>", views.delete_comment, name="delete_comment")
    	
    
]

