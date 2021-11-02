from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import datetime
from datetime import datetime, timedelta, time 
import json
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views.generic import ListView
from helpdesk.models import *
from django.db.models import *
from django import forms

max_tickets = 10

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if not username:
            return render(request, "helpdesk/register.html", {
                "message": "You must enter a username.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
                })
        
        if not email:
            return render(request, "helpdesk/register.html", {
                "message": "You must enter an email.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
                })

        if not password:
            return render(request, "helpdesk/register.html", {
                "message": "You must enter a password.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
                })
        if password != confirmation:
            return render(request, "helpdesk/register.html", {
                "message": "Passwords must match.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
            })

        # Attempt to create new user
        try:
            email_exist = User.objects.filter(email=email)
            if not email_exist:
                user = User.objects.create_user(username, email, password)
                user.save()
            else:
                return render(request, "helpdesk/register.html", {
                "message": "Email has already been taken.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
            })
        except IntegrityError:
            return render(request, "helpdesk/register.html", {
                "message": "*Username already taken.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
            })
        login(request, user)
        return redirect("account", username)
    else:
        if request.user.is_anonymous:
            return render(request, "helpdesk/register.html", {
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
            })
        else:
            return redirect('index')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "helpdesk/login.html", {
                "message": "Invalid username and/or password.",
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
            })
    else:
        if request.user.is_anonymous:
            return render(request, "helpdesk/login.html", {
                "helpdesk": Dynamics.objects.get(id=2),
                "support": Dynamics.objects.get(id=4)
            })
        else: 
            return redirect('index')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    

def index(request):
    user = request.user   
    
    if not request.user.is_authenticated:
        picture = Dynamics.objects.get(id=1)
    else:
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()
    if request.user.is_authenticated:
        user = request.session["_auth_user_id"]
        ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
        tickets = Ticket.objects.filter(user=user).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
        paginator = Paginator(tickets, max_tickets)
        page_no = request.GET.get("page")
        ticket_items = paginator.get_page(page_no)         
        return render(request, "helpdesk/index.html", {
            "tickets": ticket_items,            
            "picture": picture, 
            "support": Dynamics.objects.get(id=4),            
            "form": NewPost(),            
            "edit_ticket": EditPost()
        })        
    else:
        dynamics = Dynamics.objects.get(id=3)
        return render(request, "helpdesk/index.html", {  
            "support": Dynamics.objects.get(id=4),  
            "dynamics": dynamics,               
            "helpdesk": Dynamics.objects.get(id=2)           
        }) 
        
def account(request, username):
    if request.user.is_authenticated:
        user = request.user      
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()    
        if request.method == 'GET':
            profile = User.objects.get(username=username)
            if request.user.is_anonymous:
                return redirect("login")
            if profile.username == user.username:
                return render(request, "helpdesk/account.html", {			
                    "picture": picture,
                    "support": Dynamics.objects.get(id=4),
                    "helpdesk": Dynamics.objects.get(id=2),
			        "profile": profile,				
			    })
            else:
                return redirect("login")		
        else: 
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            role = request.POST["role"]
            location = request.POST["location"]
        
            profile = User.objects.get(username=username)
            profile.first_name = first_name
            profile.last_name = last_name   
            profile.role = role
            profile.location = location            
            email_exist = User.objects.filter(email=email)
            if not email_exist or profile.email == email:
                profile.email = email
            else:
                return render(request, "helpdesk/account.html", {			    
                    "picture": picture,
                    "support": Dynamics.objects.get(id=4),
                    "helpdesk": Dynamics.objects.get(id=2),
			        "profile": profile, 				
				    "message": "Email already taken"})        
            profile.save()        
            return render(request, "helpdesk/account.html",{
                "picture": picture,
                "support": Dynamics.objects.get(id=4),
                "helpdesk": Dynamics.objects.get(id=2),
			    "profile": profile, 			
		        "message": "Account details has been updated successfully"})    
    else:
        return redirect('index')
		
def edit_customer(request, id):
    if request.user.is_authenticated:
        user = request.user      
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()
    		
            if request.method == 'GET':  
                profile = Customer.objects.get(id=id)     
                return render(request, "helpdesk/edit_customer.html", {	 
                    "picture": picture,        
                    "support": Dynamics.objects.get(id=4),
                    "helpdesk": Dynamics.objects.get(id=2),
			        "profile": profile            			
			        })  		
            else: 
                profile = Customer.objects.get(id=id)        
                firstname = request.POST["firstname"]
                lastname = request.POST["lastname"]
                email = request.POST["email"]        
                phone_no = request.POST["phone_no"]        
                company = request.POST["company"]
                location = request.POST["location"]        
        
                profile.firstname = firstname
                profile.lastname = lastname
                profile.email = email       
                profile.phone_no = phone_no
                profile.company = company
                profile.location = location       
              
                profile.save()        
                return render(request, "helpdesk/edit_customer.html",{ 
                    "picture": picture,        
                    "support": Dynamics.objects.get(id=4),
                    "helpdesk": Dynamics.objects.get(id=2),
			        "profile": profile, 			
		            "message": "Customer's details has been updated successfully"})
    else:
        return redirect('index')
		
