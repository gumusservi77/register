from django.contrib import admin
from django.urls import path ,include
from register.views import GoogleLoginView , GitHubView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("register.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/',GoogleLoginView.as_view(),name='google_login'),
    path('dj-rest-auth/github/',GitHubView.as_view(),name='github_login'),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
]