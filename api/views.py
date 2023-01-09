from django.shortcuts import render,get_object_or_404
from rest_framework import generics,viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.models import User,Group

from .models import category,MenuItem,cart,order,orderITem
from .serializers import categorySerializer,MenuItemSerializer,cartSerializer
from .serializers import orderItemSerializer,orderSerializer,userSerializer

# Create your views here.

class categoryView(generics.ListAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer
    
# functions for listing,adding and deleting users from Manager group
# Requires super user authorization
class UserGroupViewSet(viewsets.ViewSet):
    permission_classes =[IsAdminUser]
    def list(self,request):
        managers =User.objects.all().filter(groups__name='Manager')
        serlializerList=userSerializer(managers,many =True)
        return Response(serlializerList.data)
    
    def create(self,request):
        user = get_object_or_404(User,username =request.data['username'])
        managers = Group.objects.get(name = 'Manager')
        managers.user_set.add(user)
        return Response({"message":"manager was added "},200)
    
    def destroy(self,request):
        user = get_object_or_404(User,username =request.data['username'])
        managers = Group.objects.get(name = 'Manager')
        managers.user_set.remove(user)
        return Response({"message":"manager was Removed "},200)
    
# functions for listing,adding and deleting users from Delivery crew group
# Requires super user or Manager authorization
class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    def list(self,request):
        crew =User.objects.all().filter(groups__name ='Delivery Crew')
        serializerlist = userSerializer(crew,many =True)
        return Response(serializerlist.data)
    
    def create(self,request):
        if self.request.is_Superuser ==False:
            if not self.request.groups.filter(name='Manager').exists()==False:
                return Response({'Message':'user is not Authorized'},status.HTTP_403_FORBIDDEN)

        user =get_object_or_404(User,username=request.data['username'])
        crew =Group.objects.get(name ='Delivery Crew')
        crew.user_set.add(user)
        return Response({'message':'delivery crew was added'},200)
    
    def destroy(self,request):
        if self.request.is_Superuser ==False:
            if not self.request.groups.filter(name='Manager').exists()==False:
                return Response({'Message':'user is not Authorized'},status.HTTP_403_FORBIDDEN)

        user =get_object_or_404(User,username=request.data['username'])
        crew =Group.objects.get(name ='Delivery Crew')
        crew.user_set.remove(user)
        return Response({'message':'delivery crew was deleted'},200)
        