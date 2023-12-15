from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .models import *
import jwt,datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

class podcastView(generics.ListCreateAPIView):
    queryset = podcast_data.objects.all()
    serializer_class = PopularPodcastSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PopularPodcastSerializer(queryset, many=True)
        return Response(serializer.data)
    
class podcastList(generics.ListCreateAPIView):
    search_fields = ['title','description','speaker']
    filter_backends = (filters.SearchFilter,)
    queryset = podcast_data.objects.all()
    serializer_class = PopularPodcastSerializer
    
class podcast(APIView):
    def get(self,request,postid):
        queryset = podcast_data.objects.filter(postid=postid).first()
        serializer = PopularPodcastSerializer(queryset)
        return Response(serializer.data)
    
class FavouritePodcast(APIView):
    def get(self,request,postid,username):
        user = User.objects.get(email=username)
        podcast_item = podcast_data.objects.filter(postid=postid).first()
        try:
            podcastq = Favorite_podcast.objects.get(user=user,podcast=podcast_item)
            is_favorite = podcastq.is_favorite
            print("Hereeeeeeeeeeeeeeeeeeeeeeeee---------eeee",is_favorite)
            serializer = FavouritePodcastSerializer({'is_favorite': is_favorite})
            return Response(serializer.data)
        except Favorite_podcast.DoesNotExist:
            return Response("NO favourite Podcast")
    
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        postid = request.data.get('postid')
        print(username,postid, "impooooooooooooorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrnttttttttttttt")
        user = User.objects.filter(email=username).first()
        print(user)
        podcast = podcast_data.objects.filter(postid=postid).first()
    
        print(podcast,"here------------------xxxxxxxxxxx--------------xxxxxxxxxxxxx-------xx-x-x-xxxxxxxxxxxxxx")
        try:
            fav = Favorite_podcast.objects.get(user=user, podcast=podcast)
            if fav.is_favorite==True:
                fav.is_favorite = False
                if podcast.likes >=1:
                    podcast.save()
                    podcast.likes-=1
                    podcast.save()
                fav.save()
                return Response({'message': 'Podcast removed from favorite'})
            else:
                fav.is_favorite = True
                podcast.likes+=1
                podcast.save()
                fav.save()
                return Response({'message': 'Podcast Marked as Favorite'})
            
        except Favorite_podcast.DoesNotExist:
            fav = Favorite_podcast.objects.create(user=user, podcast=podcast)
            fav.is_favorite = True
            podcast.likes+=1
            podcast.save()
            fav.save()
            return Response({'message': 'Podcast marked as favorite'})
            
    
    def put(self, request,*args,**kwargs):
        username = request.GET.get('username')
        postid = request.GET.get('postid')
        user = User.objects.filter(email=username).first()
        try:
            post = podcast_data.objects.filter(postid=postid).first()
            favorite = Favorite_podcast.objects.get(podcast=post)
            print(favorite,"------dx-x--x-xxxxxxxxxxxxxxxx---------xxxxxxxxxxxxxxxx----------xxxxxxxx")
            favorite_podcast = None
            print(favorite_podcast,"------dx-x--x-xxxxxxxxxxxxxxxx---------xxxxxxxx")
            if favorite_podcast.is_favorite == False:
                favorite_podcast.is_favorite = True
                favorite_podcast.save()
            else:
                favorite_podcast.is_favorite = False
                favorite_podcast.save()
            print(favorite_podcast)
            return Response({'message': 'Podcast marked as favorite'})
        except Favorite_podcast.DoesNotExist:
            return Response({'message': 'Podcast Not found'})
