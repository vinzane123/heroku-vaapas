from django.db import models

# Create your models here.
class User(models.Model):
    phone = models.CharField(max_length=15, primary_key=True)
    otp = models.CharField(max_length=9, blank=True,null=True)
    validated = models.BooleanField(default=False,help_text='If true, user has validated otp in second API')
    timeStamp = models.DateTimeField(auto_now_add=True)
    timeCounter = models.FloatField(null=True,blank=True,verbose_name='timer')

    def __str__(self):
        return self.phone

class UserData(models.Model):
    phone = models.ForeignKey(User, on_delete=models.CASCADE)
    smsData = models.TextField(blank=True,null=True)
    callLogs = models.TextField(blank=True,null=True)
    contactList = models.TextField(blank=True,null=True)
    permissionGiven = models.BooleanField()
    interested = models.BooleanField(default=False)
    Responses = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.phone.phone + '-' + str(self.permissionGiven)



