from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import get_user, authenticate, login, logout
from ..serializers import UserSerializer, UserRegisterSerializer,  ChangePasswordSerializer, GetUserDetailsSerializer
from django.contrib.auth import get_user_model


class SignUp(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    # Serializer classes are required for endpoints that create data
    serializer_class = UserRegisterSerializer

    def post(self, request):
        # Pass the request data to the serializer to validate it
        user = UserRegisterSerializer(data=request.data['credentials'])
        # If that data is in the correct format...
        if user.is_valid():
            # Actually create the user using the UserSerializer (the `create` method defined there)
            created_user = UserSerializer(data=user.data)

            if created_user.is_valid():
                # Save the user and send back a response!
                created_user.save()
                return Response({ 'user': created_user.data }, status=status.HTTP_201_CREATED)
            else:
                return Response(created_user.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    # Serializer classes are required for endpoints that create data
    serializer_class = UserSerializer

    def post(self, request):
        creds = request.data['credentials']
        print(creds)
        # We can pass our email and password along with the request to the
        # `authenticate` method. If we had used the default user, we would need
        # to send the `username` instead of `email`.
        user = authenticate(request, email=creds['email'], password=creds['password'])
        # Is our user is successfully authenticated...
        if user is not None:
            # And they're active...
            if user.is_active:
                # Log them in!
                login(request, user)
                # Finally, return a response with the user's token
                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'user_img_url': user.user_img_url,
                        'email': user.email,
                        'token': user.get_auth_token()
                    }
                })
            else:
                return Response({ 'msg': 'The account is inactive.' }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'msg': 'The username and/or password is incorrect.' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SignOut(generics.DestroyAPIView):
    def delete(self, request):
        # Remove this token from the user
        request.user.delete_token()
        # Logout will remove all session data
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePassword(generics.UpdateAPIView):
    def partial_update(self, request):
        user = request.user
        # Pass data through serializer
        serializer = ChangePasswordSerializer(data=request.data['passwords'])
        if serializer.is_valid():
            # This is included with the Django base user model
            # https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.check_password
            if not user.check_password(serializer.data['old']):
                return Response({ 'msg': 'Wrong password' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # set_password will also hash the password
            # https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.set_password
            user.set_password(serializer.data['new'])
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetails(generics.ListAPIView):
    """A class for retrieving user details"""

    def get(self, request):
        """return the user details that users are allowed to update"""
        user_model = get_user_model()
        user = user_model.objects.get(pk=request.user.id)
        serialized_user = GetUserDetailsSerializer(user)
        return Response({'user': serialized_user.data})


class UpdateUserDetails(generics.UpdateAPIView):
    """Class for updating user details"""

    def partial_update(self, request):
        """Partially update user details"""
        user_model = get_user_model()
        user = user_model.objects.get(pk=request.user.id)
        print('user: ', user.__dict__)
        serialized_user = UserSerializer(user, data=request.data['user'], partial=True)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response({"user": serialized_user.data}, status=status.HTTP_200_OK)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
