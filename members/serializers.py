from rest_framework import serializers
from members.models import Member

class MemberSerializer(serializers.Serializer):
    class Meta:
        model = Member
        exclude = ['member_id']