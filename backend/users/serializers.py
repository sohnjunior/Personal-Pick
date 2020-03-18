from rest_framework import serializers

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomRegisterSerializer(RegisterSerializer):
    GENDER_CHOICES = (
        ('m', '남성'),
        ('f', '여성'),
        ('o', '알수없음'),
    )
    username = None
    nickname = serializers.CharField(max_length=30, allow_blank=True)
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, default='o')

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict.pop('username')  # username 필드는 필요없으므로 삭제
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['date_of_birth'] = self.validated_data.get('date_of_birth', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        return data_dict

