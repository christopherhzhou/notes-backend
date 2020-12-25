from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.note_api_overview, name='api-overview'),
    path('note/', views.note_list, name='note-list'),
    path('note/<int:pk>/', views.note_detail, name='note-detail'),
    path('note-create/', views.note_create, name='note-create'),
    path('note-update/<int:pk>/', views.note_update, name='note-update'),
    path('note-delete/<int:pk>/', views.note_delete, name='note-delete'),
]
