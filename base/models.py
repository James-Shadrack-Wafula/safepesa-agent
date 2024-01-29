from typing import Any
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

# Create your models here.
class QRCodeScan(models.Model):
    data = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    class_name = models.CharField(max_length=50)
    student_adm = models.CharField(max_length=200, null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    cumilative_deposit = models.IntegerField(null=True, blank=True, default=balance)
    cumilative_withdraw = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


    # def save(self, *args, **kwargs):
    #     # Generate QR code and save it as an image
    #     qr = qrcode.QRCode(
    #         version=1,
    #         box_size=10,
    #         border=5,
    #     )
    #     qr.add_data(self.student_adm)
    #     qr.make(fit=True)

    #     img = qr.make_image(fill_color="black", back_color="white")
    #     buffer = BytesIO()
    #     img.save(buffer)
    #     self.image.save(f'{self.student_adm}_qr.png', File(buffer), save=False)

    #     super().save(*args, **kwargs)
    

# @receiver(post_save, sender=Student)
# def student_balance_updated(sender, instance, **kwargs):
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'balance_updates_group',
#             {
#                 'type': 'send_balance_update',
#                 'student_id': instance.id,
#                 'balance': instance.balance,
#             }
#         )
    
class TransactionHistory(models.Model,):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    init_balance = models.IntegerField(default=0)
    new_balance = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=50, default="Undefined")
    transacted_amount = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Format the time before saving
        if self.time:
            self.time_formatted = self.time.strftime('%d/%m/%Y : %H:%M')
        super().save(*args, **kwargs)
    # Format time to be in the british format ie. x/x/xxxx

    # def __init__(self,*args: Any, **kwargs: Any) -> None:
    #     self.init_balance = self.student.balance
    #     super().__init__(*args, **kwargs)
    #     self.student
    def __str__(self):
        return self.student.name

class Parent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    students = models.ManyToManyField(Student, related_name='parents')
    parents_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class RollCall(models.Model):
    students = models.ManyToManyField(Student)
    # RollCall status 
    # 
# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateField()
#     present = models.BooleanField(default=False)
#     time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.student.name

    
