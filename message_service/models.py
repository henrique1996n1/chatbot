from django.conf import settings
from django.utils import timezone
from django.db import models
from message_service.enums import AnswerEnum,GenderEnum

class User(models.Model): 
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1,choices=GenderEnum.choices)
    
class Coupon(models.Model):
    description = models.CharField(max_length=150)
    promotional_code = models.CharField(max_length=20)
    percentage = models.IntegerField(default=0)
    declined_coupon_image_link = models.CharField(max_length=300,default="https://cdn.beehappyeveryday.com/images/ci/8/have-a-wonderful-day-quotes-and-images.webp")
    
class PromotionalMessage(models.Model):
    message_id = models.CharField(max_length=20,primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
    coupon_id = models.ForeignKey(Coupon,on_delete=models.CASCADE,db_column='coupon_id')
    answer = models.CharField(max_length=2,default=AnswerEnum.NOT_ANSWERED,choices=AnswerEnum.choices)
    data_sent = models.DateTimeField(default=timezone.now)
    data_answered = models.DateTimeField(null=True) 