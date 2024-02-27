from django.urls import path
from contact import views

urlpatterns = [
    path('contact/', views.ContactMessageList.as_view()),
    path('contact/<int:pk>/', views.ContactMessageDetail.as_view())
]