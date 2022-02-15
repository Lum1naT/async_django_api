from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from api import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


router = routers.DefaultRouter()
router.register(r'sources', views.SourceViewSet)
router.register(r'keys', views.KeyViewSet)
router.register(r'leads', views.LeadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('check', views.check, name="check"),
    path('accept', views.accept, name="accept"),
    path('stats/<str:token>', views.testStats, name="stats")

]

urlpatterns += staticfiles_urlpatterns()
