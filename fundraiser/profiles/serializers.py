from rest_framework import serializers
from .models import *

# Base Serializer for Common Fields
class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True

class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CampaignOwnerSerializer(BaseSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Campaign_Owner
        fields = '__all__'

class DonorSerializer(BaseSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Donor
        fields = '__all__'