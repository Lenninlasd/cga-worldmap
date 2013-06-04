from django.conf.urls.defaults import *
from geonode.worldmap.register.views import SignupView, registercompleteOrganizationUser, forgotUsername
from geonode.worldmap.register.forms import UserRegistrationForm

urlpatterns = patterns('',
                       url(r"^signup/$", SignupView.as_view(), name="account_signup"),
                       url(r'^forgotname/$',
                           forgotUsername, name="account_forgotname"),
                       (r'', include('account.urls')),
                       )

