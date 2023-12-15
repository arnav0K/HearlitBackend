from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings

# user_podcast = UserPodcast.as_view({'post': 'addPodcast',})
user_podcast_add = UserPodcastViewset.as_view({'post': 'addPodcast',})
user_podcast_update = UserPodcastViewset.as_view({'post': 'updatePodcast',})


urlpatterns = [
    path("popular",podcastView.as_view(),name="famous_podcast"),
    path("podcast/",podcastList.as_view(),name="famous_podcast"),
    path("podcast/<str:postid>",podcast.as_view(),name="particular_podcast"),
    path("podcastFav/<uuid:postid>/<str:username>/",FavouritePodcast.as_view(),name="favourite_podcast"),
    path("podcastFav/<str:user>/",get_podcast.as_view(),name="get_podcast"),
    path("podcast/add/",user_podcast_add,name="user_podcast_add"),
    path("podcast/update/<uuid:pk>",user_podcast_update,name="user_podcast_update"),
    path("podcast/user/<str:user>/",UserPodcast.as_view(),name="user_podcast"),
    
]
