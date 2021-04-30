import random
import string
from django.contrib.auth.models import User

def generate_unique_username():
    random_userid = "".join(random.sample(string.ascii_lowercase, 8))
    # check if already user exists
    users = User.objects.filter(username=random_userid).count()
    if(users > 0):
        return generate_unique_username()
    else:
        return random_userid

def generate_pin():
    random_pin = "".join(random.sample(string.digits, 6))
    return random_pin