def user_view(request):
    if request.user.is_authenticated:
        user = request.user    
        if request.user.access != 'Regular':	
            user_picture = User.objects.get(username=user)
            pictures = Picture.objects.filter(user=user_picture)
            pictures_count = pictures.count()
            if pictures_count == 0:
                picture = Dynamics.objects.get(id=1)
            else:
                picture = pictures.first()
            return render(request, "helpdesk/users.html", {
            "all_users": User.objects.all(),
            "picture": picture,
            "support": Dynamics.objects.get(id=4),
            "helpdesk": Dynamics.objects.get(id=2)            
            })
        else:
            return redirect('index')
    else:
        return redirect('index')			
            
            
def customer_view(request):
    if request.user.is_authenticated:
        user = request.user      
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()
        return render(request, "helpdesk/customers.html", {
            "customers": Customer.objects.all(),
            "picture": picture,
            "support": Dynamics.objects.get(id=4),
            "helpdesk": Dynamics.objects.get(id=2),
            'form': AddCustomer()    
        })  
    else:
        return HttpResponseRedirect(reverse("index"))
		

def profile(request, username):
    if request.user.is_authenticated:
        person_count=0
        profile_account = User.objects.get(username=username)    
        user_picture = User.objects.get(username=profile_account)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()    
        if request.method == "GET":
            access_user = request.session["_auth_user_id"]
            person_count = Senior.objects.filter(senior=access_user, junior=profile_account).count()
            ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=access_user)
            tickets = Ticket.objects.filter(user=profile_account).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))    
            junior = Senior.objects.filter(senior=profile_account)
            senior = Senior.objects.filter(junior=profile_account)    
            junior_count = Senior.objects.filter(senior=profile_account).count()
            senior_count = Senior.objects.filter(junior=profile_account).count()
            paginator = Paginator(tickets, max_tickets)
            page_no = request.GET.get('page')
            ticket_items = paginator.get_page(page_no)
            return render(request, "helpdesk/profile.html", {
                "profile_account": profile_account,
                "picture": picture,
                "support": Dynamics.objects.get(id=4),
		        "tickets": ticket_items, 
		        "ticket_count": tickets.count(),
		        "person_count": person_count, 
                "junior": junior,
                "senior": senior,
                "non_senior": User.objects.exclude(username=profile_account).all(),
		        "junior_count": junior_count, 
		        "senior_count": senior_count, 
		        "form": NewPost(), 
                "updateform": UserAccessForm(),
		        "edit_ticket": EditPost()
            })
    else:
	    return redirect('index')

def super(request):
    user = request.user
    if not request.user.is_authenticated:
        picture = Dynamics.objects.get(id=1)
    else:
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()
    if request.user.is_authenticated:
        if request.user.access != 'Regular':
            user = request.session["_auth_user_id"]
            ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
            tickets = Ticket.objects.filter().order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))		
            paginator = Paginator(tickets, max_tickets)
            page_no = request.GET.get("page")
            ticket_items = paginator.get_page(page_no)     
            return render(request, "helpdesk/super.html", {
                "tickets": ticket_items, 
                "picture": picture,
                "support": Dynamics.objects.get(id=4),         
                "personel": User.objects.all(),        
                "form": AdminTicket(),                
                "edit_ticket": EditPost()
            })
        else:
            return redirect('index')
    else:
        return redirect('index')
		
def user_reports(request, username):
    if request.user.is_authenticated:
        profile_account = User.objects.get(username=username)        
        alltickets_count = Ticket.objects.filter(user=profile_account).count()
        opentickets_count = Ticket.objects.filter(user=profile_account, closed=False).count()
        closedtickets_count = Ticket.objects.filter(user=profile_account, closed=True).count()
	
        user = request.session["_auth_user_id"]
        ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
        tickets = Ticket.objects.filter(user=profile_account).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
        title = f"{profile_account}'s Ticket"    
        return render(request, "helpdesk/user_reports.html", {
	        "support": Dynamics.objects.get(id=4),
		    "title" : title,
            "total" : alltickets_count,				
		    "tickets" : tickets,
		    "profile_account": profile_account,
		    "alltickets_count" : alltickets_count,
		    "opentickets_count" : opentickets_count,
		    "closedtickets_count" : closedtickets_count
	        })        
    else:
        return redirect('index')
		
