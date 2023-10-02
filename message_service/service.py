from message_service.models import User,Coupon,PromotionalMessage
from message_service.enums import AnswerEnum,GenderEnum
from django.db.models import Count,Q
from django.utils import timezone
import uuid

class UserService():
    def get_users(self):
        '''Returns all user information from database'''
        user_list = list(User.objects.filter())
        
        if user_list:
            return user_list
        
        return None
        
    
class CouponService():
    def get_coupon(self,coupon_id: int):
        '''Returns the coupon information'''
        try:
            return Coupon.objects.get(id=coupon_id)
        
        except Coupon.DoesNotExist:
            return None            


class PromotionalMessageService():
    def save_promotional_messages(self,user_list: list[User],coupon: Coupon):
        '''Save sent message records for all users in the database'''
        message_list = []
        for user in user_list:
            promotion_message_id = uuid.uuid4()    
            message_list.append(PromotionalMessage(message_id=promotion_message_id,user_id = user,coupon_id = coupon))
        
        PromotionalMessage.objects.bulk_create(message_list)
        saved_records = [record for record in message_list if record.pk is not None]

        if not saved_records:
            raise Exception("Error to save records")


    def update_message_anwser(self,message_id:str , message_anwser: str):
        '''Update the client's message answer '''
        updated_register = PromotionalMessage.objects.filter(message_id = message_id).update(answer=AnswerEnum[message_anwser],data_answered=timezone.now())
        
        if updated_register == 0:
            return None 
        
        return "Updated answer"   
    
    
    def get_promotional_message(cls, message_id: str) -> PromotionalMessage: 
        '''Returns promotional message details along with user and coupon-related data.'''
        try:
            return PromotionalMessage.objects.filter(message_id = message_id).select_related('coupon_id','user_id').get()   
        except PromotionalMessage.DoesNotExist:
            return None
        

class StatisticService():
    def get_promotional_message_statistics(self, coupon_id: int|None, gender: str|None):
        '''Returns the promotional message statistics based on request filters passed'''
        response = {'filters': {}, 'data': {}}

        message_queryset = PromotionalMessage.objects.all()
        if gender is not None:
            message_queryset = message_queryset.filter(user_id__gender=GenderEnum[gender])
            response['filters']['gender'] = str.capitalize(gender)
        
        if coupon_id is not None:
            response['filters']['coupon_id'] = coupon_id
            message_queryset = message_queryset.filter(coupon_id=coupon_id)

        message_registers = message_queryset.values('coupon_id').annotate(accepted=Count('message_id',filter=Q(answer=AnswerEnum.ACCEPTED)),
                not_answered=Count('message_id',filter=Q(answer=AnswerEnum.NOT_ANSWERED)),
                declined=Count('message_id',filter=Q(answer=AnswerEnum.DECLINED))).order_by('coupon_id')
        
        response['data'] = [entry for entry in message_registers]

        return response


        