# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Beneficiary(models.Model):
    beneficiaryid = models.AutoField(db_column='BENEFICIARYID', primary_key=True)  # Field name made lowercase.
    beneficiarytype = models.CharField(db_column='BENEFICIARYTYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customer_number = models.CharField(db_column='CUSTOMER_NUMBER', max_length=200, blank=True, null=True)  # Field name made lowercase.
    accountname = models.CharField(db_column='ACCOUNTNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='BANKCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BRANCHCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    accountnumber = models.CharField(db_column='ACCOUNTNUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mobilenumber = models.CharField(db_column='MOBILENUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DATECREATED', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.DateTimeField(db_column='DATEUPDATED', blank=True, null=True)  # Field name made lowercase.
    network = models.CharField(db_column='NETWORK', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BENEFICIARY'
        unique_together = (('accountnumber', 'customer_number'),)


class BlockedRegistration(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    accountno = models.CharField(db_column='ACCOUNTNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    no_of_attempts = models.IntegerField(db_column='NO_OF_ATTEMPTS', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BLOCKED_REGISTRATION'


class Custaccount(models.Model):
    tid = models.BigAutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    accountno = models.CharField(db_column='ACCOUNTNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CUSTNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cr_no_of_d_trans = models.IntegerField(db_column='CR_NO_OF_D_TRANS', blank=True, null=True)  # Field name made lowercase.
    cr_value_of_d_trans = models.DecimalField(db_column='CR_VALUE_OF_D_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cr_max_val_trans = models.DecimalField(db_column='CR_MAX_VAL_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dr_no_of_d_trans = models.IntegerField(db_column='DR_NO_OF_D_TRANS', blank=True, null=True)  # Field name made lowercase.
    dr_value_of_d_trans = models.DecimalField(db_column='DR_VALUE_OF_D_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dr_max_val_trans = models.DecimalField(db_column='DR_MAX_VAL_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    default_custom = models.CharField(db_column='DEFAULT_CUSTOM', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CUSTACCOUNT'


class EmailSettings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    port = models.CharField(db_column='PORT', max_length=6, blank=True, null=True)  # Field name made lowercase.
    use_ssl = models.CharField(db_column='USE_SSL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    host = models.CharField(db_column='HOST', max_length=70, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EMAIL_SETTINGS'


class Enterprisesettings(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    cr_no_of_d_trans = models.IntegerField(db_column='CR_NO_OF_D_TRANS', blank=True, null=True)  # Field name made lowercase.
    dr_no_of_d_trans = models.IntegerField(db_column='DR_NO_OF_D_TRANS', blank=True, null=True)  # Field name made lowercase.
    cr_value_of_d_trans = models.DecimalField(db_column='CR_VALUE_OF_D_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dr_value_of_d_trans = models.DecimalField(db_column='DR_VALUE_OF_D_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cr_max_val_trans = models.DecimalField(db_column='CR_MAX_VAL_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dr_max_val_trans = models.DecimalField(db_column='DR_MAX_VAL_TRANS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    no_of_trans_show = models.IntegerField(db_column='NO_OF_TRANS_SHOW', blank=True, null=True)  # Field name made lowercase.
    trans_otp_exp_time = models.IntegerField(db_column='TRANS_OTP_EXP_TIME', blank=True, null=True)  # Field name made lowercase.
    passwd_exp_days = models.IntegerField(db_column='PASSWD_EXP_DAYS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENTERPRISESETTINGS'


class Entuserroles(models.Model):
    roleid = models.CharField(db_column='ROLEID', primary_key=True, max_length=50)  # Field name made lowercase.
    rolename = models.CharField(db_column='ROLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENTUSERROLES'


class Goals(models.Model):
    id = models.AutoField()
    customer_number = models.CharField(max_length=50, blank=True, null=True)
    narration = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GOALS'


class Logs(models.Model):
    id = models.AutoField()
    enc_body = models.CharField(max_length=500, blank=True, null=True)
    header = models.CharField(max_length=500, blank=True, null=True)
    decr_body = models.CharField(max_length=500, blank=True, null=True)
    auth_status = models.CharField(max_length=500, blank=True, null=True)
    response = models.CharField(max_length=500, blank=True, null=True)
    narration = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LOGS'


class Otps(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    cust_number = models.CharField(db_column='CUST_NUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='METHOD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    narration = models.CharField(db_column='NARRATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OTPS'


class Responses(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    message = models.CharField(db_column='MESSAGE', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESPONSES'


class Services(models.Model):
    reference_id = models.CharField(db_column='REFERENCE_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    req_desc = models.TextField(db_column='REQ_DESC', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    acct_no = models.CharField(db_column='ACCT_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    process_date = models.DateField(db_column='PROCESS_DATE', blank=True, null=True)  # Field name made lowercase.
    req_time = models.DateTimeField(db_column='REQ_TIME', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    mobileno = models.CharField(db_column='MOBILENO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customer_number = models.CharField(db_column='CUSTOMER_NUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SERVICES'


class SmsSettings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sendername = models.CharField(db_column='SENDERNAME', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SMS_SETTINGS'


class TransOnline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    refno = models.CharField(db_column='REFNO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prime5_refno = models.CharField(db_column='PRIME5_REFNO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sp_refno = models.CharField(db_column='SP_REFNO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dest_acct_mobno = models.CharField(db_column='DEST_ACCT_MOBNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_acct_mobno = models.CharField(db_column='SOURCE_ACCT_MOBNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='AMOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    trans_date = models.DateField(db_column='TRANS_DATE', blank=True, null=True)  # Field name made lowercase.
    trans_time = models.DateTimeField(db_column='TRANS_TIME', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='USERID', max_length=60, blank=True, null=True)  # Field name made lowercase.
    cust_no = models.CharField(db_column='CUST_NO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    trans_type = models.CharField(db_column='TRANS_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sp_code = models.CharField(db_column='SP_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    channel = models.CharField(db_column='CHANNEL', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRANS_ONLINE'


class Users(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='USERID', max_length=200)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mobileno = models.CharField(db_column='MOBILENO', max_length=50, blank=True, null=True)  # Field name made lowercase.
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


class UserTransaction(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    customerid = models.CharField(db_column='CUSTOMERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_account = models.CharField(db_column='SOURCE_ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_account_name = models.CharField(db_column='SOURCE_ACCOUNT_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_branch_code = models.CharField(db_column='SOURCE_BRANCH_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_bank_code = models.CharField(db_column='SOURCE_BANK_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dest_account_name = models.CharField(db_column='DEST_ACCOUNT_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dest_account = models.CharField(db_column='DEST_ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dest_bank_code = models.CharField(db_column='DEST_BANK_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dest_branch_code = models.CharField(db_column='DEST_BRANCH_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    channel = models.CharField(db_column='CHANNEL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    narration = models.CharField(db_column='NARRATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    trans_type = models.CharField(db_column='TRANS_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='AMOUNT', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DATECREATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_TRANSACTION'


class UssdLog(models.Model):
    sessionid = models.CharField(db_column='SESSIONID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    message_type = models.IntegerField(db_column='MESSAGE_TYPE', blank=True, null=True)  # Field name made lowercase.
    body = models.CharField(db_column='BODY', max_length=400, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    custno = models.CharField(db_column='CUSTNO', max_length=18, blank=True, null=True)  # Field name made lowercase.
    stage = models.IntegerField(db_column='STAGE', blank=True, null=True)  # Field name made lowercase.
    selected_account = models.CharField(db_column='SELECTED_ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    selected_amount = models.CharField(db_column='SELECTED_AMOUNT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    rec_account = models.CharField(db_column='REC_ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    accounts = models.CharField(db_column='ACCOUNTS', max_length=900, blank=True, null=True)  # Field name made lowercase.

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
    tid = models.AutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    body = models.CharField(db_column='BODY', max_length=500, blank=True, null=True)  # Field name made lowercase.
    date_created = models.DateField(db_column='DATE_CREATED', blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USSD_SESSION'


class WalletTransaction(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    exttrid = models.CharField(max_length=50, blank=True, null=True)
    customer_number = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=50, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    nw = models.CharField(max_length=50, blank=True, null=True)
    trans_type = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    voucher_code = models.CharField(max_length=50, blank=True, null=True)
    customerid = models.CharField(db_column='customerID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=50, blank=True, null=True)
    app_trans_id = models.CharField(max_length=50, blank=True, null=True)
    channel = models.CharField(max_length=50, blank=True, null=True)
    datecreated = models.DateTimeField(db_column='DateCreated', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.DateTimeField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WALLET_TRANSACTION'
        unique_together = (('app_trans_id', 'customerid'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EasyauditCrudevent(models.Model):
    event_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    object_repr = models.CharField(max_length=255, blank=True, null=True)
    object_json_repr = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_pk_as_string = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easyaudit_crudevent'


class EasyauditLoginevent(models.Model):
    login_type = models.SmallIntegerField()
    username = models.CharField(max_length=255, blank=True, null=True)
    datetime = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    remote_ip = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easyaudit_loginevent'


class EasyauditRequestevent(models.Model):
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=20)
    query_string = models.CharField(max_length=255, blank=True, null=True)
    remote_ip = models.CharField(max_length=50, blank=True, null=True)
    datetime = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easyaudit_requestevent'


class PostOfficeAttachment(models.Model):
    file = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'post_office_attachment'


class PostOfficeAttachmentEmails(models.Model):
    attachment = models.ForeignKey(PostOfficeAttachment, models.DO_NOTHING)
    email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_office_attachment_emails'
        unique_together = (('attachment', 'email'),)


class PostOfficeEmail(models.Model):
    from_email = models.CharField(max_length=254)
    to = models.TextField()
    cc = models.TextField()
    bcc = models.TextField()
    subject = models.CharField(max_length=989)
    message = models.TextField()
    html_message = models.TextField()
    status = models.SmallIntegerField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    scheduled_time = models.DateTimeField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    template = models.ForeignKey('PostOfficeEmailtemplate', models.DO_NOTHING, blank=True, null=True)
    backend_alias = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'post_office_email'


class PostOfficeEmailtemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField()
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    default_template = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    language = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'post_office_emailtemplate'
        unique_together = (('name', 'language', 'default_template'),)


class PostOfficeLog(models.Model):
    date = models.DateTimeField()
    status = models.SmallIntegerField()
    exception_type = models.CharField(max_length=255)
    message = models.TextField()
    email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_office_log'


class PrimeAppuser(models.Model):
    first_time = models.BooleanField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True, blank=True, null=True)
    user_role = models.ForeignKey('PrimeUserrole', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prime_appuser'


class PrimeEmailsettings(models.Model):
    email_user_tls = models.BooleanField()
    email_host = models.CharField(max_length=100, blank=True, null=True)
    email_port = models.CharField(max_length=100, blank=True, null=True)
    email_host_user = models.CharField(max_length=254, blank=True, null=True)
    email_host_password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prime_emailsettings'


class PrimeUserrole(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prime_userrole'
