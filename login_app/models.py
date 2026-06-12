from django.db import models
import re ,bcrypt
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self , postData):
        errors = {}
        #check the first_name , last_name > 2 and only letters
        if len(postData.get('first_name' , '').strip()) < 2 :
            errors['first_name'] = 'first name must be at least 2 character long!'
        elif not postData.get('first_name' , '').strip().isalpha():
            errors['first_name'] = 'first name should contain letter only'

        if  len(postData.get('last_name' , '').strip()) < 2:
            errors['last_name'] = 'last name must be at least 2 character long!'
        elif not postData.get('last_name' , '').strip().isalpha():
            errors['last_name'] = 'last name should contain letter only'

        # Check format for email
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', postData.get('email', '')):
            errors['email'] = "Invalid email format!"

        # Check uniqueness for email
        elif User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists!"
                
        #check password
        if len(postData.get('password', '')) < 8:
            errors['password'] = 'Password must be at least 8 characters!'
        elif postData.get('password') != postData.get('confirm_pw'):
            errors['password'] = 'Passwords do not match!'

        return errors
        
    def login_validator(self, postData):
        errors = {}
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if not re.match(email_regex, postData.get('email', '')):
            errors['email'] = 'Please enter a valid email address.'
        else:
            user = self.filter(email=postData.get('email', ''))
            if not user:
                errors['email'] = 'Invalid email or password!'
            elif not bcrypt.checkpw(postData.get('password', '').encode(), user[0].password.encode()):
                errors['password'] = 'Invalid email or password!'
        return errors
                
    def create_user(self, postData):
        hash_pw = bcrypt.hashpw(postData.get('password', '').encode(), bcrypt.gensalt()).decode()
        return User.objects.create(
            first_name = postData.get('first_name', ''),
            last_name = postData.get('last_name', ''),
            email = postData.get('email', ''),
            password = hash_pw,
        )

class User(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    email = models.EmailField(max_length= 255)
    password = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager() 

        
    