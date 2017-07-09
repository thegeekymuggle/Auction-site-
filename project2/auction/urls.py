from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'auction'

urlpatterns = [

    url(r'^home/$', views.HomeView.as_view(), name='home'),

    url(r'^$', login, {'template_name': 'auction/login.html'}, name='login'),

    url(r'^register/$', views.UserReg.as_view(), name='user'),

    url(r'^home/productreg/$', views.ProductReg.as_view(), name='product-reg'),

    url(r'^home/category/product/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),

    url(r'^home/category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category-page'),

    url(r'^home/category/product/bid/(?P<pk>[0-9]+)/$', views.BidView.as_view(), name='bid-page'),
]

