import message_service.service as services
from unittest import TestCase
from message_service.tests.conftest import ConftestModels

class PromotionalMessageServiceTest(TestCase):
    def setUp(self):
        ConftestModels.mock_user_register_object().save()
        ConftestModels.mock_coupon_register_object().save()
        ConftestModels.mock_promotional_message_register_object().save()
        
    def test_getPromotionalMessage_messageNotFound_returnsEmptyObject(self):
        response = services.PromotionalMessageService().get_promotional_message("not_existente_message_id_value")
        
        self.assertEqual(response,None)


    def test_getPromotionalMessage_messageFound_returnsMessageObject(self):
        response_expected = ConftestModels.mock_promotional_message_register_object()
                
        response = services.PromotionalMessageService().get_promotional_message(response_expected.message_id)

        self.assertEqual(response,response_expected)

    def test_updateMessageAnwser_messageNotFound_returnsEmptyObject(self):
        answer = "ACCEPTED"
        response_expected = None
        response = services.PromotionalMessageService().update_message_anwser("not_existente_message_id_value", answer)
        
        self.assertEqual(response,response_expected)


    def test_updateMessageAnwser_messageFound_returnsMessageObject(self):
        message_register = ConftestModels.mock_promotional_message_register_object()
        answer = "ACCEPTED"
        response_expected = "Updated answer"
        response = services.PromotionalMessageService().update_message_anwser(message_register.message_id, answer)
        
        self.assertEqual(response,response_expected)
        
    def test_savePromotionalMessages_errorToSaveMessage_returnsException(self):
        with self.assertRaises(Exception):
            response = services.PromotionalMessageService().save_promotional_messages([ConftestModels.mock_user_register_object()],
                                                                             "Invalid coupon")
    


    def test_savePromotionalMessages_messageSavedCorrect(self):
        response_expected = "messages saved"
        response = services.PromotionalMessageService().save_promotional_messages([ConftestModels.mock_user_register_object()],
                                                                    ConftestModels.mock_coupon_register_object())
        
        assert (response, response_expected)
        

class CouponServiceTest(TestCase):
    def setUp(self):
        ConftestModels.mock_coupon_register_object().save()
        
    def test_getCoupon_couponNotFound_returnsNone(self):
        response_expected = None
        response = services.CouponService().get_coupon("23")
        
        self.assertEqual(response,response_expected)

    def test_getCoupon_couponFound_returnsCouponObject(self):
        response_expected = ConftestModels.mock_coupon_register_object()
        
        response = services.CouponService().get_coupon(response_expected.id)
        
        self.assertEqual(response,response_expected)

class UserServiceTest(TestCase):
    def test_getUsers_userFound_returnsUserObjectList(self):
        user_register = ConftestModels.mock_user_register_object()
        user_register.save()
        response_expected = [user_register]
        
        response = services.UserService().get_users()

        self.assertEqual(response,response_expected)
        
        
class PromotionalStatisticsServiceTest(TestCase):
    user_1 = ConftestModels.mock_user_register_object()
    user_2 = ConftestModels.mock_user_register_object()
    user_2.gender = "F"
    user_1.save()
    user_2.save()
    
    coupon_1 = ConftestModels.mock_coupon_register_object()
    coupon_2 = ConftestModels.mock_coupon_register_object()
    coupon_1.save()
    coupon_2.save()
    
    message_register_1= ConftestModels.mock_promotional_message_register_object()
    message_register_2 = ConftestModels.mock_promotional_message_register_object()
    message_register_2.user_id = user_2
    message_register_2.coupon_id = coupon_2
    message_register_1.save()
    message_register_2.save()
    
    def test_getPromotionalMessageStatistics_NoFiltersApplied_returnAllStatistics(self):
        response_expected = {'filters': {}, 'data': [{'coupon_id': 1, 'accepted': 0, 'not_answered': 2, 'declined': 0}]}
        
        response = services.StatisticService().get_promotional_message_statistics(None,None)
        
        self.assertEqual(response,response_expected) 

    def test_getPromotionalMessageStatistics_genderFilterApplied_returnStatisticsFilteredByGender(self):
        gender = "MALE"
        response_expected = {'filters': {'gender': str.capitalize(gender)}, 'data': [{'coupon_id': 1, 'accepted': 0, 'not_answered': 2, 'declined': 0}]}
        
        response = services.StatisticService().get_promotional_message_statistics(None,gender)
        self.assertEqual(response,response_expected) 

    def test_getPromotionalMessageStatistics_couponFilterApplied_returnStatisticsFilteredByCoupon(self):
        coupon_id = 1
        response_expected = {'filters': {'coupon_id': 1}, 'data': [{'coupon_id': 1, 'accepted': 0, 'not_answered': 2, 'declined': 0}]}
        
        response = services.StatisticService().get_promotional_message_statistics(coupon_id,None)
        self.assertEqual(response,response_expected) 
    
    