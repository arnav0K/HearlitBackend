from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
import jwt,datetime
from rest_framework import generics

class register(APIView):
    def post(self,request):
        serializers = UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

class login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('You are not registered on the platform')
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=720),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        # .decode('utf-8')
        response = Response()
        # response.set_cookie(key='jwt',value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response

class userView(APIView):
    def get(self, request,JWTUser):
        token = None
        if JWTUser!='None':
            token = JWTUser
        # request.COOKIES.get('jwt')
        print(type(token),"typeeeeeeeeeeeeeeeeeeeeeeeeee")
        print(token,"Here is the token, -----------sssssssssssss-----s-s--s-s-sssssssss")
        if not token:
            raise AuthenticationFailed('Unauthenticated please login')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated please login')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)

class logout(APIView):
    def post(self, request):
        response = Response()
        # response.delete_cookie('jwt')
        response.data = {
            'message':"Successfully Logout"
        }
        return response

