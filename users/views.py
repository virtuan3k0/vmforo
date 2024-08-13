from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import UserUpdateSerializer, UserDetailSerializer, UserRegistrationSerializer


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    @extend_schema(
        tags=['user'],
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiExample(
                'User Registration Success',
                value={'message': 'User registered successfully'},
            ),
            400: OpenApiExample(
                'User Registration Error',
                value={'email': ['This field is required.']},
            )
        },
        description="Register a new user by providing first name, last name, email, password, and username. "
                    "Each of these fields is required. Ensure the email is unique and valid.",
        examples=[
            OpenApiExample(
                'User Registration Example',
                summary='Sample Registration Payload',
                description='An example of a valid registration request payload.',
                value={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'username': 'johndoe',
                    'password': 'strongpassword123'
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    API endpoint to retrieve details of the currently logged-in user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['user'],
        responses=UserDetailSerializer,
        description="Retrieve the details of the currently logged-in user. "
                    "This endpoint requires authentication and returns the user's profile information.",
        examples=[
            OpenApiExample(
                'User Detail Example',
                summary='Sample User Detail Response',
                description='An example of a successful response for the user detail endpoint.',
                value={
                    'id': 1,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'username': 'johndoe',
                    'is_email_verified': True,
                    'subscription_status': 'active',
                    'subscription_start_date': '2024-01-01T00:00:00Z',
                    'subscription_end_date': '2025-01-01T00:00:00Z',
                    'is_trial_used': False,
                    'is_auto_renewal': True,
                    'stripe_customer_id': 'cus_Jf93dj3f93j',
                    'stripe_subscription_id': 'sub_49ty789o56er',
                    'avatar': 'http://example.com/media/avatars/johndoe.jpg',
                    'city': 'New York',
                    'bio': 'I am a medical student...',
                    'educational_status': 3,
                    'desired_specialty': 8
                }
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    """
    API endpoint to update the currently logged-in user's profile.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)  # Allow JSON input in addition to form data

    @extend_schema(
        tags=['user'],
        request={
            'application/json': UserUpdateSerializer,
            'multipart/form-data': UserUpdateSerializer,
        },
        responses=UserDetailSerializer,
        description="Update the profile of the currently logged-in user. "
                    "This endpoint supports updating fields such as first name, last name, email, avatar, city, and bio. "
                    "The avatar should be a valid image file and must not exceed 1 MB.",
        examples=[
            OpenApiExample(
                'User Profile Update JSON Example',
                summary='Sample Profile Update JSON Payload',
                description='An example of a valid profile update request payload using JSON.',
                value={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.newemail@example.com',
                    'avatar': 'http://example.com/media/avatars/johndoe.jpg',  # JSON representation of avatar
                    'city': 'Los Angeles',
                    'bio': 'Updated bio text...'
                },
                request_only=True
            ),
            OpenApiExample(
                'User Profile Update Form Example',
                summary='Sample Profile Update Form Payload',
                description='An example of a valid profile update request payload using form data.',
                value={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.newemail@example.com',
                    'avatar': '<binary_image_data>',  # Placeholder for binary image data
                    'city': 'Los Angeles',
                    'bio': 'Updated bio text...'
                },
                request_only=True
            ),
            OpenApiExample(
                'User Profile Update Success',
                summary='Successful Profile Update Response',
                description='An example of a successful response after updating the profile.',
                value={
                    'id': 1,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.newemail@example.com',
                    'username': 'johnnydoe',
                    'is_email_verified': True,
                    'subscription_status': 'active',
                    'subscription_start_date': '2024-01-01T00:00:00Z',
                    'subscription_end_date': '2025-01-01T00:00:00Z',
                    'is_trial_used': False,
                    'is_auto_renewal': True,
                    'stripe_customer_id': 'cus_Jf93dj3f93j',
                    'stripe_subscription_id': 'sub_49ty789o56er',
                    'avatar': 'http://example.com/media/avatars/johnnydoe.jpg',
                    'city': 'Los Angeles',
                    'bio': 'Updated bio text...',
                    'educational_status': 3,
                    'desired_specialty': 8
                },
                response_only=True
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(UserDetailSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
