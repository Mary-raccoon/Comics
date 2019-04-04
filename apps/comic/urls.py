from django.conf.urls import url
from django.conf.urls.static import static
from . import views   

urlpatterns = [
    url(r'^$', views.before),
    url(r'^log_reg$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^all_c$', views.all_c),
    url(r'^my_collection$', views.my_collection, name='my_collection'),
    url(r'^wishlist$', views.wishlist, name='wishlist'),
    url(r'^sold$', views.sold, name='sold'),
    url(r'^new_comic_my_collection$', views.new_comic_my_collection),
    url(r'^new_comic_wishlist$', views.new_comic_wishlist),
    url(r'^view_from_all/(?P<id>\d+)', views.view_from_all),
    url(r'^view_from_my_collection/(?P<id>\d+)', views.view_from_my_collection),
    url(r'^view_from_wishlist/(?P<id>\d+)', views.view_from_wishlist),
    url(r'^view_from_sold/(?P<id>\d+)', views.view_from_sold),
    url(r'^from_wish_to_collect/(?P<id>\d+)$', views.from_wish_to_collect),
    url(r'^from_collect_to_sold/(?P<id>\d+)$', views.from_collect_to_sold),
    url(r'^from_all_to_wish/(?P<id>\d+)$', views.from_all_to_wish),
    url(r'^add_to_my_collection$', views.add_to_my_collection),
    url(r'^add_to_wishlist$', views.add_to_wishlist),
    url(r'^(?P<id>\d+)/update_comic_all$', views.update_comic_all),
    url(r'^(?P<id>\d+)/update_comic_wish$', views.update_comic_wish),
    url(r'^(?P<id>\d+)/update_comic_sold$', views.update_comic_sold),
    url(r'^(?P<id>\d+)/update_comic_collect$', views.update_comic_collect),
    url(r'^(?P<id>\d+)/edit_all$', views.edit_all),
    url(r'^(?P<id>\d+)/edit_wish$', views.edit_wish),
    url(r'^(?P<id>\d+)/edit_sold$', views.edit_sold),
    url(r'^(?P<id>\d+)/edit_collect$', views.edit_collect),
    url(r'^(?P<id>\d+)/to_sell$', views.to_sell),
    url(r'^(?P<id>\d+)/destroy_from_my_collection$', views.destroy_from_my_collection),
    url(r'^(?P<id>\d+)/destroy_from_wishlist$', views.destroy_from_wishlist),
    url(r'^(?P<id>\d+)/destroy_from_sold$', views.destroy_from_sold),
    url(r'^sort_collect$', views.sort_collect),
    url(r'^sort_wish$', views.sort_wish),
    url(r'^sort_sold$', views.sort_sold),
    url(r'^sort_all$', views.sort_all),   
    url(r'^logout$', views.logout),
   
] 

