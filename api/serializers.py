from rest_framework import serializers
from .models import category,order,orderITem,cart,MenuItem
from decimal import Decimal
from django.contrib.auth.models import User

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model= category
        fields = ['slug', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset = category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category']
        
class cart(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault
    )
    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return super().validate(attrs)
    class Meta:
        model = cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
        extra_kwargs ={
            'price':{'read_only':True}    
        }
       
class orderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderITem
        fields = ['order', 'menuitem', 'quantity',
                  'unit_price', 'price'] 
        
class orderSerializer(serializers.ModelSerializer):
    orderItem = orderItemSerializer(many = True, read_only = True,
                                    source ='order')
    class Meta:
        model  = order
        fields = ['user', 'delivery_crew', 'status',
                  'total', 'date', 'orderItem']
        
class users(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        

    