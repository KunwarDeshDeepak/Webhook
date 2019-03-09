from django.urls import path
from handler import views

urlpatterns = [
   path('webhook/',views.get_changes),
   path('webhook_show/', views.get_changes_show),
   path('demo/',views.sheets_handler),
   path('googlea73117b61cc11fc2.html/', views.show_html),
]
