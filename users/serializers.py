from rest_framework import serializers
from .models import CustomUser

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar', 'city', 'bio']
        extra_kwargs = {
            'email': {'required': False},
            'avatar': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'city': {'required': False},
            'bio': {'required': False},
        }

    def validate_avatar(self, value):
        """
        Validate avatar size to ensure it is less than 1 MB.
        """
        max_size = 1 * 1024 * 1024  # 1 MB

        if value.size > max_size:
            raise serializers.ValidationError("The avatar image size should not exceed 1 MB.")
        
        return value

    def validate_email(self, value):
        """
        Validate email to ensure no other user has the same email.
        """
        user = self.context['request'].user
        if CustomUser.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'username',
            'is_email_verified', 'subscription_status', 'subscription_start_date',
            'subscription_end_date', 'is_trial_used', 'is_auto_renewal',
            'stripe_customer_id', 'stripe_subscription_id', 'avatar',
            'city', 'bio', 'educational_status', 
            'desired_specialty'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        help_text='First name of the user.',
        max_length=150
    )
    last_name = serializers.CharField(
        required=True,
        help_text='Last name of the user.',
        max_length=150
    )
    email = serializers.EmailField(
        required=True,
        help_text='Email address of the user.',
    )
    username = serializers.CharField(
        required=True,
        help_text='Desired username for the user.',
        max_length=150
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Password for the user.',
        max_length=128
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        # Create a new user using the custom user manager
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )
        return user
