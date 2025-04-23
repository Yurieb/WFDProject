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


@login_required
def case_list(request):
    cases = SupportCase.objects.all()
    return render(request, 'case_list.html', {'cases': cases})


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

@login_required
def manager_dashboard(request):
    if not request.user.profile.role == 'Manager':
        raise PermissionDenied("Only managers can access this page.")
    
    cases = SupportCase.objects.all().order_by('-created_at')
    return render(request, 'manager_dashboard.html', {'cases': cases})

@login_required
def assign_agent(request, case_id):
    if not request.user.profile.role == 'Manager':
        raise PermissionDenied("Only managers can assign agents.")

    case = SupportCase.objects.get(id=case_id)
    agents = User.objects.filter(profile__role='Agent')

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        selected_agent = User.objects.get(id=agent_id)
        case.agent = selected_agent
        case.save()
        return redirect('manager_dashboard')
    
    return render(request, 'assign_agent.html', {'case': case, 'agents': agents})

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


