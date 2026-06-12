from django.db import models
from login_app.models import User

# Create your models here.
class BookManager(models.Manager):
    def basic_validator(self , postData):
        errors ={}
        if len(postData.get('title' , '').strip()) ==  0:
            errors['title'] = 'title is required!'
        if len(postData.get('description' , '').strip()) < 5:
            errors['description'] = 'description must be at least 5 characters!'
        return errors
    
    def create_book(self, postData):
        user_id = postData.get('user_id')
        try:
            uploader = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User not found")

        new_book = self.create(
            title=postData.get('title', '').strip(),
            description=postData.get('description', '').strip(),
            uploaded_by=uploader
        )
        
        new_book.users_who_like.add(uploader)
        return new_book


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = "books_uploaded", on_delete = models.CASCADE) # the user who uploaded a given book
    users_who_like = models.ManyToManyField(User, related_name = "liked_books") # a list of users who like a given book
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = BookManager()