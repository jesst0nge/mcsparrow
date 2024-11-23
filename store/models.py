from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import inventory

# Create Customer Profile
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	

	def __str__(self):
		return self.user.username

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)

class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    value = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.00 for 10%
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.value}%"



class Giftcard(models.Model):
    gift_card_code = models.CharField(max_length=25, default='123', blank=True, null=True)
    gift_card_balance = models.DecimalField(default=0.05, decimal_places=2, max_digits=6)
    remaining_balance = models.DecimalField(default=0.07, decimal_places=2, max_digits=6)
    gift_name = models.CharField(max_length=25, default='Customer', blank=True, null=True)

    def __str__(self):
        return self.gift_card_code
