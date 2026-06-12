from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.index),
    path('add_book/' , views.create_book),
    path('<int:book_id>' , views.book_detail),
    path('<int:book_id>/favorite' , views.favorite_book),
    path('<int:book_id>/unfavorite' , views.unfavorite_book),
    path('<int:book_id>/delete' , views.delete_book),
]
