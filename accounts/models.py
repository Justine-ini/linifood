from django.db import models  # Importing the models module from Django to define database models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # Importing the necessary classes for user authentication from Django
from django.db.models.fields.related import ForeignKey, OneToOneField
# Create your models here.

class UserManager(BaseUserManager):  # Creating a custom user manager class inheriting from BaseUserManager
  def create_user(self, first_name, last_name, username, email, password=None):  # Method to create a standard user
    if not email:  # If email is not provided
      raise ValueError("User must have an email address")  # Raise an error
    if not username:  # If username is not provided
      raise ValueError("User must have a username")  # Raise an error
    
    user = self.model(  # Create a new user instance
      email=self.normalize_email(email),  # Normalize email address
      username=username,
      first_name=first_name,
      last_name=last_name,
    )
    
    user.set_password(password)  # Set the password for the user
    user.save(using=self._db)  # Save the user to the database
    return user  # Return the created user object
  
  def create_superuser(self, first_name, last_name, username, email, password=None):  # Method to create a superuser
    user = self.create_user(  # Create a user using the create_user method defined above
      email=self.normalize_email(email),  # Normalize email address
      username=username,
      password=password,
      first_name=first_name,
      last_name=last_name,
    )
    user.is_admin = True  # Set user as admin
    user.is_active = True  # Set user as active
    user.is_staff = True  # Set user as staff
    user.is_superadmin = True  # Set user as super admin
    user.save(using=self._db)  # Save the user to the database
    return user  # Return the created user object

class User(AbstractBaseUser):  # Custom user model inheriting from AbstractBaseUser
  VENDOR = 1  # Constant representing a vendor user
  CUSTOMER = 2  # Constant representing a customer user

  ROLE_CHOICE = (  # Tuple containing choices for user role
    (VENDOR, "vendor"),  # Choice for vendor user
    (CUSTOMER, "customer")  # Choice for customer user
  )
  first_name = models.CharField(max_length=50)  # Field for user's first name
  last_name = models.CharField(max_length=50)  # Field for user's last name
  username = models.CharField(max_length=50, unique=True)  # Field for user's username, must be unique
  email = models.EmailField(max_length=100, unique=True)  # Field for user's email, must be unique
  phone_number = models.CharField(max_length=15, blank=True)  # Field for user's phone number, optional
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)  # Field for user's role

  # Required fields
  date_joined = models.DateTimeField(auto_now_add=True)  # Field for the date the user joined
  last_login = models.DateTimeField(auto_now_add=True)  # Field for the last login date
  date_created = models.DateTimeField(auto_now_add=True)  # Field for the date the user was created
  modified_date = models.DateTimeField(auto_now=True)  # Field for the last modification date
  is_admin = models.BooleanField(default=False)  # Field indicating if user is an admin
  is_staff = models.BooleanField(default=False)  # Field indicating if user is staff
  is_active = models.BooleanField(default=True)  # Field indicating if user is active
  is_superadmin = models.BooleanField(default=False)  # Field indicating if user is a super admin

  objects = UserManager()  # Manager for this user model

  # Authentication
  USERNAME_FIELD = "email"  # Field to be used for authentication
  REQUIRED_FIELDS = ["username", "first_name", "last_name"]  # Required fields for user creation

  def __str__(self):  # String representation of the user object
    return self.email
  
  def has_perm(self, perm, obj=None):  # Method to check if user has a permission
    return self.is_admin  # Returning if the user is an admin or not
  
  def has_module_perms(self, app_label):  # Method to check if user has permissions for a given module
    return True  # All users have permission for any module
  
  def get_role(self):
    if self.role == 1:
      user_role = "vendor"
    elif self.role == 2:
      user_role = "customer"
    return user_role


'''
This code defines a custom user model (User) and a custom user manager (UserManager) using Django's authentication system. The User model inherits from AbstractBaseUser, allowing customization of user authentication in Django projects. The UserManager provides methods for creating both standard users and superusers. The User model includes fields for standard user information such as first name, last name, username, email, phone number, and role. It also includes fields related to authentication and permissions such as date joined, last login, admin status, staff status, and active status. Additionally, it defines methods for checking permissions.
'''

class UserProfile(models.Model):  # Define a model named UserProfile to store additional user profile information
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)  # Establish a one-to-one relationship with the User model, deleting this profile if the associated user is deleted
  profile_picture = models.ImageField(upload_to="users/profile_pictures", blank=True, null=True)  # Field to store the user's profile picture, allowing blank entries
  cover_photo = models.ImageField(upload_to="users/cover_photos", blank=True, null=True)  # Field to store the user's cover photo, allowing blank entries
  address = models.CharField(max_length=250, blank=True, null=True)  # Field to store the user's address line 1, allowing blank entries

  country = models.CharField(max_length=20, blank=True, null=True)  # Field to store the user's country, allowing blank entries
  state = models.CharField(max_length=20, blank=True, null=True)  # Field to store the user's state, allowing blank entries
  city = models.CharField(max_length=20, blank=True, null=True)  # Field to store the user's city, allowing blank entries
  pin_code = models.CharField(max_length=6, blank=True, null=True)  # Field to store the user's pin code, allowing blank entries
  latitude = models.CharField(max_length=20, blank=True, null=True)  # Field to store the user's latitude, allowing blank entries
  longitude = models.CharField(max_length=20, blank=True, null=True)  # Field to store the user's longitude, allowing blank entries
  created_at = models.DateTimeField(auto_now_add=True)  # Field to automatically store the date and time when this profile was created
  modified = models.DateTimeField(auto_now=True)  # Field to automatically store the date and time when this profile was last modified

  def __str__(self):  # Define how this object is represented as a string
    return self.user.email  # Return the email address of the associated user as the string representation

  # def full_address(self):
  #   return f"{self.address_line1}, {self.address_line2} "

'''
This code defines a Django model named UserProfile. It contains fields to store various details about a user's profile, including their profile picture, cover photo, address, location, and timestamps for creation and modification. The user field establishes a one-to-one relationship with the User model, linking each user to their profile. The __str__ method is overridden to return the email address of the associated user, providing a readable representation of the UserProfile object.
'''

