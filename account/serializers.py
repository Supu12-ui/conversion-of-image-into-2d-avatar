from xml.dom import ValidationErr
from rest_framework import serializers
from account.models import Sunglass, User, Avatar, EyeImage



class UserRegistrationSerailzer(serializers.ModelSerializer):
    #password2 = serializers.CharField(style ={'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['email','name','tc', 'password','mobile','country']
        extra_kwargs={
            'password': {'write_only':True},
            'mobile': {'required': True},
            'country': {'required': True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
       
        if not password:
            raise serializers.ValidationError("Password is required")
        return attrs
    
    def create(self, validate_data):
        # validate_data.pop('password2')
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta: 
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        # user = self.context.get('user')
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist: 
            raise serializers.ValidationError("User with this email does not exist")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self,attrs):
            email = attrs.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email = email)
            else:
                raise ValidationErr("You are not registered with this email")

class GenderUserSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gender']
    
    def update(self, instance, validated_data):
         instance.gender = validated_data.get('gender', instance.gender)

         instance.save()
         return instance
    
    def validate(self, data):
         errors={}
         if data.get('gender') is None:
              errors['gender'] = ['This field is required.']
         if errors:
              raise serializers.ValidationError(errors)
         return data
              
class AvatarImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'image', 'avatar_image_url', 'created_at', 'png_image']
    def validate_image(self, value):
            if not (value.name.endswith('.jpg') or value.name.endswith('.png') or value.name.endswi2):
                raise serializers.ValidationError("Only JPG and PNG images are allowed.")
            return value

    def update(self, instance, validated_data):
            if (validated_data.get('image') is not None):
                instance.image = validated_data.get('image')
            if validated_data('avatar_image_url') is not None:
                instance.avatar_image_url = validated_data.get('avatar_image_url')
            instance.save()
            return instance
        
    def validate(self,data):
            errors={}
            if data.get('image') is None:
                errors['image'] = ['This field is required.']
            
            if errors:
                raise serializers.ValidationError(errors)
            
            return data


class EyeImageSerailzer(serializers.ModelSerializer):
     class Meta:
          model = EyeImage
          fields = ['id', 'left_eye_image','right_eye_image']

class SunglassImageSerailzer(serializers.ModelSerializer):
    class Meta:
        model = Sunglass
        fields = ['avatar_url', 'sunglasses_image']
