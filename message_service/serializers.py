from rest_framework import serializers
from message_service.enums import AnswerEnum,GenderEnum
from rest_framework.exceptions import ValidationError

class SendMessageRequestSerializer(serializers.Serializer):
    coupon_id = serializers.IntegerField(required=True)

class PromotionStatisticsRequestSerializer(serializers.Serializer):
    gender = serializers.CharField(max_length=6,required=False)
    coupon_id = serializers.IntegerField(default=None)
    
    def to_internal_value(self, data):
        if 'gender' in data: 
            if str.upper(data['gender']) not in [member.name for member in GenderEnum]:
                raise ValidationError({'gender': "The unique valid values to the answer field are 'Male' or 'Female'"})
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'gender' in data: 
            data['gender'] = str.upper(data['gender'])
        else: 
            data['gender']= None
        return data

class UpdateCouponAnswerRequestSerializer(serializers.Serializer):
    message_id = serializers.CharField(required=True)
    message_answer = serializers.CharField(required=True)

    def to_internal_value(self, data):
        if 'message_answer' not in data: 
            raise ValidationError({'message_answer': ["This field is required."]})
        
        if str.upper(data['message_answer']) not in [member.name for member in AnswerEnum]:
            raise ValidationError({'message_answer': "The unique valid values to the answer field are 'Accepted', 'Declined' or 'Not_Answered'"})
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['message_answer'] = str.upper(data['message_answer'])
        return data

class OpenCouponMessageRequestSerializer(serializers.Serializer):
    message_id = serializers.CharField(required=True)