def user_periods(request, username, reports, period):
    if request.user.is_authenticated:
        profile_account = User.objects.get(username=username)
        alltickets_count = Ticket.objects.filter(user=profile_account).count()
        opentickets_count = Ticket.objects.filter(user=profile_account, closed=False).count()
        closedtickets_count = Ticket.objects.filter(user=profile_account, closed=True).count()
	
        user = request.session["_auth_user_id"]
        ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
        tickets = Ticket.objects.filter(user=profile_account).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
        title = f"{profile_account}'s Ticket"
        today = datetime.datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.datetime.combine(today, time())
        today_end = datetime.datetime.combine(tomorrow, time())
	
        today = datetime.datetime.today()
        one_week_ago = today - timedelta(days=7)
        if reports == "alltickets":		
            tickets = Ticket.objects.filter(user=profile_account).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"All {profile_account}'s Tickets"
            total = alltickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user=profile_account, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"All Today's Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user=profile_account, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"All this Week's Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(user=profile_account, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"All this Month's Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, date__year=today.year, date__month=today.month).count()
        elif reports == "opentickets":		
            tickets = Ticket.objects.filter(user=profile_account, closed=False).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"{profile_account}'s Open Tickets"
            total = opentickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user=profile_account, closed=False, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"Today's Open Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, closed=False, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user=profile_account, closed=False, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Week's Open Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, closed=False, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(user=profile_account, closed=False, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Month's Open Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, closed=False, date__year=today.year, date__month=today.month).count()
        elif reports == "closedtickets":		
            tickets = Ticket.objects.filter(user=profile_account, closed=True).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"{profile_account}'s Closed Tickets"
            total = closedtickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user=profile_account, closed=True, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"Today's Closed Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, closed=True, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user=profile_account, closed=True, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Week's Closed Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, closed=True, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(user=profile_account, closed=True, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Month's Closed Tickets for {profile_account}"
                total = Ticket.objects.filter(user=profile_account, closed=True, date__year=today.year, date__month=today.month).count()            	
        return render(request, "helpdesk/user_reports.html", {
	        "support": Dynamics.objects.get(id=4),
		    "title" : title,
            "total" : total,			
		    "tickets" : tickets,
		    "reports": reports,
		    "profile_account" : profile_account,
		    "alltickets_count" : alltickets_count,
		    "opentickets_count" : opentickets_count,
		    "closedtickets_count" : closedtickets_count
	    })
    else:	    
        return redirect('index')
		
		
def customer_reports(request, customer):
    if request.user.is_authenticated:
        if request.user.access != 'Regular':
            alltickets_count = Ticket.objects.filter(customer__customer=customer).count()
            opentickets_count = Ticket.objects.filter(customer__customer=customer, closed=False).count()
            closedtickets_count = Ticket.objects.filter(customer__customer=customer, closed=True).count()
	
            user = request.session["_auth_user_id"]
            ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
            tickets = Ticket.objects.filter(customer__customer=customer).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"{customer}'s Ticket"    
            return render(request, "helpdesk/customer_reports.html", {
	            "support": Dynamics.objects.get(id=4),
		        "title" : title,
                "total" : alltickets_count,				
		        "tickets" : tickets,
		        "customer" : customer,
		        "alltickets_count" : alltickets_count,
		        "opentickets_count" : opentickets_count,
		        "closedtickets_count" : closedtickets_count
	        })
        else:
            return redirect('index')
    else:
        return redirect('index')
		
