from datetime import datetime, timedelta
import message_service.models as models
from django.utils import timezone

class ConftestModels():
    def mock_user_register_dict():
      return {
        "id": 1,
        "name": "Tonny stark",
        "phone_number": "123-456-7890",
        "gender": "M"
      }

    def mock_user_register_object():
        return models.User(**ConftestModels.mock_user_register_dict())

    def mock_coupon_register_dict():
      return {
        "id":1,  
        "description": "Free shipping on orders over $50",
        "promotional_code": "FREE50",
        "percentage": 20
      }
    
    def mock_coupon_register_object():
        return models.Coupon(**ConftestModels.mock_coupon_register_dict())
      
    def mock_promotional_message_register_dict():
      return {   
        'message_id': '2c704a32-9f89-47e7-9e38-769c19eaadf9', 
        'user_id': ConftestModels.mock_user_register_object(), 
        'coupon_id': ConftestModels.mock_coupon_register_object(), 
        'answer': 'NA', 
        'data_sent': timezone.make_aware(datetime(2023, 10, 1, 13, 6, 34, 741500)),
        'data_answered': timezone.make_aware(datetime(2023, 10, 1, 13, 6, 34, 741500)+ timedelta(minutes=20))
      }
      
    def mock_promotional_message_register_object():
        return models.PromotionalMessage(**ConftestModels.mock_promotional_message_register_dict())
    
class ConftestViews():
  def mock_statistics_response_dict():
      return {
        "coupon_id": 1,
        "accepted": 4,
        "not_answered": 4,
        "declined": 0
      }
      
  
      