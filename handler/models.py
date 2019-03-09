from django.db import models
from django.contrib.auth.models import User


# class AccessToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, null=True)
#     token = models.CharField(max_length=100000,unique= True)
#     # def __str__(self):
#     #     return self.user.username
#
#
class Webhook(models.Model):
    data =models.CharField(max_length=50000)


# class SpreadSheet(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)#this can be the Access Token
#     sheet_id = models.CharField(max_length=500)
#
# class Worksheet(models.Model):
#     spread_sheet = models.ForeignKey(SpreadSheet, on_delete = models.CASCADE, null=True)
#     index = models.IntegerField(null=True)
#     max_row = models.IntegerField()
#
#
# class SasSSheetMap(models.Model):
#     jira_actions = models.ForeignKey(SasSActions, on_delete=models.CASCADE, default='', unique=True)
#     sheet_actions = models.ForeignKey(SheetActions, on_delete=models.CASCADE, default='')
#     sheet_id = models.CharField(max_length=100)  # it should be unique
#     # worksheet_id = models.CharField(max_length=3)
#     # last_row_update = models.CharField(max_length=3)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')
#
#     def __str__(self):
#         return self.jira_actions.action
#
#     class Meta:
#         verbose_name_plural = "SasS SheetMap"
#
#
#
#
#
#
#
#

class JiraSetup(models.Model):

    url = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, null=True)

    def __str__(self):
        return self.url


class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, null=True)
    url = models.CharField(max_length=100,null=True)
    token = models.CharField(max_length=100000)

    def __str__(self):
        return self.user.username


class SasSActions(models.Model):
    action = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name_plural = "SasS Actions"


class SheetActions(models.Model):
    action = models.CharField(max_length=100)
    details = models.CharField(max_length=100)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name_plural = 'Sheet Actions'


class SasSSheetMap(models.Model):
    jira_actions = models.ForeignKey(SasSActions, on_delete=models.CASCADE, default='', unique=True)
    sheet_actions = models.ForeignKey(SheetActions, on_delete=models.CASCADE, default='')
    sheet_id = models.CharField(max_length=100)  # it should be unique
    # worksheet_id = models.CharField(max_length=3)
    # last_row_update = models.CharField(max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')

    def __str__(self):
        return self.jira_actions.action

    class Meta:
        verbose_name_plural = "SasS SheetMap"