def customer_periods(request, customer, reports, period):
    if request.user.is_authenticated:
        alltickets_count = Ticket.objects.filter(customer__customer=customer).count()
        opentickets_count = Ticket.objects.filter(customer__customer=customer, closed=False).count()
        closedtickets_count = Ticket.objects.filter(customer__customer=customer, closed=True).count()
	
        user = request.session["_auth_user_id"]
        ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
        tickets = Ticket.objects.filter(customer__customer=customer).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
        title = f"{customer}'s Ticket"    
        today = datetime.datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.datetime.combine(today, time())
        today_end = datetime.datetime.combine(tomorrow, time())
	
        today = datetime.datetime.today()
        one_week_ago = today - timedelta(days=7)
        if reports == "alltickets":		
            tickets = Ticket.objects.filter(customer__customer=customer).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"All {customer}'s Tickets"
            total = alltickets_count
            if period == "today":
                tickets = Ticket.objects.filter(customer__customer=customer, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"All Today's Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(customer__customer=customer, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"All this Week's Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(customer__customer=customer, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"All this Month's Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, date__year=today.year, date__month=today.month).count()
        elif reports == "opentickets":		
            tickets = Ticket.objects.filter(customer__customer=customer, closed=False).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"{customer}'s Open Tickets"
            total = opentickets_count
            if period == "today":
                tickets = Ticket.objects.filter(customer__customer=customer, closed=False, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"Today's Open Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, closed=False, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(customer__customer=customer, closed=False, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Week's Open Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, closed=False, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(customer__customer=customer, closed=False, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Month's Open Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, closed=False, date__year=today.year, date__month=today.month).count()
        elif reports == "closedtickets":		
            tickets = Ticket.objects.filter(customer__customer=customer, closed=True).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = f"{customer}'s Closed Tickets"
            total = closedtickets_count
            if period == "today":
                tickets = Ticket.objects.filter(customer__customer=customer, closed=True, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"Today's Closed Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, closed=True, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(customer__customer=customer, closed=True, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Week's Closed Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, closed=True, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(customer__customer=customer, closed=True, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = f"This Month's Closed Tickets for {customer}"
                total = Ticket.objects.filter(customer__customer=customer, closed=True, date__year=today.year, date__month=today.month).count()            		
        return render(request, "helpdesk/customer_reports.html", {
	        "support": Dynamics.objects.get(id=4),
		    "title" : title,
            "total" : total,			
		    "tickets" : tickets,
		    "reports": reports,
		    "customer" : customer,
		    "alltickets_count" : alltickets_count,
		    "opentickets_count" : opentickets_count,
		    "closedtickets_count" : closedtickets_count
	    })
    else:	    
        return redirect('index')
		
		
def view_reports(request):
    if request.user.is_authenticated:
        user = request.session["_auth_user_id"]
        ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)
        seniors = Senior.objects.filter(senior=user)
	
        alltickets_count = Ticket.objects.filter().count()
        opentickets_count = Ticket.objects.filter(closed=False).count()
        closedtickets_count = Ticket.objects.filter(closed=True).count()
	
        useralltickets_count = Ticket.objects.filter(user=user).count()
        useropentickets_count = Ticket.objects.filter(user=user, closed=False).count()
        userclosedtickets_count = Ticket.objects.filter(user=user, closed=True).count()
	
        escalltickets_count = Ticket.objects.filter(user_id__in=seniors.values('junior_id')).count()
        escopentickets_count = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False).count()
        escclosedtickets_count = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True).count()	
        total = 0
        title = "Your Ticket Summary"
        total = useralltickets_count
        return render(request, "helpdesk/reports.html", {
	        "support": Dynamics.objects.get(id=4),
		    "title" : title,
		    "total" : total,
		    "alltickets_count" : alltickets_count,
		    "opentickets_count" : opentickets_count,
		    "closedtickets_count" : closedtickets_count,
		    "useralltickets_count" : useralltickets_count,
		    "useropentickets_count" : useropentickets_count,
		    "userclosedtickets_count" : userclosedtickets_count,
		    "escalltickets_count" : escalltickets_count,
		    "escopentickets_count" : escopentickets_count,
		    "escclosedtickets_count" : escclosedtickets_count
	    })
    else:	    
        return redirect('index')
		
