from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.http import JsonResponse, Http404, FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from PIL import Image as PILImage
from thumbnail.models import Image, User, AccountTier, ExpiringLink
from thumbnail.serializers import ImageSerializer, ExpiringLinkSerializer


class ImageListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user
        tier = AccountTier.objects.get(id=user.tier_id)
        if tier.original_img:
            queryset = Image.objects.all().filter(owner=user)
        else:
            queryset = Image.objects.all().filter(owner=user, is_original=False)
        return queryset

    def get_object(self):
        image_id = self.kwargs.get('img_id')
        try:
            image = Image.objects.get(pk=image_id, owner=self.request.user)
        except Image.DoesNotExist:
            raise Http404
        return image.image

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object().image
        return FileResponse(image)


class ImageDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        image_id = self.kwargs.get('img_id')
        try:
            image = Image.objects.get(pk=image_id, owner=self.request.user)
        except Image.DoesNotExist:
            raise Http404
        return image.image

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object()
        return FileResponse(image)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_image(request):
    response_dict = {}
    request.data.owner = request.POST.get('owner')
    user = User.objects.get(pk=request.user.id)
    tier = AccountTier.objects.get(pk=user.tier_id)
    request.data.image = request.FILES.get('image')
    valid_formats = ['png', 'jpg']
    img_name = request.data.image.name.lower()
    if not any([True if img_name.endswith(i) else False for i in valid_formats]):
        raise ValidationError('invalid image format')
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save(owner=request.user)
            img_url = '/images/' + str(serializer.data['id'])
            if tier.original_img:
                response_dict["Original_img_" + request.data.image.name] = img_url
        thumbnails = tier.thumbnail_size.all()
        for thumbnail in thumbnails:
            thumbnail_name = 'Thumbnail-{thumbnail}px_{original_name}'.format(thumbnail=thumbnail.thumbnail_size,
                                                                              original_name=request.data.image.name)
            pilImage = PILImage.open(request.data.image)
            tmp_img = pilImage.resize((thumbnail.thumbnail_size, thumbnail.thumbnail_size))
            tmp_img.save(settings.MEDIA_ROOT + '/' + thumbnail_name)
            with open('files/' + thumbnail_name, 'rb') as file:
                image_file = File(file)
                img = Image.objects.create(image=image_file, owner=request.user, is_original=False)
            response_dict[thumbnail_name] = settings.MEDIA_URL + str(img.pk)
    else:
        error = serializer.errors
        return Response({
            'status': 'Bad request',
            'message': error,
        }, status=HTTP_400_BAD_REQUEST)
    return JsonResponse(response_dict)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_expiring_link(request, img_id, seconds):
    try:
        img = Image.objects.get(pk=img_id, owner=request.user)
    except Image.DoesNotExist:
        raise Http404
    expiring_link = ExpiringLink.objects.create(image=img, expire_time=seconds)
    response_dict = {'expiring_link': str(expiring_link.pk)}
    return JsonResponse(response_dict)


class ExpiringLinkModelViewSet(RetrieveAPIView):
    serializer_class = ExpiringLinkSerializer

    def get_object(self):
        expiring_link_id = self.kwargs.get('img_id')
        try:
            expiring_link = ExpiringLink.objects.get(pk=expiring_link_id)
        except ExpiringLink.DoesNotExist:
            raise Http404
        if expiring_link.is_expired():
            expiring_link.delete()
            raise Http404
        return expiring_link.image

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object().image
        return FileResponse(image)