class get_podcast(APIView):
    
    def get(self,request,user):
        try:
            user1 = User.objects.filter(email=user).first()
            queryset = Favorite_podcast.objects.filter(user=user1)
            fpod = []
            print(type(queryset),"-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-here is querset")
            print(queryset,"-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-here is querset")
            for i in queryset:
                if i.is_favorite:
                    fpod.append(i.podcast)
                    print(i.podcast,"-/-/-/-/-/-/-/-/-/-/-/-")
            print(fpod)
            serializer = PopularPodcastSerializer(fpod, many=True)
            return Response(serializer.data)
        except user1.DoesNotExist or queryset.DoesNotExist:
            return Response("No Favorite Podcast")
    # def list(self, request,user):
    #     try:
    #         queryset = self.get_queryset()
    #         serializer = PopularPodcastSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     except queryset.DoesNotExist:
    #         return Response("No Favorite Podcast")
    
class UserPodcastViewset(viewsets.ViewSet):
    def addPodcast(self,request):
        user = request.data.get('formuser')
        title = request.data.get('title')
        description = request.data.get('description')
        speakername = request.data.get('speakername')
        imagefile = request.data.get('imagefile')
        audiofile = request.data.get('audiofile')

        #user 
        podcastuser = User.objects.filter(email=user).first()
        # creating the podcast object for user
        podcast_data.objects.create(user=podcastuser, title=title, description=description,thumbnail=imagefile, type="AUDIO",speaker=speakername, file=audiofile)
        print(user, title, " ",description,speakername, imagefile, audiofile)

        return Response(status=201)
        
    def updatePodcast(self,request,pk):
        print(" =========  ",request.data)
        data = request.data
        podcast = podcast_data.objects.get(postid=pk)
        if podcast:
            podcast.title = data['title']
            podcast.description = data['description']
            podcast.speaker = data['speaker']
            # Update other fields as needed
            podcast.save()
            return Response(status=201,data={'message': 'Podcast updated successfully'})
        else:
            return Response({'message': 'Podcast not found'})
        
    
        #     return Response(status=201, data="Sucessfully Updated Post Data")
        # else:
        #     return Response(status=401,data="Invalid User")
    
# class addPodcast(APIView):
    
#     def post(self, request):
#         user = request.data.get('formuser')
#         title = request.data.get('title')
#         description = request.data.get('description')
#         speakername = request.data.get('speakername')
#         imagefile = request.data.get('imagefile')
#         audiofile = request.data.get('audiofile')

#         #user 
#         podcastuser = User.objects.filter(email=user).first()
#         # creating the podcast object for user
#         podcast_data.objects.create(user=podcastuser, title=title, description=description,thumbnail=imagefile, type="AUDIO",speaker=speakername, file=audiofile)
#         print(user, title, " ",description,speakername, imagefile, audiofile)

#         return Response(status=201)
    
#     def update(self,request):
#         postid = request.data.get('postid')
#         user = request.data.get('formuser')
#         title = request.data.get('title')
#         description = request.data.get('description')
#         speakername = request.data.get('speakername')
#         imagefile = request.data.get('imagefile')
#         audiofile = request.data.get('audiofile')
#         # podcast_user = User.objects.filter(email=user).first()
#         podcast_data_obj = podcast_data.objects.get(postid=postid)
#         if podcast_data_obj.user.email == user:
#             podcast_data_obj.title = title
#             podcast_data_obj.description = description
#             podcast_data_obj.speaker = speakername
#             podcast_data_obj.thumbnail = imagefile
#             podcast_data_obj.file = audiofile
#             podcast_data_obj.save()
#             return Response(status=201, body="Sucessfully Updated Post Data")
#         else:
#             return Response(status=401,body="Invalid User")
        
    
class UserPodcast(APIView):
    def get(self, request,user):
        print(user)
        podcastuser = User.objects.filter(email=user).first()
        print(podcastuser," =-------------------xxxxxxxxxxxxxxxxxxxxxxxxxxxx---------------=")
        userpodcast = podcast_data.objects.filter(user=podcastuser)
        serializer = PopularPodcastSerializer(userpodcast, many=True)
        return Response(serializer.data)
        
    