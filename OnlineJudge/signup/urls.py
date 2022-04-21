from django.conf.urls import url
from signup import views

urlpatterns = [
	# url(r'^home/$',views.greetings),
    url(r'^P{0-9}$/^home/run$',views.runcode),
]
