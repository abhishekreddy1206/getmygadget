from django.conf.urls import patterns, include, url
from gadgetapp import views, api


urlpatterns = patterns('',

	# Direct django page rendering
	url(r'^$', views.DefaultView, name='default'),
	url(r'^menu/', views.ShowMenu, name='showmenu'),
	url(r'^register/$', views.Register, name='register'),
	url(r'^order/$', views.OrderView, name='order'),
	url(r'^checkout/$', views.Checkout, name='checkout'),
	url(r'^confirmorder/$', views.ConfirmOrder, name='corfirmorder'),
	url(r'^inventoryapi/', api.InventoryList.as_view(), name='inventorylist'),
)