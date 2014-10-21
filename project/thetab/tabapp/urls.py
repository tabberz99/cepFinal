from django.conf.urls import patterns, url
from tabapp import views

urlpatterns = patterns('',
        #url(r'^$', views.home, name='index'),
        url(r'^$', views.ListActivities, name='actList'),
        url(r'^custom/(?P<activity_name_url>\w+)/$', views.customActivity, name='actDetail'),
        url(r'^customact/$',views.add_customActivity, name="newCustomAct"),
        url(r'^customvar/$',views.add_customVariable, name="newCustomVar"),
        url(r'^customtm/$',views.add_customTeam, name="newCustomTeam"),
        url(r'^customdel/(?P<del_name_url>\w+)/$',views.delCustomActivity, name="delCustomAct"),
        url(r'^Cookie_Eating/$', views.CookEat2, name='cookieEating'),
        url(r'^Swimming/$', views.swimming, name='swim'),
        url(r'^Debate/$',views.Debate, name="Debating"),
        url(r'^register/$', views.register, name='register'),
        #url(r'^restricted/', views.restricted, name='restricted'), #View that requires users to login
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
)