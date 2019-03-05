from django.urls import path
from handler import views

urlpatterns = [
   path('webhook/',views.get_changes),
   path('webhook_show/', views.get_changes_show),

]
