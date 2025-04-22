from django.shortcuts import render, redirect
from .forms import SupportCaseForm
from .models import SupportCase

# View for Homepage
def home(request):
    return render(request, 'home.html')

# View for submitting a new support case
def submit_case(request):
    if request.method == 'POST':
        form = SupportCaseForm(request.POST)
        if form.is_valid():
            support_case = form.save(commit=False)
            # Link it to the logged-in customer 
            support_case.customer_id = 1  # TEMP: set to ID 1 for now
            support_case.save()
            return redirect('home')  # Redirect after submitting
    else:
        form = SupportCaseForm()

    return render(request, 'submit_case.html', {'form': form})

# View for listing all submitted cases
def case_list(request):
    cases = SupportCase.objects.all()
    return render(request, 'case_list.html', {'cases': cases})

