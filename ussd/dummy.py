data = {'AccountTransactionses': [{'Account': {'ACCOUNTNO': '2050000000101', 'ACTUAL_AVAILABLE_BAL': 47958.5, 'COUNT': 0, 'PRODUCT_DESC': 'INDIVIDUAL CURRENT', 'ACTUAL_CURRENT_BAL': 47958.5, 'TRANS_FROM': None, 'ACCT_NAME': 'ADJEI ALEX INDIVIDUAL', 'TRANS_TO': None, 'CUSTOMER_ID': None}, 'Transaction': [{'ACCT_NAME': 'ADJEI ALEX INDIVIDUAL', 'TRANS_NARRATION': 'MOBILE MONEY TRANSFER-CASH-IN', 'ACCT_GL_NO': '2050000000101', 'DR_CR': 'DR', 'AMT_FOREIGN': 1.0, 'TRANS_REF_NO': 3398.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX INDIVIDUAL', 'TRANS_NARRATION': 'FUND TRANSFER TO ADJEI ALEX KWEKU SA 2', 'ACCT_GL_NO': '2050000000101', 'DR_CR': 'DR', 'AMT_FOREIGN': 1.0, 'TRANS_REF_NO': 3378.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX INDIVIDUAL', 'TRANS_NARRATION': 'MOBILE MONEY TRANSFER-CASH-OUT', 'ACCT_GL_NO': '2050000000101', 'DR_CR': 'CR', 'AMT_FOREIGN': 0.1, 'TRANS_REF_NO': 3369.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX INDIVIDUAL', 'TRANS_NARRATION': 'MOBILE MONEY TRANSFER-CASH-IN', 'ACCT_GL_NO': '2050000000101', 'DR_CR': 'DR', 'AMT_FOREIGN': 0.1, 'TRANS_REF_NO': 3364.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX INDIVIDUAL', 'TRANS_NARRATION': 'FUND TRANSFER TO ADJEI ALEX KWEKU SA 2', 'ACCT_GL_NO': '2050000000101', 'DR_CR': 'DR', 'AMT_FOREIGN': 1.0, 'TRANS_REF_NO': 3362.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}]}, {'Account': {'ACCOUNTNO': '2050000000102', 'ACTUAL_AVAILABLE_BAL': 35.0, 'COUNT': 0, 'PRODUCT_DESC': 'INDIVIDUAL CURRENT', 'ACTUAL_CURRENT_BAL': 35.0, 'TRANS_FROM': None, 'ACCT_NAME': 'ADJEI ALEX KWEKU SA 2', 'TRANS_TO': None, 'CUSTOMER_ID': None}, 'Transaction': [{'ACCT_NAME': 'ADJEI ALEX KWEKU SA 2', 'TRANS_NARRATION': 'FUND TRANSFER FROM ADJEI ALEX INDIVIDUAL', 'ACCT_GL_NO': '2050000000102', 'DR_CR': 'CR', 'AMT_FOREIGN': 1.0, 'TRANS_REF_NO': 3379.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX KWEKU SA 2', 'TRANS_NARRATION': 'FUND TRANSFER FROM ADJEI ALEX INDIVIDUAL', 'ACCT_GL_NO': '2050000000102', 'DR_CR': 'CR', 'AMT_FOREIGN': 1.0, 'TRANS_REF_NO': 3363.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX KWEKU SA 2', 'TRANS_NARRATION': 'FUND TRANSFER FROM ADJEI ALEX INDIVIDUAL', 'ACCT_GL_NO': '2050000000102', 'DR_CR': 'CR', 'AMT_FOREIGN': 14.0, 'TRANS_REF_NO': 3361.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX KWEKU SA 2', 'TRANS_NARRATION': 'FUND TRANSFER FROM ADJEI ALEX INDIVIDUAL', 'ACCT_GL_NO': '2050000000102', 'DR_CR': 'CR', 'AMT_FOREIGN': 1.0, 'TRANS_REF_NO': 3359.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}, {'ACCT_NAME': 'ADJEI ALEX KWEKU SA 2', 'TRANS_NARRATION': 'FUND TRANSFER FROM ADJEI ALEX INDIVIDUAL', 'ACCT_GL_NO': '2050000000102', 'DR_CR': 'CR', 'AMT_FOREIGN': 12.0, 'TRANS_REF_NO': 3339.0, 'VALUE_DATE': '0001-01-01T00:00:00', 'TRANS_DATE': '2017-01-12T00:00:00'}]}], 'User': {'CUSTOMER_NUMBER': '00000001', 'LOGINATTEMPTS': 0, 'OTP_DATECREATED': None, 'MAX_VAL_TRANS': 0.0, 'USSD_SUB': None, 'OLDPASSWORD': None, 'ACCOUNT_NUMBER': None, 'CREATIONCHANNEL': None, 'INTER_BANK_SUB': None, 'OTP': None, 'NO_OF_D_TRANS': 0, 'USSD_PIN': None, 'MOBILENO': '+233273725809', 'PASSWORDEXPIRYDATE': None, 'VALUE_OF_D_TRANS': 0.0, 'OTP_METHOD': None, 'PASSWORD': None, 'AUTHSTATUS': None, 'METHOD': None, 'LASTLOGIN': '10/31/2018 8:51:21 AM', 'USERSTATUS': None, 'USERNAME': 'ADJEI ALEX KWEKU', 'PASSWORD_SET': False, 'USERID': 'alex@teksol.com.gh'}}

accounts = data['AccountTransactionses']
log_accounts = []
count=0
info=''
# for i in accounts:
#     lists_of_transactions = []
#     for trans in i['Transaction']:
#         print(trans)
#         lists_of_transactions.append(trans)
for i in accounts:
    count = count + 1
    lists_of_transactions = []
    for trans in i['Transaction'][:2]:
        # print(len(i['Transaction']))
        trans = {
            "date": trans['TRANS_DATE'][:10],
            "amount": trans["AMT_FOREIGN"],
            "narration": trans["TRANS_NARRATION"]
        }
        lists_of_transactions.append(trans)
    print(len(lists_of_transactions))
    # print(lists_of_transactions)

#     _account = {
#         "num": "{0}".format(count),
#         "account": i['Account']['ACCOUNTNO'],
#         "avail_balance": i['Account']['ACTUAL_AVAILABLE_BAL'],
#         "transactions": lists_of_transactions
#     }
#
#     log_accounts.append(_account)
#     # print(i['Account'])
#     # print(i['Account']['ACCOUNTNO'])
#     account = i['Account']['ACCOUNTNO']
#     statement = "{0}. {1}\n".format(count, account)
#     info = info + statement
# # print("custno is", session_check[0].custno)
# print(log_accounts)
# header = "Select an Account" + "\n" + info
# data = {
#     "msg_type": "1",
#     "ussd_body": "{0}".format(header),
#     # "session_id": body['session_id'],
#     # "msisdn": body['msisdn'],
#     # "nw_code": body['nw_code'],
#     # "service_code": body['service_code'],
# }
# print("abt to save data")