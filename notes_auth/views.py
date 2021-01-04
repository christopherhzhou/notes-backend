from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from .models import SafeEmail
from constants import AuthConstants


@api_view(['POST'])
def register(request):
    if not request.data.get('username') or not request.data.get('email') or not request.data.get('password'):
        return Response('Required fields missing.', status=status.HTTP_400_BAD_REQUEST)

    try:
        email = SafeEmail.objects.get(email=request.data['email'])
    except ObjectDoesNotExist:
        return Response('Your email has not been whitelisted for account creation.',
                        status=status.HTTP_401_UNAUTHORIZED)

    # check if email already exists, since Django doesn't automatically force user emails to be unique
    if len(User.objects.filter(email=request.data['email'])) == 1:
        return Response('The given email is already in use.', status=status.HTTP_401_UNAUTHORIZED)

    serialized_user = UserSerializer(data=request.data)

    if serialized_user.is_valid():
        serialized_user.save()
        curr_user = User.objects.get(id=serialized_user.instance.id)
        refresh = RefreshToken.for_user(curr_user)

        acc_created_res = {
            'code': AuthConstants.ACCOUNT_CREATED,
            'message': 'Account created!',
            'token': str(refresh.access_token),
        }

        return Response(acc_created_res, status=status.HTTP_201_CREATED)

    return Response('The given username is already in use.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def check_token(request):
    if request.user.is_authenticated:
        print(type(request.user))
        res = {
            'code': AuthConstants.TOKEN_VALID,
            'data': {
                'username': request.user.username
            }
        }
        return Response(res)

    error_res = {
        'code': AuthConstants.TOKEN_MISSING,
        'detail': 'No token was provided.'
    }

    return Response(error_res)


