import json
from django.test import TestCase
from message_service.models import PromotionalMessage
from message_service.views import StatisticsView
from django.test import RequestFactory
from rest_framework.test import APIClient
from unittest.mock import patch
from message_service.errors import Error
from rest_framework import status
from message_service.tests.conftest import ConftestModels, ConftestViews

class UpdateAnswerEndpointTest(TestCase):
    def setUp(self):
        self.client =  APIClient()
        ConftestModels.mock_user_register_object().save()
        ConftestModels.mock_coupon_register_object().save()
        self.promotional_message_register = ConftestModels.mock_promotional_message_register_object()
        self.promotional_message_register.save()
        self.update_answer_request_data = {'message_id': self.promotional_message_register.message_id,'message_answer': "declined"}
      
        
    def test_updateAnswerEndpoint_invalidRequestParameters_returnsBadRequest(self):
        invalid_data = {"invalid_field": "invalid_value"}         
              
        response = self.client.get('/updateAnswer/',data= invalid_data)    
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_updateAnswerEndpoint_invalidMessageAnswerValue_returnsBadRequest(self):
        self.update_answer_request_data['message_answer'] = "invalid_value"         
        response = self.client.get('/updateAnswer/',data= self.update_answer_request_data)    
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    @patch('message_service.service.PromotionalMessageService.update_message_anwser',side_effect=Exception("Error to connect into database"))
    def test_updateAnswerEndpoint_failToAcessDatabase_returnException(self,mock_update_message_anwser):
        response_expected = Error.INTERNAL_SERVER_ERROR

        response = self.client.get('/updateAnswer/',data= self.update_answer_request_data)    
        response_content = response.json()    
        
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content,response_expected)

    @patch('message_service.service.PromotionalMessageService.update_message_anwser',return_value=None)
    def test_updateAnswerEndpoint_promotionalMessageNotFound_returnsNotFoundError(self,mock_update_message_anwser):
        response_expected = Error.MESSAGE_NOT_FOUND

        response = self.client.get('/updateAnswer/',data= self.update_answer_request_data)    
        response_content = response.json()    
        
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_content,response_expected)

    @patch('message_service.service.PromotionalMessageService.update_message_anwser')
    def test_UpdateAnswerEndpoint_EverythingWorks_ReturnsValidResponse(self,mock_update_message_anwser):
        mock_update_message_anwser.return_value = self.promotional_message_register

        response = self.client.get('/updateAnswer/',data= self.update_answer_request_data) 

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)        
        

