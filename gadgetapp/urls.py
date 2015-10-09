from django.conf.urls import patterns, url

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
                       url(r'^postorder/', views.PostOrder, name='postorder'),
                       url(r'^postnotes/', views.PostNotes, name='postnotes'),
                       url(r'^getlatestorderuser/', api.GetLatestOrderUser.as_view(), name='getlatestorderuser'),
                       url(r'^dashboard/$', views.Dashboard, name='dashboard'),
                       url(r'^userapi/', api.UserOrderList.as_view(), name='userlist'),
                       url(r'^approverapi/', api.ApproverList.as_view(), name='approverlist'),
                       url(r'^changeorderstatus/(?P<pk>\d+)/(?P<status>.*)', views.ChangeOrderStatus, name='changeorderstatus'),
                       url(r'^getorderdetail/(?P<pk>\d+)', api.GetOrderDetail.as_view(), name='getorderdetail'),
                       url(r'^postcomments/', views.PostComments, name='postcomments'),
                       )
