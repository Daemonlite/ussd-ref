from django.db import models

# Create your models here.

class Users(models.Model):
    userid = models.CharField(db_column='USERID', primary_key=True, max_length=200)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mobileno = models.IntegerField(db_column='MOBILENO', blank=True, null=True)  # Field name made lowercase.
    lastlogin = models.DateTimeField(db_column='LASTLOGIN', blank=True, null=True)  # Field name made lowercase.
    userstatus = models.CharField(db_column='USERSTATUS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    authstatus = models.CharField(db_column='AUTHSTATUS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    otp_datecreated = models.DateTimeField(db_column='OTP_DATECREATED', blank=True, null=True)  # Field name made lowercase.
    otp = models.CharField(db_column='OTP', max_length=500, blank=True, null=True)  # Field name made lowercase.
    otp_method = models.CharField(db_column='OTP_METHOD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    loginattempts = models.IntegerField(db_column='LOGINATTEMPTS', blank=True, null=True)  # Field name made lowercase.
    lastloginweb = models.DateTimeField(db_column='LASTLOGINWEB', blank=True, null=True)  # Field name made lowercase.
    lastloginmobile = models.DateTimeField(db_column='LASTLOGINMOBILE', blank=True, null=True)  # Field name made lowercase.
    creationchannel = models.CharField(db_column='CREATIONCHANNEL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    makerid = models.CharField(db_column='MAKERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    authid = models.CharField(db_column='AUTHID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    makedatetime = models.DateTimeField(db_column='MAKEDATETIME', blank=True, null=True)  # Field name made lowercase.
    authdatetime = models.DateTimeField(db_column='AUTHDATETIME', blank=True, null=True)  # Field name made lowercase.
    passwordexpirydate = models.DateTimeField(db_column='PASSWORDEXPIRYDATE', blank=True, null=True)  # Field name made lowercase.
    passwordresetdays = models.IntegerField(db_column='PASSWORDRESETDAYS', blank=True, null=True)  # Field name made lowercase.
    customer_number = models.CharField(db_column='CUSTOMER_NUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    account_number = models.CharField(db_column='ACCOUNT_NUMBER', max_length=30, blank=True, null=True)  # Field name made lowercase.
    registrationdate = models.DateField(db_column='REGISTRATIONDATE', blank=True, null=True)  # Field name made lowercase.
    no_of_d_trans = models.IntegerField(db_column='NO_OF_D_TRANS', blank=True, null=True)  # Field name made lowercase.
    value_of_d_trans = models.FloatField(db_column='VALUE_OF_D_TRANS', blank=True, null=True)  # Field name made lowercase.
    max_val_trans = models.FloatField(db_column='MAX_VAL_TRANS', blank=True, null=True)  # Field name made lowercase.
    user_trans_settings = models.CharField(db_column='USER_TRANS_SETTINGS', max_length=75, blank=True, null=True)  # Field name made lowercase.
    ussd_pin = models.CharField(db_column='USSD_PIN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ussd_sub = models.CharField(db_column='USSD_SUB', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inter_bank_sub = models.CharField(db_column='INTER_BANK_SUB', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERS'


class UssdLog(models.Model):
    sessionid = models.CharField(db_column='SESSIONID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    message_type = models.IntegerField(db_column='MESSAGE_TYPE', blank=True, null=True)  # Field name made lowercase.
    body = models.CharField(db_column='BODY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CUSTNO', max_length=18, blank=True, null=True)  # Field name made lowercase.
    stage = models.IntegerField(db_column='STAGE', blank=True, null=True)  # Field name made lowercase.
    selected_account = models.CharField(db_column='SELECTED_ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    selected_amount = models.CharField(db_column='SELECTED_AMOUNT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    rec_account = models.CharField(db_column='REC_ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    accounts = models.CharField(db_column='ACCOUNTS', max_length=1400, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USSD_LOG'


class UssdScreen(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SESSIONID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CUSTNO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='LEVEL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USSD_SCREEN'


class UssdSession(models.Model):
    # tid = models.AutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    body = models.CharField(db_column='BODY', max_length=500, blank=True, null=True)  # Field name made lowercase.
    date_created = models.DateField(db_column='DATE_CREATED', blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USSD_SESSION'


class Custaccount(models.Model):
    tid = models.BigAutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    accountno = models.CharField(db_column='ACCOUNTNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CUSTNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='USERID', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CUSTACCOUNT'

    def __str__(self):
        return self.accountno

class Love(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.name