@login_required
def reports(request, reports, period):
    if request.user.is_authenticated:
        user = request.session["_auth_user_id"]
        ticketranks = Ticketrank.objects.filter(ticket=OuterRef("id"), user_id=user)	
        seniors = Senior.objects.filter(senior=user)	
	
        alltickets_count = Ticket.objects.filter().count()
        opentickets_count = Ticket.objects.filter(closed=False).count()
        closedtickets_count = Ticket.objects.filter(closed=True).count()
	
        useralltickets_count = Ticket.objects.filter(user=user).count()
        useropentickets_count = Ticket.objects.filter(user=user, closed=False).count()
        userclosedtickets_count = Ticket.objects.filter(user=user, closed=True).count()
	
        escalltickets_count = Ticket.objects.filter(user_id__in=seniors.values('junior_id')).count()
        escopentickets_count = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False).count()
        escclosedtickets_count = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True).count()
	
        today = datetime.datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.datetime.combine(today, time())
        today_end = datetime.datetime.combine(tomorrow, time())
	
        today = datetime.datetime.today()
        one_week_ago = today - timedelta(days=7)
	
        title = "Your Tickets Summary"
        total = 0
        # Filter tickets returned based on reports
        if reports == "useralltickets":		
            tickets = Ticket.objects.filter(user=user).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = " Your Tickets"
            total = useralltickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user=user, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Today's Tickets"
                total = Ticket.objects.filter(user=user, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user=user, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Week's Tickets"
                total = Ticket.objects.filter(user=user, date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(user=user, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Month's Tickets"
                total = Ticket.objects.filter(user=user, date__year=today.year, date__month=today.month).count()          
				
        elif reports == "useropentickets":
            tickets = Ticket.objects.filter(user=user, closed=False).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = "Your Open Tickets"
            total = useropentickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user=user, closed=False, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Today's Open Tickets"
                total = Ticket.objects.filter(user=user, closed=False, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user=user, closed=False, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Week's Open Tickets"
                total = Ticket.objects.filter(user=user, closed=False, date__gte=one_week_ago).count()
            elif period == "month":
                tickets = Ticket.objects.filter(user=user, closed=False, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Month's Open Tickets"
                total = Ticket.objects.filter(user=user, closed=False, date__year=today.year, date__month=today.month).count()
        elif reports == "userclosedtickets":
            tickets = Ticket.objects.filter(user=user, closed=True).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = "Your Closed Tickets"
            total = userclosedtickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user=user, closed=True, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Today's Closed Tickets"
                total = Ticket.objects.filter(user=user, closed=True, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user=user, closed=True, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Week's Closed Tickets"
                total = Ticket.objects.filter(user=user, closed=True, date__gte=one_week_ago).count()
            elif period == "month":
                tickets = Ticket.objects.filter(user=user, closed=True, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Your Month's Closed Tickets"
                total = Ticket.objects.filter(user=user, closed=True, date__year=today.year, date__month=today.month).count()
        elif reports == "escalltickets":		
            tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id')).order_by(
                "-date").annotate(current_ticketrank=Count(ticketranks.values('id')))
            title = " Escalated Tickets"
            total = escalltickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Today's Escalated Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "This Week's Escalated Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "This Month's Escalated Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), date__year=today.year, date__month=today.month).count()
        elif reports == "escopentickets":
            tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False).order_by(
                "-date").annotate(current_ticketrank=Count(ticketranks.values('id')))
            title = "Escalated Open Tickets"
            total = escopentickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Today's Escalated Open Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "This Week's Escalated Open Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False, date__gte=one_week_ago).count()
            elif period == "month":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "This Month's Escalated Open Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=False, date__year=today.year, date__month=today.month).count()
        elif reports == "escclosedtickets":
            tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True).order_by(
                "-date").annotate(current_ticketrank=Count(ticketranks.values('id')))
            title = "Escalated Closed Tickets"
            total = escclosedtickets_count
            if period == "today":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "Today's Escalated Closed Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "This Week's Escalated Closed Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True, date__gte=one_week_ago).count()
            elif period == "month":
                tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "This Month's Escalated Closed Tickets"
                total = Ticket.objects.filter(user_id__in=seniors.values('junior_id'), closed=True, date__year=today.year, date__month=today.month).count()
        elif reports == "alltickets":		
            tickets = Ticket.objects.filter().order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = "All Tickets"
            total = alltickets_count
            if period == "today":
                tickets = Ticket.objects.filter(date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All Today's Tickets"
                total = Ticket.objects.filter(date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All this Week's Tickets"
                total = Ticket.objects.filter(date__gte=one_week_ago).count
            elif period == "month":
                tickets = Ticket.objects.filter(date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All this Month's Tickets"
                total = Ticket.objects.filter(date__year=today.year, date__month=today.month).count()
        elif reports == "opentickets":
            tickets = Ticket.objects.filter(closed=False).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = "All Open Tickets"
            total = opentickets_count
            if period == "today":
                tickets = Ticket.objects.filter(closed=False, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All Today's Open Tickets"
                total = Ticket.objects.filter(closed=False, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(closed=False, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All this Week's Open Tickets"
                total = Ticket.objects.filter(closed=False, date__gte=one_week_ago).count()
            elif period == "month":
                tickets = Ticket.objects.filter(closed=False, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All this Month's Open Tickets"
                total = Ticket.objects.filter(closed=False, date__year=today.year, date__month=today.month).count()
        elif reports == "closedtickets":
            tickets = Ticket.objects.filter(closed=True).order_by("-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
            title = "All Closed Tickets"
            total = closedtickets_count
            if period == "today":
                tickets = Ticket.objects.filter(closed=True, date__lte=today_end, date__gte=today_start).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All Today's Closed Tickets"
                total = Ticket.objects.filter(closed=True, date__lte=today_end, date__gte=today_start).count()
            elif period == "week":
                tickets = Ticket.objects.filter(closed=True, date__gte=one_week_ago).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All this Week's Closed Tickets"
                total = Ticket.objects.filter(closed=True, date__gte=one_week_ago).count()
            elif period == "month":
                tickets = Ticket.objects.filter(closed=True, date__year=today.year, date__month=today.month).order_by(
			        "-date").annotate(current_ticketrank=Count(ticketranks.values("id")))
                title = "All this Month's Closed Tickets"
                total = Ticket.objects.filter(closed=True, date__year=today.year, date__month=today.month).count()
        elif reports == "summary":
	        total = useralltickets_count
	        title = "Your Tickets Summary"        
	        tickets = ""         	
        else:        
            return JsonResponse({"error": "Invalid report."}, status=400)       
        return render(request, "helpdesk/reports.html", {
	        "support": Dynamics.objects.get(id=4),
		    "tickets": tickets,
		    "title": title,
		    "total": total,
		    "reports": reports,
		    "alltickets_count" : alltickets_count,
		    "opentickets_count" : opentickets_count,
		    "closedtickets_count" : closedtickets_count,
		    "useralltickets_count" : useralltickets_count,
		    "useropentickets_count" : useropentickets_count,
            "userclosedtickets_count" : userclosedtickets_count,
            "escalltickets_count" : escalltickets_count,
            "escopentickets_count" : escopentickets_count,
            "escclosedtickets_count" : escclosedtickets_count
	    })
		
    else:	    
        return redirect('index')
	
def ticketrank(request, id):
    try:
        ticketrank_class = 'fas fa-bug'
        user = User.objects.get(id=request.session['_auth_user_id'])
        ticket = Ticket.objects.get(id=id)
        ticketrank = Ticketrank.objects.get_or_create(user=user, ticket=ticket)
        if not ticketrank[1]:
            ticketrank_class = 'fa fa-bug'
            Ticketrank.objects.filter(user=user, ticket=ticket).delete()

        total_ticketranks = Ticketrank.objects.filter(ticket=ticket).count()
        if total_ticketranks == 0:
            ticketrank_class = 'fa fa-desktop'
    except KeyError:
        return HttpResponseBadRequest("Bad Request: There is no ticketrank")
    return JsonResponse({
        "ticketrank": id, 
		"ticketrank_class": ticketrank_class, 
		"total_ticketranks": total_ticketranks
    }) 

def post_ticket(request):
    if request.method == "POST":
        form = NewPost(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.session['_auth_user_id'])
            customer = form.cleaned_data['customer']
            title = form.cleaned_data['title']
            text = form.cleaned_data["text"]
            image = form.cleaned_data['image']
            ticket = Ticket.objects.create(
                user=user,
                customer=customer,
                title=title,
                text=text,
                image=image
            ) 
            return HttpResponseRedirect(reverse("index"))     	
    else:
        return render(request, "helpdesk/index.html", {
            'ticket':ticket,
            'user':user,
            'message': 'The New ticket has been created successfully',
            'form': NewPost()            
        })	


def edit_ticket(request, id):
    if request.is_ajax and request.method == "POST":
        form = EditPost(request.POST)
        if form.is_valid():
            title = form.cleaned_data["edit_title"]
            text = form.cleaned_data["edit_text"]
            Ticket.objects.filter(
                id=id, user_id=request.session['_auth_user_id']).update(text=text)
            Ticket.objects.filter(
                id=id, user_id=request.session['_auth_user_id']).update(title=title)
            return JsonResponse({
            'result': 'ok',
            'title': title,
            'text': text})
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({
	    "error": HttpResponseBadRequest("Bad Request: Unable to edit ticket")}, 
		status=400
	)        
		
def add_image(request):
    if request.user.is_authenticated:     
        user = request.user      
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()
        if user.id is None:
            return redirect('login')		

        if request.method == 'GET':	    
            return render(request, "helpdesk/add_image.html", {
		        "picture": picture,
                "support": Dynamics.objects.get(id=4),
                "helpdesk": Dynamics.objects.get(id=2),
                "form": PictureForm()            
            })   
	
        else:    
            form = PictureForm(request.POST, request.FILES)
		
            if form.is_valid():               
                image = form.cleaned_data['image']
                imageCreated = Picture.objects.create( 
                    user=request.user,			
                    image=image
                )
                return render(request, "helpdesk/add_image.html",{
			        "form": form,
                    "picture": picture,
                    "support": Dynamics.objects.get(id=4),
                    "helpdesk": Dynamics.objects.get(id=2),
                    "imageCreated":imageCreated,
		            "message": "Image uploaded successfully"}) 
    else:
	    return redirect('index')


def ticket_view(request, ticket): 
    picture = Dynamics.objects.get(id=2)      
    if request.method == 'GET':     
        if request.user.id is None:            
            return HttpResponseRedirect(reverse("login"))   
    
        ticket = Ticket.objects.get(id=ticket)
        comments = ticket.comments.all().order_by('id').reverse()
        return render(request, 'helpdesk/ticket_view.html', {
            "ticket": ticket, 
            "picture": picture, 
            "support": Dynamics.objects.get(id=4),
            "troubleticket": Dynamics.objects.get(id=5),            
            "comments": comments            
        })  
        
    
def admin_ticket(request):
    if request.method == "POST":
        form = AdminTicket(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['user']
            customer = form.cleaned_data['customer']
            title = form.cleaned_data['title']
            text = form.cleaned_data["text"]
            image = form.cleaned_data['image']
            ticket = Ticket.objects.create(
                user=user,
                customer=customer,
                title=title,
                text=text,
                image=image
            ) 
            return HttpResponseRedirect(reverse("super"))     	
    else:
        return render(request, "helpdesk/super.html", {
            'ticket':ticket,
            'user':user,
            'message': 'The New ticket has been created successfully',
            'form': AdminTicket()            
        })
        
def admin_control(request, username): 
    profile_account = User.objects.get(username=username)  
    if request.method == 'GET':            
        updateform = UserAccessForm(instance=request.POST)   
    else:         
        updateform = UserAccessForm(request.POST)              
        access = request.POST["access"]
        profile_account.access = access
        profile_account.save()
    return HttpResponseRedirect(reverse("profile",args=(username,))) 
    
def profile_ticket(request, username):
    if request.method == "POST":
        form = NewPost(request.POST, request.FILES)
        if form.is_valid():
            profile_account = User.objects.get(username=username) 
            customer = form.cleaned_data['customer']            
            title = form.cleaned_data['title']
            text = form.cleaned_data["text"]
            image = form.cleaned_data['image']
            ticket = Ticket.objects.create(
                user=profile_account,
                customer=customer,
                title=title,
                text=text,
                image=image
            ) 
            return HttpResponseRedirect(reverse("profile",args=(username,)))     	
    else:
        return render(request, "helpdesk/profile.html", {
            'ticket':ticket,
            'profile_account':profile_account,
            'message': 'The New ticket has been created successfully',
            'form': NewPost()            
        })	       
        
def escalate(request):
    if request.user.is_authenticated:
        user = request.user      
        user_picture = User.objects.get(username=user)
        pictures = Picture.objects.filter(user=user_picture)
        pictures_count = pictures.count()
        if pictures_count == 0:
            picture = Dynamics.objects.get(id=1)
        else:
            picture = pictures.first()
        if request.user.is_authenticated:
            user = request.session['_auth_user_id']
            seniors = Senior.objects.filter(senior=user)
            ticketranks = Ticketrank.objects.filter(ticket=OuterRef('id'), user_id=user)
            tickets = Ticket.objects.filter(user_id__in=seniors.values('junior_id')).order_by(
                "-date").annotate(current_ticketrank=Count(ticketranks.values('id')))
        else:
            return HttpResponseRedirect(reverse("login"))

        paginator = Paginator(tickets, max_tickets)
        page_no = request.GET.get('page')
        ticket_items = paginator.get_page(page_no)
        return render(request, "helpdesk/escalate.html", {
            "tickets": ticket_items,
            "support": Dynamics.objects.get(id=4),
            "picture": picture,
            "form": NewPost()
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
def add_customer(request):    
    if request.method == "POST":
        form = AddCustomer(request.POST, request.FILES)
        if form.is_valid():            
            customer = form.cleaned_data['customer']
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data["phone_no"]
            company = form.cleaned_data['company']
            location = form.cleaned_data['location']
            new_customer = Customer.objects.create(
                customer=customer,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone_no=phone_no,
                company=company,
                location=location               
            ) 
            return HttpResponseRedirect(reverse("customer_view"))     	
    else:
        return render(request, "helpdesk/customers.html", {            
            'message': 'The new Customer has been registered successfully',
            'form': AddCustomer()            
        })	
    
    
def supervise(request, id):
    try:
        result = 'supervise'
        user = User.objects.get(id=request.session['_auth_user_id'])
        person = User.objects.get(id=id)
        senior = Senior.objects.get_or_create(senior=user, junior=person)
        if not senior[1]:
            Senior.objects.filter(senior=user, junior=person).delete()
            result = 'unsupervise'
        total_seniors = Senior.objects.filter(junior=person).count()
    except KeyError:
        return HttpResponseBadRequest("Bad Request: There are no supervisors")
    return JsonResponse({
	    "result": result, 
	    "total_seniors": total_seniors
	})



def supervisor(request, username):
    try:
        if request.method =="POST":      
            profile_account = User.objects.get(username=username)            
            escalate = User.objects.get( username = request.POST["username"])            
            supervisor = Senior.objects.get_or_create(senior=escalate, junior=profile_account)
            if not supervisor[1]:
                supervisor = Senior.objects.filter(senior=escalate, junior=profile_account).delete()
    except KeyError:
        return HttpResponseBadRequest("Bad Request: The user does not exist")
    return HttpResponseRedirect(reverse("profile",args=(username,))) 


def subordinate(request, username):
    try:
        if request.method =="POST":      
            profile_account = User.objects.get(username=username)            
            referer = User.objects.get( username = request.POST["username"])            
            subordinate = Senior.objects.get_or_create(senior=profile_account, junior=referer)
            if not subordinate[1]:
                subordinate = Senior.objects.filter(senior=profile_account, junior=referer).delete()
    except KeyError:
        return HttpResponseBadRequest("Bad Request: The user does not exist")
    return HttpResponseRedirect(reverse("profile",args=(username,))) 
    

def close_ticket(request, ticket):
    if request.method == 'GET':
        ticket_item = Ticket.objects.get(id=ticket)
        ticket_item.closed = True
        ticket_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))              
        
        
def add_comment(request, ticket):
    if request.method == 'POST':
        ticket = Ticket.objects.get(id=ticket)
        comment = request.POST['comment']
        if not comment:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        comment = Comment.objects.create(comment=comment, user=request.user)
        ticket.comments.add(comment)
        ticket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		
def delete_comment(request, comment):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment)
        comment.delete()
        return HttpResponse('success')

class NewPost(forms.ModelForm): 
    class Meta:  
        model = Ticket 
        fields = ('customer','title', 'text', 'image')
        widgets =  {'customer':forms.Select(attrs={'class' : 'form-control'}),       
                   'title': forms.TextInput(attrs={
                        'class': 'form-control', 'placeholder': 'Enter the ticket title here'}),
                   'text': forms.Textarea({
                       'rows': '3', 
		               'maxlength': 300, 
		               'class': 'form-control', 
		               'placeholder': 'Enter the ticket description here'
		           })
        }    
    
class AdminTicket(forms.ModelForm): 
    class Meta:  
        model = Ticket 
        fields = ('user','customer','title', 'text', 'image')
        widgets = {'user':forms.Select(attrs={'class' : 'form-control'}),
                   'customer':forms.Select(attrs={'class' : 'form-control'}),
                   'title': forms.TextInput(attrs={
                        'class': 'form-control', 'placeholder': 'Enter the ticket title here'}),
                   'text': forms.Textarea({
                       'rows': '3', 
		               'maxlength': 300, 
		               'class': 'form-control', 
		               'placeholder': 'Enter the ticket description here'
		           })
        }   

class AddCustomer(forms.ModelForm): 
    class Meta:  
        model = Customer 
        fields = ('__all__')
        widgets = {'customer': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Customer's Business name (Alias)" }),
                   'firstname': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Customer's Fisrtname"}),
                   'lastname': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Customer's Lastname"}), 
                   'email': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Customer's Email"}),
                   'phone_no': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Customer's Phone No."}),
                   'company': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Company name"}),
                   'location': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter Customer's Location"})
        }
class EditPost(forms.Form): 
    edit_title = forms.Field(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter the ticket title here',
        'id': 'edit_title'
        }), label="Ticket Title", required=True)
    edit_text = forms.Field(widget=forms.Textarea(
        {"rows": "3",
		"maxlength": 300, 
		"class": "form-control", 
		"placeholder": "Enter the ticket description here", 
		"id": "edit_text"
		}), label="New Ticket", required=True)
		
class PictureForm(forms.ModelForm):
    """Image Model Form for processing images"""
    class Meta:
        model = Picture        
        fields = ('image',)  

class UserAccessForm(forms.ModelForm):
    """Image Model Form for processing users access""" 
    class Meta:  
        model = User
        fields = ('access',)
        widgets = {'access': forms.Select(attrs={'class': 'custom-select md-form'})}
     