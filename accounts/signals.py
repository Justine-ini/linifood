from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile
# from .utils import send_verification_email





@receiver(post_save, sender=User)  # Decorator to register a receiver function for the post_save signal of the User model
def post_save_create_profile_receiver(sender, instance, created, **kwargs):  # Signal handler function for post_save signal
  if created:  # Check if a new instance of User was created
    UserProfile.objects.create(user=instance)  # Create a UserProfile instance associated with the newly created User instance

    
  else:  # If the User instance was not newly created
    try:  # Try to fetch an existing UserProfile instance associated with the User
      profile = UserProfile.objects.get(user=instance)
      profile.save()  # Save the UserProfile instance to update it
    except UserProfile.DoesNotExist:  # If no UserProfile instance is found for the User
      # Create the user profile if it does not exist
      UserProfile.objects.create(user=instance)
 
'''
In summary, this signal handler function ensures that whenever a new User instance is created, either a new UserProfile instance is created if the User is newly created, or the existing UserProfile instance is updated if it already exists. This helps maintain consistency in the application's data structure by ensuring that each User has a corresponding profile immediately upon creation.
'''

# PRE-SAVE
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
  pass
# Another way to write it
#post_save.connect(post_save_create_profile_receiver, sender=User)


# @receiver(post_save, sender=User)
# def send_user_verification_email(sender, instance, created, **kwargs):
#     if created:
#         send_verification_email(user=instance)