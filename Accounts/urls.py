from django.urls import path, include
from .views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('register', register.as_view()),
    path('login', login.as_view()),
    path('user/<str:JWTUser>', userView.as_view()),
    path('logout', logout.as_view()),
    
]