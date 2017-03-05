from django.conf.urls import url, include # Notice we added include
from django.contrib import admin
urlpatterns = [
	url(r'^', include('apps.django_test_app.urls')) # And now we use include to pull in our first_app.urls...
]
