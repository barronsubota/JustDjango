
# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include

app_name = 'JustDjango'

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('products/', include('fabric.urls', namespace='products')),
]
