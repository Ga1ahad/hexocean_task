from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from thumbnail.views import ImageListView, upload_image, create_expiring_link, ExpiringLinkModelViewSet, ImageDetailView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('images', ImageListView.as_view(), name='images'),
    path('images/<int:img_id>', ImageDetailView.as_view(), name='image'),
    path('images/upload', upload_image, name='upload_image'),
    path('images/<int:img_id>/expiring_img/<int:seconds>', create_expiring_link, name='create_tmp_link'),
    path('expiring_img/<int:img_id>/', ExpiringLinkModelViewSet.as_view(), name='get_tmp_link')
]
