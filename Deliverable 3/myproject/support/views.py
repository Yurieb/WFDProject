from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SupportCaseForm, ResponseForm, FeedbackForm
from .models import SupportCase, Profile, Response, Feedback


def home(request):
    return render(request, 'home.html')

# Submit a new support case only accessible by logged-in users
@login_required
def submit_case(request):
    if request.method == 'POST':
        form = SupportCaseForm(request.POST)
        if form.is_valid():
            support_case = form.save(commit=False)
            support_case.customer = request.user
            support_case.save()
            return redirect('home')
    else:
        form = SupportCaseForm()
    return render(request, 'submit_case.html', {'form': form})

# User registration view creates a Customer profile by default
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='Customer')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Allow an agent to respond to an open case
@login_required
def add_response(request, case_id):
    if request.user.profile.role != 'Agent':
        raise PermissionDenied("Only agents can respond to cases.")

    case = get_object_or_404(SupportCase, id=case_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.agent = request.user
            response.case = case
            response.save()
            case.status = 'closed'
            case.save()
            return redirect('case_list')
    else:
        form = ResponseForm()
    return render(request, 'response_form.html', {'form': form, 'case': case})

# Allow a customer to give feedback after the case is closed
@login_required
def give_feedback(request, case_id):
    case = get_object_or_404(SupportCase, id=case_id)
    if request.user.profile.role != 'Customer' or case.customer != request.user:
        raise PermissionDenied("Only the customer who submitted this case can give feedback.")
    if case.status != 'closed':
        raise PermissionDenied("You can only give feedback after the case is closed.")

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.case = case
            feedback.save()
            return redirect('case_list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form, 'case': case})

# Manager dashboard view
@login_required
def manager_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Manager':
        raise PermissionDenied("Only managers can view this page.")

    cases = SupportCase.objects.all().order_by('-created_at')
    agents = Profile.objects.filter(role='Agent')

    return render(request, 'manager_dashboard.html', {'cases': cases, 'agents': agents})

# Manager assigns an agent to a support case
@login_required
def assign_agent(request, case_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Manager':
        raise PermissionDenied("Only managers can assign agents.")

    case = get_object_or_404(SupportCase, id=case_id)

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(User, id=agent_id)
        case.agent = agent
        case.save()
        return redirect('manager_dashboard')

    return redirect('manager_dashboard')

@login_required
def case_list(request):
    cases = SupportCase.objects.all()
    return render(request, 'case_list.html', {'cases': cases})

@login_required
def case_list(request):
    user = request.user
    role = user.profile.role

    if role == 'Customer':
        cases = SupportCase.objects.filter(customer=user)
    elif role == 'Agent':
        cases = SupportCase.objects.filter(agent=user)
    elif role == 'Manager':
        cases = SupportCase.objects.all()
    else:
        cases = SupportCase.objects.none()

    return render(request, 'case_list.html', {'cases': cases})


