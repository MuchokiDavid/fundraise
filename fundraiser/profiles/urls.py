from django.urls import path
from .views import SignUp, LogIn, RefreshTokenView, LogOut, UserView,ResetPassword,ChangePassword

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),
    path('refresh/token/', RefreshTokenView.as_view(), name='refresh token'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path("reset-password/", ResetPassword.as_view(), name="reset password"), #POST: Send token to user email
    path("change-password/", ChangePassword.as_view(), name="change password"),
]