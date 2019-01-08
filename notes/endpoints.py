from django.conf.urls import include, url
from rest_framework import routers
from knox import views as knox_views
from .api import NoteViewSet, RegistrationAPI, LoginAPI, UserAPI,Logout

router = routers.DefaultRouter()
router.register('notes', NoteViewSet, 'notes')

urlpatterns = [
    url("^", include(router.urls)),
    url("^auth/register/$", RegistrationAPI.as_view()),
    url("^auth/login/$", LoginAPI.as_view()),
    url("^auth/user/$", UserAPI.as_view()),
    url("^auth/logout/$", knox_views.LogoutView.as_view()),
]