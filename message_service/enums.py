from django.db import models

class GenderEnum(models.TextChoices):
    MALE = "M" 
    FEMALE = "F" 

class AnswerEnum(models.TextChoices):
    DECLINED = "D" 
    NOT_ANSWERED = "NA" 
    ACCEPTED = "A" 