class SendMessageEndpointTest(TestCase):
    def setUp(self):
        self.client =  APIClient()
        self.body = json.loads('{"coupon_id": 1}')
        
    def test_sendMessageEndpoint_invalidRequestParameters_returnsInternalServerError(self):
        self.body = {"invalid_field": "1"}         
              
        response = self.client.post('/sendMessage/',data= self.body, content_type='application/json')        

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    @patch('message_service.service.UserService.get_users',return_value=None)   
    def test_sendMessageEndpoint_notUserFoundInDatabase_returnNotFoundUser(self,mock_user_query):
        response_expected = Error.USER_NOT_FOUND
        
        response = self.client.post('/sendMessage/',data= self.body)        

        response_content = response.json()

        self.assertEqual(response_content,response_expected)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    @patch('message_service.service.UserService.get_users',return_value=ConftestModels.mock_user_register_object())    
    @patch('message_service.service.CouponService.get_coupon',return_value=None)    
    def test_sendMessageEndpoint_notCouponFoundInDatabase_returnNotFoundUser(self,mock_coupon_service,mock_user_service):
        
        response_expected = Error.COUPON_NOT_FOUND
        
        response = self.client.post('/sendMessage/',data= self.body)        

        
        response_content = response.json()

        self.assertEqual(response_content,response_expected)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    @patch('message_service.service.UserService.get_users',side_effect=Exception("Error to connect into database"))
    def test_sendMessageEndpoint_failToAcessDatabase_returnsException(self,mock_user_service):
        response_expected = Error.INTERNAL_SERVER_ERROR
        
        response = self.client.post('/sendMessage/',data= self.body)        

        response_content = response.json()

        self.assertEqual(response_content,response_expected)
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch('message_service.service.UserService.get_users',return_value=ConftestModels.mock_user_register_object())
    @patch('message_service.service.CouponService.get_coupon',return_value=ConftestModels.mock_coupon_register_object())       
    @patch('message_service.service.PromotionalMessageService.save_promotional_messages',side_effect=Exception("Error to connect into database"))      
    def test_sendMessageEndpoint_failToSavePromotionalMessageIntoDatabase_returnException(self,mock_save_promotional_message_service,mock_coupon_service,mock_user_service):
        
        response_expected = Error.INTERNAL_SERVER_ERROR
        
        response = self.client.post('/sendMessage/',data= self.body)        

        
        response_content = response.json()

        self.assertEqual(response_content,response_expected)
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch('message_service.service.UserService.get_users',return_value=ConftestModels.mock_user_register_object())
    @patch('message_service.service.CouponService.get_coupon',return_value=ConftestModels.mock_coupon_register_object())     
    @patch('message_service.service.PromotionalMessageService.save_promotional_messages',return_value="Ok")      
    def test_sendMessageEndpoint_EverythingWorks_ReturnsValidResponse(self,mock_save_promotional_message_service,mock_coupon_service,mock_user_service):
        
        response = self.client.post('/sendMessage/',data= self.body)        
    

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

       
class PromotionalStatisticsTest(TestCase):
    def setUp(self):
        self.client =  APIClient()
        self.body = {"gender": "Male", "coupon_id": 1}
    
    @patch('message_service.service.StatisticService.get_promotional_message_statistics',side_effect=Exception("Error to connect into database"))
    def test_promotionalStatistics_failToAcessDatabase_returnsException(self,mock_get_promotional_message_statistics):
        response_expected = Error.INTERNAL_SERVER_ERROR

        response = self.client.get('/promotionalStatistics/',data= self.body)
        response_content = response.json()    
        
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content,response_expected)

    @patch('message_service.service.StatisticService.get_promotional_message_statistics',return_value=ConftestViews.mock_statistics_response_dict())
    def test_promotionalStatistics_EverythingWorks_ReturnsValidResponse(self,mock_get_promotional_message_statistics):
        response_expected = ConftestViews.mock_statistics_response_dict()

        response = self.client.get('/promotionalStatistics/',data= self.body)    
        response_content = response.json()

        self.assertEqual(response_content,response_expected)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class GenerateMessageEndpointTest(TestCase):
    def setUp(self):
        self.client =  APIClient()
        ConftestModels.mock_user_register_object().save()
        ConftestModels.mock_coupon_register_object().save()
        self.promotional_message_register = ConftestModels.mock_promotional_message_register_object()
        self.promotional_message_register.save()
        self.generate_message_request_data = {'message_id': self.promotional_message_register.message_id}
      
        
    def test_generateMessageEndpoint_invalidRequestParameters_returnsBadRequest(self):
        invalid_data = {"invalid_field": "invalid_value"}         
              
        response = self.client.get('/generateMessage/',data= invalid_data)    
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    @patch('message_service.service.PromotionalMessageService.get_promotional_message',return_value=None)
    def test_generateMessageEndpoint_promotionalMessageNotFound_returnsNotFoundError(self,mock_get_promotional_message):
        response_expected = Error.MESSAGE_NOT_FOUND
        self.generate_message_request_data = {"message_id": "not_existent_value"}
        
        response = self.client.get('/generateMessage/',data= self.generate_message_request_data)    
        response_content = response.json()    
        
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_content,response_expected)

    @patch('message_service.service.PromotionalMessageService.get_promotional_message',side_effect=Exception("Error to connect into database"))
    def test_generateMessageEndpoint_failToAcessDatabase_returnsException(self,mock_get_promotional_message):
        response_expected = Error.INTERNAL_SERVER_ERROR

        response = self.client.get('/generateMessage/',data= self.generate_message_request_data)    
        response_content = response.json()    
        
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content,response_expected)


    @patch('message_service.service.PromotionalMessageService.get_promotional_message')
    def test_generateMessageEndpoint_everythingWorks_returnsValidResponse(self,mock_get_promotional_message):
        mock_get_promotional_message.return_value = self.promotional_message_register

        response = self.client.get('/generateMessage/',data= self.generate_message_request_data) 

        self.assertEqual(response.status_code,status.HTTP_200_OK)