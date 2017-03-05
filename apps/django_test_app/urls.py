from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.homepage),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^success_page$', views.success_page),
	url(r'^trip_info_page/(?P<url_id>\d+)$', views.trip_info_page),
	url(r'^join/(?P<url_id>\d+)$', views.join),
	url(r'^add_page$', views.add_page),
	url(r'^add$', views.add),
	url(r'^log_out$', views.log_out),

]
