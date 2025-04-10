from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,LoginForm,ProfileUpdateForm, ApplicationForm
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate,logout,login as auth_login
from .models import user_profile,custom_user, Application
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,"index.html")

def home(request):
    return render(request,"home.html")

def User_application(request):
    return render(request,"application_form.html")

def User_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  
        else:
            messages.error(request, "Registration failed! Please check your details.")
    else:
        form = UserCreationForm()

    return render(request, "registration.html", {"form": form}) 


def user_login(request):  
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = custom_user.objects.get(email=username_or_email)
                username = user.username
            except custom_user.DoesNotExist:
                username = username_or_email

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)   
                messages.success(request, "Login Successful!")
                return redirect('profile')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})  

from .models import InternshipList


# def internship_list_view(request):
#     internships = InternshipList.objects.all()
#     return render(request, 'list.html', {'internships': internships})

def internship_list_view(request):
    internships = InternshipList.objects.all()

    # Get distinct values for dropdown filters
    roles = InternshipList.objects.values_list('role', flat=True).distinct()
    locations = InternshipList.objects.values_list('location', flat=True).distinct()
    work_hours = InternshipList.objects.values_list('work_hours', flat=True).distinct()

    context = {
        'internships': internships,
        'roles': roles,
        'locations': locations,
        'work_hours': work_hours
    }

    return render(request, 'list.html',  context)


def user_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully!")
    return redirect('login')


from django.db import IntegrityError

@login_required(login_url='/login')
def profile_form(request):
    # Get the user's profile or create one only if it doesn't exist
    profile = user_profile.objects.filter(user=request.user).first()
    
    if not profile:
        try:
            profile = user_profile.objects.create(user=request.user)
        except IntegrityError:
            messages.error(request, "Error creating profile. Please try again.")
            return redirect('profile')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Ensure contact_number is not an empty string
            if form.cleaned_data.get("contact_number") == '':
                form.instance.contact_number = None  # Avoid duplicate empty entries

            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please check the details.")
    else:
        form = ProfileUpdateForm(instance=profile)  

    return render(request, 'profile_form.html', {'form': form, 'profile': profile})



@login_required
def profile_view(request):
    try:
        profile, created = user_profile.objects.get_or_create(user=request.user)

        # If a new profile is created, inform the user
        if created:
            messages.info(request, "Your profile has been created. Please update your details. And reload the page")

    except Exception as e:
        messages.error(request, f"An error occurred while fetching your profile: {str(e)}")
        profile = None

    applications = Application.objects.filter(user=request.user)

    if request.method == 'POST' and 'profile_picture' in request.FILES:
        try:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, "Profile picture updated successfully! reload the page")
        except Exception as e:
            messages.error(request, f"Failed to update profile picture: {str(e)}")
        return redirect('profile')

    # If no applications, show an info message
    if not applications:
        messages.info(request, "You have not applied for any internships yet.")

    return render(request, 'profile.html', {'profile': profile, 'applications': applications})

# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import UsernameUpdateForm

@login_required
def update_username(request):
    if request.method == "POST":
        form = UsernameUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to the profile page after update
    else:
        form = UsernameUpdateForm(instance=request.user)

    return render(request, "update_username.html", {"form": form})
    
@login_required
def apply_internship(request):
    form = ApplicationForm()
    if request.method == "POST":
        print("POST Data Received:", request.POST)  # Debugging line

        phone = request.POST.get('phone', '').strip()
        # Validate phone number length
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone number must be exactly 10 digits.")
            form = ApplicationForm(request.POST, request.FILES)  # Preserve entered data
            return render(request, 'application_form.html', {"form": form})

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        preferred_technology = request.POST.get('preferred_technology')
        company_name = request.POST.get('company_name')
        linkedin = request.POST.get('linkedin')
        github = request.POST.get('github')
        internship_role = request.POST.get('internship_role')
        position = request.POST.get('position')
        resume = request.FILES.get('resume')
        certificates = request.FILES.get('certificates')
        applied_on = request.POST.get('applied_on')


        # Check if user has already applied for two internships
        if request.user.applications.count() >= 4:
            messages.error(request, "Single user can only apply for 4 internships.")
            form = ApplicationForm(request.POST, request.FILES) 
            return redirect('apply_internship')  # Redirect back to the form

        # Save to database
        application = Application.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            skills=skills,
            experience=experience,
            preferred_technology=preferred_technology,
            company_name=company_name,
            linkedin=linkedin,
            github=github,
            internship_role=internship_role,
            position=position,
            resume=resume,
            certificates=certificates,
            applied_on=applied_on,
        )
        application.save()
        messages.success(request, "Application submitted successfully!")
        return redirect('profile')  # Redirect to profile page

    return render(request, 'application_form.html', {"form": form})


@login_required
def quit_application(request, application_id):
    try:
        application = Application.objects.get(id=application_id, user=request.user)
        application.delete()
        messages.success(request, "You have successfully quit the application. Reload the page")
    except Application.DoesNotExist:
        messages.error(request, "Application not found.")
    except Exception as e:
        messages.error(request, f"An error occurred while quitting the application: {str(e)}")
    
    return redirect("profile")