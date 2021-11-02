# CS50 - Final Project - Helpdesk Application

The project is a Helpdesk application (Helpdesk dynamics) where staff of an organization can raise and assign job/trouble tickets to themselves or to a fellow staff of the same organization based on their roles and the level of access. It is a customer service application where the users create, organize, track as well as monitor job tickets for their customers until they are resolved and closed.

Technologies used:

- Python
- Django
- JavaScript
- HTML
- CSS
- sqlite3
- BootStrap4x
- other small libraries or packages(see file "requirements.txt")

## How the application works?

The idea is simple. A new staff of the organization (user) registers in the application with his/her username, email and password. After the initial registration, the user is required to update the following fields:

- Firstname
- Lastname
- Role
- Location
- Image(profile picture)

### Access Levels

There are three Access Levels for users in the application (Regular, Standard and Admin). All new users automatically are registered as "Regular" with limited access. Standard users have more access than Regular, while Admin has the highest privilege. 

An initial user account that is required to grant or change other user's access to privileged access after registration is "support" (It is being shipped with the application). The log-in credential are as follows:

- Username: support
- Password: helpdesk

The Three levels of Access are described below:

1. Regular: Regular users can raise and assign job tickets to themselves or to any escalated user that must have been escalated to them by Admin as their subordinate. They can only track and update job tickets raised by themselves or their subordinates.

2. Standard: Standard users can raise and assign job tickets to themselves, to specified escalated users that must have been escalated to them by Admin as their subordinate as well as all other users in the organization. They can track and update all job tickets raised by themselves, their subordinates and all other users.

3. Admin: The Admin has all the privileges of the Standard or Regular users and in addition, can supervise any user he wishes to supervise (escalated user). Admin has the right to make other users as supervisors or subordinates to a supervisor. He can also change access levels of any user to either Regular, Standard or Admin. 

### **Files:**

The following is the file structure of the project that were created or modified. Default project files are omitted.

```
/ (folder)
-- (files)

/optidesk - main project folder
 --README.md - this file - description of the project
 --db.sqlite3 - sqlite database file of the project 
 --requirements.txt - list of libraries needed to run
  /optidesk - Django main project folder   
   --settings.py - slightly modified settings (mostly to for static files)
   --urls.py - url paths configuration   
  /helpdesk - Django helpdesk app
    /migrations - migrated files update from app's database
    /static - static files used in the app are located here
      /helpdesk - folder housing static files
       --main.js - JavaScript commands used for manipulating the DOM
       --styles.css - CSS styles sheet for styling the templates
    /templates - template files used in the app are located here
      /helpdesk - folder housing template files
       --layout.html - page that displays the layout of the app's templates
       --index.html - main home page of the app
       --register.html - page for registering new users into the app
       --login.html - login page for granting access to a user
       --account.html - page for updating user's account details
       --add_image.html - page for uploading user's profile image
       --admin_control.html - an included feature that allows for the updating of user access levels by admins
       --adminticket_form.html - an included feature that allows for the assigning of tickets to any user
       --customers.html - page for viewing all registered customers
       --edit_customer.html - page for updating customer's details
       --escalate.html - page for viewing all escalated user's tickets
       --personel.html - an included feature for accessing all users
       --post_form.html - an included feature for raising and assigning tickets
       --profile.html - page for viewing and updating user's profile
       --profile_account.html - an included feature for granting access privilages on user's profiles
       --profile_picture.html - an included feature for viewing user's profile image, full name, email and role
       --profile_ticket.html - an included feature for assigning tickets to users on their profiles
       --subordinate.html - an included feature for assigning a subordinate to a user by admin
       --supervisor.html - an included feature for assigning a supervisor to a user by admin
       --super.html - page for viewing all tickets raised and for accessing all user and customer profiles
       --ticket_view.html - page for viewing and updating job tickets
       --users.html - page for viewing all registered users
   --admin.py - admin settings for model view (app tables)   
   --models.py - database models   
   --urls.py - all standard HTTP requests routing are handled here
   --views.py - definition of the app url & form functions are handled here
  /media - Django media files folder
    /images - folder for keeping image files   
  
```

---

### Application pages

- Index: User's dashboard for raising personalized job tickets.
- Profile: User's profile for assigning job tickets to specific users and updating their access (By Admin) and profile details.
- Escalated Tickets: Page for tracking and updating escalated users tickets.
- Ticket Reports: Page for viewing and querying support tickets.
- Super Access: Page accessible to only Standard and Admin users for assigning and tracking job tickets for any user. Also a route where access of other users are being updated by Admin 

## How to launch application

1. Download the distribution code into your system
2. Check that Django and all requirements are installed
3. In your terminal, cd into the project directory
4. Run "python manage.py runservser" to start the server
5. In your browser go to `http://127.0.0.1:8000/`
6. You are ready to go!

## Distinctiveness and Complexity

- The web application is mobile responsive
- The web application has a provison for the raising of job tickets and assigning same to another user to execute. This feature is not available in other projects.
- There are provisions for adding, viewing and updating both customers and registered users details that are lacking in other projects.  
- The website is distinctive from other websites of other projects due to its ability to handle customer's jobs via the raising and tracking of job tickets.
- The website is also complex because it has various controls that allows for registering new customers and updating their tickets, granting various access privileges to users and other important features. 


:computer: &nbsp; **View Course [here](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)**

:arrow_forward: &nbsp; **View Live Demo [here](https://youtu.be/sv8WnFp1fuA)**

:spider_web: &nbsp; **View Demo Website [here](https://helpdeskdynamics.azurewebsites.net)**

