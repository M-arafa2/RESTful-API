from django.contrib import admin
from .models import cart,category,MenuItem,order,orderITem

# Register your models here.
admin.site.register(cart)
admin.site.register(category)
admin.site.register(MenuItem)
admin.site.register(order)
admin.site.register(orderITem)
