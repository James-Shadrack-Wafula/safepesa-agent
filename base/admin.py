from django.contrib import admin
from . models import QRCodeScan,Student,TransactionHistory, Parent
# Register your models here.
admin.site.register(QRCodeScan)
admin.site.register(Student)
admin.site.register(TransactionHistory)
admin.site.register(Parent)
# admin.site.register(Attendance)
