# myapp/urls.py
from django.urls import path
from .views import custom_login
from django.contrib import admin
from .views import qr_code_decoder, video_feed,event_list,add_to_purchased,stop_stream,land,gallery_view,export_view,remove_purchased

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_code_decoder/', qr_code_decoder, name='qr_code_decoder'),
    path('video_feed/', video_feed, name='video_feed'),
    path('remove_purchased/<int:event_id>', remove_purchased, name='remove_purchased'),
    path('', land,name="land"),
    path('custom_login/', custom_login, name='custom_login'),
    path('export_view/', export_view, name='export'),
    path('gallery/', gallery_view, name='gallery'),
    path('event_list/',event_list, name='event_list'),
    path('add_to_purchased/<int:event_id>/', add_to_purchased, name='add_to_purchased'),
    path('stop_stream/', stop_stream, name='stop_stream'),
]
