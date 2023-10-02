import json
import message_service.serializers as serializers 
from rest_framework import generics,status 
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from message_service.service import UserService,CouponService,PromotionalMessageService,StatisticService
from rest_framework.exceptions import ValidationError
from message_service.errors import Error
import logging 
    
class PromotionalMessageView(generics.ListAPIView):
    def get (self,request):
        '''Allows clients to update their message answers, modifying their responses to messages'''
        serializer = serializers.UpdateCouponAnswerRequestSerializer(data=request.query_params)  #arrumar isso após escrever os testes    
        try:
            serializer.is_valid(raise_exception=True)
            request_data = serializer.data 

            updated_answer = PromotionalMessageService().update_message_anwser(request_data['message_id'], request_data['message_answer'])
            if not updated_answer:
                return JsonResponse(Error.MESSAGE_NOT_FOUND, 
                        status = Error.MESSAGE_NOT_FOUND['status_code'])
                
            return HttpResponse(status = status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            error_response = Error.INVALID_REQUEST_PARAMETER
            error_response['reason'] = e.detail
            return JsonResponse(error_response, status = error_response['status_code'])       
        
        except Exception as e:
                logging.error(f"{str(e)}'")
                return JsonResponse(Error.INTERNAL_SERVER_ERROR, 
                                    status = Error.INTERNAL_SERVER_ERROR['status_code'])
        
       
    def post(self, request):
        serializer = serializers.SendMessageRequestSerializer(data=request.data)  
        try:
            serializer.is_valid(raise_exception=True)
            request_data = serializer.data 
            
            users_data = UserService().get_users()  
            if not users_data:
                return JsonResponse(Error.USER_NOT_FOUND, 
                                    status = Error.USER_NOT_FOUND['status_code'])
            
            coupon_data = CouponService().get_coupon(request_data['coupon_id'])
            if not coupon_data:
                return JsonResponse(Error.COUPON_NOT_FOUND, 
                                    status = Error.COUPON_NOT_FOUND['status_code'])
        
            PromotionalMessageService().save_promotional_messages(users_data,coupon_data)
            return HttpResponse(status = status.HTTP_204_NO_CONTENT)
        
        except ValidationError as e:
            error_response = Error.INVALID_REQUEST_PARAMETER
            error_response['reason'] = e.detail
            return JsonResponse(error_response, status = error_response['status_code'])      
        
        except Exception as e:
                logging.error(f"protocol:'POST', endpoint:'/sendMessage', message:  {str(e)}'")
                return JsonResponse(Error.INTERNAL_SERVER_ERROR, 
                                    status = Error.INTERNAL_SERVER_ERROR['status_code'])
            

class PromotionalMessageRepresentationView(generics.ListAPIView):
    def get(self,request):
        '''Displays the promotional message interface and manages user interaction with the promotional flow.'''
        serializer = serializers.OpenCouponMessageRequestSerializer(data=request.query_params)  
        try:
            serializer.is_valid(raise_exception=True)
            request_data = serializer.data 
            message_information  = PromotionalMessageService().get_promotional_message(request_data['message_id'])
            if not message_information:
                return JsonResponse(Error.MESSAGE_NOT_FOUND, 
                                     status = Error.MESSAGE_NOT_FOUND['status_code'])
            
            template_information = {
                'message_id': message_information.message_id,
                'coupon_percentage':message_information.coupon_id.percentage,
                'user_name': message_information.user_id.name,
                'declined_message_link': message_information.coupon_id.declined_coupon_image_link,
                'promotional_code': message_information.coupon_id.promotional_code,
            }
            
            return render(request, 'template.html',template_information)
  
        except ValidationError as e:
            error_response = Error.INVALID_REQUEST_PARAMETER
            error_response['reason'] = e.detail
            return JsonResponse(error_response, status = error_response['status_code'])       
        
        except Exception as e:
            logging.error(f"protocol:'GET', endpoint:'/generateMessage', message: 'Error to generate the message template: {str(e)}'")
            return JsonResponse(Error.INTERNAL_SERVER_ERROR, status = Error.INTERNAL_SERVER_ERROR['status_code'])
        
        
class StatisticsView(generics.ListAPIView):
        def get(self,request):
            try:
                serializer = serializers.PromotionStatisticsRequestSerializer(data=request.query_params)  
                serializer.is_valid(raise_exception=True)
                request_data = serializer.data 
               
                statistic_data = StatisticService().get_promotional_message_statistics(request_data['coupon_id'],request_data['gender'])
            
            except ValidationError as e:
                error_response = Error.INVALID_REQUEST_PARAMETER
                error_response['reason'] = e.detail
                return JsonResponse(error_response, status = error_response['status_code'])       
            
            except Exception as e:
                logging.error(f"protocol:'GET', endpoint:'/promotionalStatistics', message: 'Error to get information from database: {str(e)}'")
                return JsonResponse(Error.INTERNAL_SERVER_ERROR, 
                                status = Error.INTERNAL_SERVER_ERROR['status_code']) 

            return JsonResponse(statistic_data, status = status.HTTP_200_OK, safe=False)
        
    