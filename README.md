CaseKart – Retail Customer Support

Overview:
CaseKart is a customer support sytem built with Django it is designed specifically for retail settings. It allows customers to report issues such as a size being to small wrong item being sent.The agents respond to them, and managers to oversee the process. 
It way designed around the Customer Support (Customers – Cases) use case in mind, shows secure authentication, role-based access control, and organized interactions between users with different roles.The user frendly UI shows a ready  production-ready support solution suitable for real-world deployment. 

Live Demo
You can try the project live here:
https://Yurie90.pythonanywhere.com


Use these logins to test different roles:
Role	  Username	Password
Customer	Yurie   Django15
Agent	    Paul  	Django15
Manager	  Adam   	Django15
Admin	    admin_user   Django15

Log In using one of the sample accounts:
Customer: Submit a new case right your issue then submit the case will be open. After an agent replies you can come back and leave feedback.

Agent: View assigned cases and write a response to a customer. The case will then close.

Manager: Assign open cases to differnt agents.

Admin :Manage all models: users, support cases, responses, feedback, and roles.


How to setup Instructions (Local):
Clone the project like this
git clone https://github.com/Yurieb/WFDProject.git
cd WFDProject/Deliverable\ 3/myproject

Create a virtual environment:
python -m venv env
source env/bin/activate
or
env\Scripts\activate

Install the required packages:
pip install -r requirements.txt

Apply migrations:
py manage.py makemigrations
py manage.py migrate

Creating a Superuser (Admin):
python manage.py createsuperuser

Run the server:
py manage.py runserver
Open your browser and past this :
http://127.0.0.1:8000/


What is being tested:
Case Submission
Verifies that a logged-in customer can submit a new support case successfully.

Agent Assignment
Checks that a manager can assign an agent to an open support case using the dashboard.

Case Response by Agent
Confirms that when an agent responds to a case, the system records the response and automatically marks the case as closed.

Customer Feedback
Ensures that customers can leave feedback rating and comments after the case is closed.
