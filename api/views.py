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
    
    
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['categort__title']
    ordering_fields = ['price','inventory']
    def get_permissions(self):
        permission_classes =[]
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
                
        return [permission() for permission in permission_classes]
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        permission_classes =[]
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
                
        return [permission() for permission in permission_classes]
    
class CartView(generics.ListCreateAPIView):
    queryset = cart.objects.all()
    serializer_class = cartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return cart.objects.all().filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        cart.objects.all().filter(user=self.request.user).delete()
        return Response("Deleted")
    
    
class orderView(generics.ListCreateAPIView):
    queryset = order.objects.all()
    serializer_class = orderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.is_superuser or self.request.groups.filter(name='Manager').exists():
            return order.objects.all()
        elif self.request.groups.filter(name='Delivery Crew').exists():
            return cart.objects.all().filter(delivery_crew =self.request.user)
        elif self.request.groups.count()==0:
            return cart.objects.all().filter(user =self.request.user)
        
    def create(self, request, *args, **kwargs):
        menuitem_count = cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "cart is empty"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = orderSerializer(data=data)
        if (order_serializer.is_valid()):
            order = order_serializer.save()

            items = cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = orderITem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()
                cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data)
    
    def get_total_price(self, user):
        total = 0
        items = cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = order.objects.all()
    serializer_class = orderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: 
            # customer
            return Response('Not Ok')
        else: #Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)
        
        
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
            if self.request.groups.filter(name='Manager').exists()==False:
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
        