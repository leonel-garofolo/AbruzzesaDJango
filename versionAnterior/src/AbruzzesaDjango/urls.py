from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from ajax_select import urls as ajax_select_urls
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.sites.site = admin.site
admin.autodiscover()

urlpatterns = [  
    url(r'^', include('gestionAlumnos.urls')),
    # place it at whatever base url you like
    url(r'^ajax_select/', include(ajax_select_urls)),   
    url(r'^admin/', include(admin.site.urls)),    
] 