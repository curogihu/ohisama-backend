from rest_framework import serializers
from api.models import TVer, Member

class MemberSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name']

class TVerSerializer(serializers.ModelSerializer):
    members = MemberSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = TVer
        fields = '__all__'