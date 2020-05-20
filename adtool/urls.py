from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.AdvertisementListView.as_view(), name='home'),
    path('advertisement/<int:pk>/',
         views.AdvertisementDetailView.as_view(), name='detail'),
    path('advertisement/upload/',
         views.AdvertisementCreateView.as_view(), name='upload'),
    path('advertisement/<int:pk>/update/',
         views.AdvertisementUpdateView.as_view(), name='update'),
    path('advertisement/<int:pk>/delete/',
         views.AdvertisementDeleteView.as_view(), name='delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/<str:size>/<str:user_key>', views.Api.as_view(), name='api'),
    path('api/', views.Api.as_view(), name='api_post'),
    path('api/advertisement/<int:pk>/<int:site_pk>/<str:unique_key>/', views.ad_redir, name='ad_redir'),
    path('about/',views.about,name = 'about'),
    path('adclient/', views.register_website, name='register_website'),
    # AJAX:
    path('home/advertisement-enable-toggle-ajax/', views.enable_toggle, name='enable_toggle'),
    path('adclient/change-userkey/', views.change_userkey, name='change-userkey'),
    path('adclient/delete-userkey/', views.delete_userkey, name='delete-userkey'),
]
