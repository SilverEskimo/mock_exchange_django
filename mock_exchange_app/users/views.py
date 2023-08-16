import os
import uuid
import boto3
from botocore.config import Config
from dotenv import load_dotenv
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mock_exchange_app.users.serializers import UserSerializer, UserProfileSerializer
from rest_framework.viewsets import ModelViewSet
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
BUCKET_NAME = 'mock-exchange-profile'


s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(
            signature_version='s3v4',
            region_name="us-east-2"
        )
)


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST'])
def google_login(request):
    google_jwt = request.data['google_jwt']
    print(google_jwt)
    try:
        id_info = id_token.verify_oauth2_token(google_jwt, requests.Request(), CLIENT_ID)

        email = id_info['email']
        user = ''
        try:
            user = User.objects.get(email=email)
            print('user found', user)
        except User.DoesNotExist:
            print('user does not exist')
            User.objects.create_user(
                username=email,
                email=email,
                password=str(uuid.uuid4()),
                first_name=id_info['given_name'],
                last_name=id_info['family_name']
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            data={
                'access': str(refresh.access_token)
            }
        )
    except ValueError:
        print(ValueError)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user_serializer = UserProfileSerializer(instance=request.user, many=False)
    # user_serializer = UserSerializer(instance=request.user, many=False)
    return Response(data=user_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_profile_image_signed_url(request):

    file_name = request.data['fileName']
    _, file_extension = os.path.splitext(file_name)
    object_name = f'profile_img_{request.user.id}_{uuid.uuid4()}{file_extension}'

    response = s3.generate_presigned_post(BUCKET_NAME, object_name, ExpiresIn=360)
    return Response(data=response)


@api_view(['POST'])
def update_profile_img(request):
    old_url = request.user.profile.img_url
    new_object_name = request.data['objectName']
    request.user.profile.img_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{new_object_name}'
    request.user.profile.save()

    old_object_name = old_url.split("/")[-1]
    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=old_object_name
    )

    response = UserProfileSerializer(request.user)
    return Response(data=response.data)
