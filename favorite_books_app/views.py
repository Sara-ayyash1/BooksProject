from django.shortcuts import render , redirect
from login_app.models import User
from .models import *
from django.contrib import messages
# Create your views here.

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user , 
        'all_books' : Book.objects.all() , 

    }
    return render(request , 'books.html' , context)

def create_book(request):
    if request.method == 'POST':
        if 'user_id' not in request.session:
           return redirect('/')
        
        errors = Book.objects.basic_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')

        Book.objects.create_book(request.POST)
        return redirect('/books')
    return redirect('/books')

def book_detail(request , book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('/books')
    
    context = {
        'book' : book,
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request , 'book_detail.html' , context)


def favorite_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('/books')

    user = User.objects.get(id=request.session['user_id'])
    book.users_who_like.add(user)
    
    # Redirect back to the page the user came from (either Main Page or Book Details)
    # If the referrer header is missing, safely default to the main '/books' page
    return redirect(request.META.get('HTTP_REFERER', '/books'))



def unfavorite_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('/books')

    user = User.objects.get(id=request.session['user_id'])
    book.users_who_like.remove(user)
    
    return redirect(request.META.get('HTTP_REFERER', '/books'))



def delete_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    try:
        book_to_delete = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('/books')
    
    # حماية أمنية: التحقق من أن المستخدم الحالي هو نفسه من قام برفع الكتاب
    if book_to_delete.uploaded_by.id == request.session['user_id']:
        book_to_delete.delete()
        return redirect('/books')
        
    return redirect('/books')



def update_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        book_to_update = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('/books')
    
    if book_to_update.uploaded_by.id == request.session['user_id']:
        errors =Book.objects.basic_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f'/books/{book_id}')
        else:
            book_to_update.title = request.POST.get('title')
            book_to_update.description = request.POST.get('description')
            book_to_update.save()
            return redirect(f'/books/{book_id}')
        
    return redirect('/books')
