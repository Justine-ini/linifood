from django.shortcuts import render, redirect

from orders.models import Order
from .forms import UserForm
from .models import User, UserProfile
from .utils import detectUser #send_verification_email, send_password_reset_email
from vendor.forms import VendorForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify




from django.core.exceptions import PermissionDenied


from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import login

from vendor.models import Vendor



# Create your views here.
# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied
  
# Restrict the customer from accessing the vendor page
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied
  



# def registerUser(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "You are already logged in.")
#         return redirect("myAccount")

#     form = UserForm()  # Ensure form is initialized

#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             username = form.cleaned_data["username"]
#             email = form.cleaned_data["email"]
#             password = form.cleaned_data["password"]

#             # Create a new user with proper password hashing
#             user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#             user.first_name = first_name
#             user.last_name = last_name
#             user.save()  # Save user data after setting attributes

#             # Send a welcome email
#             try:
#                 send_mail(
#                     subject='Welcome to Your Account!',
#                     message=f'''
#                         Hi {user.first_name},

#                         Thank you for registering with our website!

#                         You can now log in to your account using your email address and password.

#                         Best regards,

#                         The Team
#                     ''',
#                     from_email='inijustine4040@gmail.com',  # Replace with your email address
#                     recipient_list=[email],  # Replace with dynamic recipient list if needed
#                 )
#                 messages.success(request, "Your account has been registered successfully. A welcome email has been sent to your inbox.")
#             except Exception as e:
#                 messages.error(request, f"An error occurred while sending the welcome email: {e}")

#             # Log in the newly created user (optional)
#             # login(request, user)

#             return redirect("login")  # Redirect to login page after registration
#         else:
#             messages.error(request, "Please correct the errors in the form.")
#             print(form.errors)

#     context = {'form': form}  # Pass form to template for rendering
#     return render(request, 'accounts/registerUser.html', context)
  

# Method 2 original function
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()

            # Send verification email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)
    
#   # Method 2
#   # if request.method == "POST":
#   #   form = UserForm(request.POST)
#   #   if form.is_valid():
#   #     password = form.cleaned_data['password']
#   #     user = form.save(commit=False)
#   #     user.set_password(password)
#   #     user.role = User.CUSTOMER
#   #     user.save()
#   #     messages.success(request, "Your Account has been Registered Successfully")
#   #     return redirect("registerUser")
#   #   else:
#   #    print("Invalid form")
#   #    print(form.errors)
    
#   else:
#     form = UserForm()
#   context = {
#     "form" : form
#   }
#   return render(request, "accounts/registerUser.html", context)



def registerVendor(request):
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in ")
    return redirect("myAccount")
  elif request.method == "POST":
    # Store the data and create the user
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST, request.FILES) # The request.FILES must be added whenever there's files in the form
    if form.is_valid() and v_form.is_valid():
      first_name = form.cleaned_data["first_name"]
      last_name = form.cleaned_data["last_name"]
      username = form.cleaned_data["username"]
      email = form.cleaned_data["email"]
      password = form.cleaned_data["password"]

      user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,  username=username, password=password)
      user.role = User.VENDOR
      user.save()
      vendor = v_form.save(commit=False)
      vendor.user = user
      vendor_name = v_form.cleaned_data["vendor_name"]
      vendor.vendor_slug = slugify(vendor_name)+"-"+str(user.id)
      user_profile = UserProfile.objects.get(user=user)
      vendor.user_profile = user_profile
      vendor.save()
      # send verification email
      # send_verification_email(request, user)
      messages.success(request, "Your Account has been Registered Successfully! Please wait for Approval")
      return redirect("registerVendor")
    else:
      print("Invalid form")
      print(form.errors)

  else:
    form = UserForm()
    v_form = VendorForm()

  context = {
    "form" : form,
    "v_form": v_form
  }
  return render(request, "accounts/registerVendor.html", context)
  
def activate(request, uidb64, token):
  # Activate the user by setting the is_active status to true
  return


def login(request):
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in ")
    return redirect("myAccount")
  elif request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = auth.authenticate(email=email, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, "Login Successfull")
      return redirect("myAccount")
    else:
      messages.error(request, "Invalid login credentials")
      return redirect("login")
  return render(request, "accounts/login.html")


def logout(request):
  auth.logout(request)
  messages.info(request, "You are logged out")
  return redirect("login")


@login_required(login_url="login")
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url="login")
@user_passes_test(check_role_customer)
def custDashboard(request):
  orders = Order.objects.filter(user=request.user, is_ordered=True)
  recent_orders = orders[:5]
  context = {
    "orders": orders,
    "orders_count": orders.count(),
    "recent_orders": recent_orders,
  }
  return render(request, "accounts/custDashboard.html", context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  return render(request, "accounts/vendorDashboard.html")

def forgot_password(request):
  if request.method == "POST":
    email = request.POST["email"]

    if User.objects.filter(email=email).exist():
      user = User.objects.get(email__exact= email)

      # send reset password email
      # send_password_reset_email(request, user)

      messages.success(request, "Password reset have been sent to your email address")
      return redirect("login")
    else:
      messages.error(request, "Account does not exist")
      return redirect("forgot_password")

  return render(request, 'accounts/forgot_password.html')

def reset_password(request):
  if request.method == "POST":
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    if password == confirm_password:
      pk = request.session.get("uid")
      user = User.objects.get(pk=pk)
      user.set_password(password)
      user.is_active=True
      user.save()
      messages.success(request, "Password reset successfull")
      return redirect("login")
      
    else:
      messages.error(request, "Password do not match")
      return redirect("reset_password")
  
  return render(request, 'accounts/reset_password.html')

def reset_password_validate(request, uidb64, token):
  # Validate the user by decoding the token and user pk

  return 