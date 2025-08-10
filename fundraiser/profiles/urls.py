from django.urls import path
from .views import SignUp, LogIn, RefreshTokenView, LogOut, UserView

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),
    path('refresh/token/', RefreshTokenView.as_view(), name='refresh token'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
]