from rest_framework import serializers
from .models import *

class PopularPodcastSerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(source="thumbnail.url")
    file = serializers.CharField(source="file.url")
    
    class Meta:
        model = podcast_data
        fields = ['user','postid','title','thumbnail','description','type','likes','speaker','file']

class FavouritePodcastSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField()
class getPodcast(serializers.Serializer):
    class Meta:
        model = Favorite_podcast
        fields = ['__all__']
