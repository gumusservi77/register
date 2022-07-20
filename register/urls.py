from django.urls import path 
from .views import  EmailView , CodeView , ConfirmView , LoginView , ChangeView , ResetView , LogoutView  , GoogleLoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    
    path('email/',EmailView.as_view(),name='email'),
    path('code/',CodeView.as_view(),name='code'),
    path('confirm/<int:pk>/', ConfirmView.as_view(),name='confirm'),


    path('login/',LoginView.as_view(),name='login'),
    path('change/',ChangeView.as_view(),name='change'),
    path('reset/<int:pk>/',ResetView.as_view(),name='reset'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('google/',GoogleLoginView.as_view(),name='google'),


    # path('dj-rest-auth/google/',GoogleLoginView.as_view(),name='google_login'),
    

    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('token/verify/',TokenVerifyView.as_view(),name='token_verify'),

]