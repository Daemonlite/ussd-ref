# dev: kojo_mcroni
# email: mcroni@teksol.com.gh
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import random
import json
import arrow
from ussd.models import *
from django.db.models import F
import uuid
import ast
import hashlib
today = arrow.now().date()
import time
import threading
import logging
import os
logger = logging.getLogger(__name__)
# BASE_URL = "http://1ce84561.ngrok.io"
# BASE_URL = "http://192.168.1.125/ibankwebservice"
# BASE_URL = "http://197.251.253.48:90/ibankwebservice"
# BASE_URL = "http://23.99.142.24/ibank"
BASE_URL = "https://mobile.test.servicesintegrity.com/ibankwebservice"
# BASE_URL = "http://192.168.1.125/ibankwebservice"
# BASE_URL = "197.251.253.43:90/ibankwebservice/"
# BASE_URL = "197.251.253.48:90/ibankwebservice"
# BASE_URL = "http://172.17.202.11/ibankwebservice"
# BASE_URL = ""
auth_name = 'teksol'
auth_pass = 'POP#teksol'


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


"""
USSD STAGES

2: HOME PAGE SCREEN
4 - ACCOUNT TO WALLET TRANSACTIONS
5- WALLET TO ACCOUNT TRANSACTIONS
6- USSD REGISTRATION PROCESS
7 - cHANGE PIN STAGE



32 - REAL HOME SCREEN DATA REQUEST TO SHOW THE OPTIONS

53 - WHEN YOU NEED TO REDIRECT A USER BACK TO THE HOME PAGE
"""



""" ussd session types
0 - new session
1- session continue
2- session end
"""

""" NETWORKS
027,057,056 = TIGO
024,054,055 = MTN
020,050 = VODA
026, = AIRTEL


"""
MTN = ["024","054","055"]
TIGO = ["027","057"]
VODA = ["020","050"]
AIRTEL = ["026","056"]


class USSDThread(threading.Thread):
    def __init__(self,phone_number,account,net,amount,bearer,super_log):
        threading.Thread.__init__(self)
        self.phone = phone_number
        self.account = account
        self.net = net
        self.amount = amount
        self.bearer = bearer
        self.log = super_log

    def run(self):
        print("starting")
        time.sleep(3)
        try:
            data = {
                "app_trans_id": str(uuid.uuid4()),
                'customer_number': self.phone,
                'account_number': self.account,
                'nw': self.net,
                'reference': "transferred money from {0}".format(self.phone),
                'trans_type': "DR",
                'amount': self.amount,
                "channel": "USSD",
            }
            print(data)
            url = "{0}/api/wallet".format(BASE_URL)
            headers = {'Authorization':
                           'Bearer {0}'.format(self.bearer)}
            r = requests.post(url, headers=headers, data=data)
        except Exception as e:
            print("connection error", e)

        else:
            print("waiting on response")
            print(r.text)
            response = json.loads(r.text)
            print(response)
            if not response['result']:
                print(response['message'])
                try:
                    url = "{0}".format(BASE_URL) + "/api/sms/"
                    print(url)
                    data = {
                        'PHONE': "+233{0}".format(self.phone),
                        "MESSAGE": "{0}. Thank you for banking with Teksol Bank".format(response['message'])
                    }
                    r = requests.post(url, data=data,
                                      auth=('{0}'.format(auth_name), '{0}'.format(auth_pass)))
                except Exception as e:
                    print("cant hit the api", e)

                else:
                    response = json.loads(r.text)
                    if not response['result']:
                        print(response)
                    else:
                        print("sms sent successfully")

            else:
                print("successfully sent ussd initiator")

        print("ending")





@csrf_exempt
def index(request):
    print("hitting ussd")
    if request.method == "POST":
        print("receiving a post request",request)
        # sess = request.POST.get("sessionId")
        # phone = request.POST.get("phoneNumber")
        # print("session id",pho)
        body = json.loads(request.body.decode("utf-8"))
        print(body)
        session_id = body['session_id']
        session_check = UssdLog.objects.using("sql").filter(sessionid=session_id)
        print(session_check)
        if session_check.exists():
            print("session exists")
            """lets grab the session id and the stage"""
            print(body)
            super_log = session_check[0]
            stage = session_check[0].stage
            print(stage)

            if stage == 10:
                print("momo transaction number screen")
                momo_network = body['ussd_body']
                print(momo_network)
                trans_net = ''
                if momo_network == "1":
                    trans_net = "MTN"
                if momo_network == "2":
                    trans_net = "AIR"
                if momo_network == "3":
                    trans_net = "TIG"
                if momo_network == "4":
                    trans_net = "VOD"
                print(trans_net)
                super_log.stage = 101
                super_log.phone = trans_net
                """i am tie'n the network and the phone number in the same variable with the : as a delimiter """
                super_log.save(using="sql")
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please type the Mobile Money Account Number",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                return JsonResponse(data)

            if stage == 101:
                print("received the momo number")
                momo_number = body['ussd_body']
                print(momo_number)
                if len(momo_number) == 10 and momo_number.startswith("0"):
                    print("a correct number")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please Type the Amount",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    super_log.stage = 102
                    momo_number = "+233{0}".format(momo_number[1:])
                    print(momo_number)
                    """so we add the momo number to the selected network in the same variable with a : delim """
                    super_log.phone = super_log.phone + ":" + momo_number
                    print(super_log.phone)
                    super_log.save(using="sql")
                    print("saved")
                    return JsonResponse(data)

                else:
                    print("a wrong number")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please type a correct mobile money number",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    super_log.stage = 101
                    super_log.save(using="sql")
                    return JsonResponse(data)

            if stage == 102:
                print("enter amount screen")
                try:
                    amount = float(body['ussd_body'])
                except Exception as e:
                    print("please enter a valid amount")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please enter a valid amount",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 102
                    super_log.save(using="sql")
                    return JsonResponse(data)

                else:
                    super_log.selected_amount = amount
                    super_log.stage = 103
                    super_log.save(using="sql")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Do you want to Approve this Transaction \n1) Yes \n2) No",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)

            if stage == 103:
                print("select an account to withdraw money from")
                try:
                    access_token = super_log.body
                    url = "{0}/api/userinfo".format(BASE_URL)
                    headers = {'Authorization':
                                   'Bearer {0}'.format(access_token)}
                    r = requests.get(url, headers=headers)
                except Exception as e:
                    print("cant get userinfo or accounts")
                else:
                    json_data = json.loads(r.text)
                    print("grabbed userinfo")
                    accounts = json_data['AccountTransactionses']
                    info = ""
                    count = 0
                    if len(accounts) == 0:
                        print("no account setup for user")
                        data = {
                            "msg_type": "2",
                            "ussd_body": "You don't have an account setup yet",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("ending session")
                        return JsonResponse(data)
                    log_accounts = []
                    for i in accounts:
                        count = count + 1
                        _account = {
                            "num": "{0}".format(count),
                            "account": i['Account']['ACCOUNTNO'],
                            "avail_balance": i['Account']['ACTUAL_AVAILABLE_BAL'],
                        }
                        log_accounts.append(_account)
                        print(i['Account']['ACCOUNTNO'])
                        account = i['Account']['ACCOUNTNO']
                        statement = "{0}. {1}\n".format(count, account)
                        info = info + statement
                    print("custno is", session_check[0].custno)
                    print(log_accounts)
                    header = "Select an Account to Transfer From" + "\n" + info
                    data = {
                        "msg_type": "1",
                        "ussd_body": "{0}".format(header),
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    session_check.using("sql").update(stage=104, accounts=log_accounts)
                    print("moving")
                    return JsonResponse(data)

            if stage == 104:
                print("grab all account and verify")
                # account = body['']
                account = int(body['ussd_body'])
                print(account, " the key the user typed")
                accounts = ast.literal_eval(super_log.accounts)
                print("the accounts saved during ussd session", accounts)
                try:
                    account = int(account)
                except ValueError:
                    print("wrong input")
                    info = ""
                    count = 0
                    for i in accounts:
                        print(i)
                        count = count + 1
                        account = i['account']
                        statement = "{0}. {1}\n".format(count, account)
                        info = info + statement
                    header = "Select an Account" + "\n" + info
                    data = {
                        "msg_type": "1",
                        "ussd_body": "{0}".format(header),
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    session_check.using("sql").update(stage=103)
                    return JsonResponse(data)
                else:
                    if account > len(accounts):
                        info = ""
                        count = 0
                        for i in accounts:
                            print(i)
                            count = count + 1
                            account = i['account']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        header = "Wrong Input \nSelect an Account" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        session_check.using("sql").update(stage=103)
                        return JsonResponse(data)
                    else:
                        account = int(account) - 1
                        account = accounts[account]['account']
                        try:
                            super_log.stage = 105
                            super_log.selected_account = str(account)
                            super_log.save(using="sql")
                        except Exception as e:
                            print(e)
                            print("cant save session obj")
                        else:
                            try:
                                print(super_log.phone, "thats the saved phone number")
                                """the phone number is tied to the mobile network with : as the delimiter, lets"""
                                network = super_log.phone.split(":")[0]
                                phone_number = super_log.phone.split(":")[1]
                                print(network, "and the network is ", phone_number)
                                data = {
                                    "app_trans_id": str(uuid.uuid4()),
                                    'customer_number': phone_number,
                                    'account_number': super_log.selected_account,
                                    'nw': network,
                                    'reference': "transfered money to {0}".format(phone_number),
                                    'trans_type': "CR",
                                    'amount': super_log.selected_amount,
                                    "channel": "USSD",
                                }
                                url = "{0}/api/wallet".format(BASE_URL)
                                headers = {'Authorization':
                                               'Bearer {0}'.format(super_log.body)}
                                r = requests.post(url, headers=headers, data=data)
                            except Exception as e:
                                print("connection error", e)
                            else:
                                print("waiting on response")
                                print(r.text)
                                response = json.loads(r.text)
                                print(response)
                                if not response['result']:
                                    print(response['message'])
                                    message = response['message']

                                    data = {
                                        "msg_type": "1",
                                        "ussd_body": message + "\n1) Go back \n2) Exit",
                                        "session_id": body['session_id'],
                                        "msisdn": body['msisdn'],
                                        "nw_code": body['nw_code'],
                                        "service_code": body['service_code'],
                                    }
                                    print("sending back to ussd server")
                                    super_log.stage = 43
                                    super_log.rec_account = ""
                                    super_log.selected_amount = ""
                                    super_log.save(using="sql")
                                    return JsonResponse(data)
                                else:
                                    print("successful")
                                    try:
                                        super_log.stage = 43
                                        super_log.rec_account = ""
                                        super_log.selected_amount = ""
                                        super_log.save(using="sql")
                                    except Exception as e:
                                        print(e)
                                        """this is bad, i know,,,just re-enforcing the code to save"""
                                        super_log.stage = 43
                                        super_log.rec_account = ""
                                        super_log.selected_amount = ""
                                        super_log.save(using="sql")
                                    finally:
                                        data = {
                                            "msg_type": "1",
                                            "ussd_body": "{0} Thank you for banking with Teksol Bank \n1) Go Back \n2) Exit".format(
                                                response['message']),
                                            "session_id": body['session_id'],
                                            "msisdn": body['msisdn'],
                                            "nw_code": body['nw_code'],
                                            "service_code": body['service_code'],
                                        }
                                        print("sending back to ussd server")
                                        return JsonResponse(data)

            if stage == 8:
                print("check balance account page")
                account = body['ussd_body']
                print(account, " the key the user typed", type(account))
                accounts = ast.literal_eval(super_log.accounts)
                print("the accounts saved during ussd session", accounts,type(accounts))
                try:
                    account = int(account)
                except ValueError:
                    print("wrong input")
                    info = ""
                    count = 0
                    for i in accounts:
                        print(i)
                        count = count + 1
                        account = i['account']
                        statement = "{0}. {1}\n".format(count, account)
                        info = info + statement
                    header = "Select an Account" + "\n" + info
                    data = {
                        "msg_type": "1",
                        "ussd_body": "{0}".format(header),
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    session_check.using("sql").update(stage=8)
                    return JsonResponse(data)
                else:
                    if account > len(accounts):
                        info = ""
                        count = 0
                        for i in accounts:
                            # print(i)
                            count = count + 1
                            account = i['account']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        header = "Select an Account" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        session_check.using("sql").update(stage=8)
                        return JsonResponse(data)
                    else:
                        account = int(account) - 1
                        # print(account)
                        # print(accounts[account]['account'])
                        # print(accounts[account]['avail_balance'])
                        session_check.using("sql").update(stage=32)
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Balance Enquiry\n Your available balance on your account is GHC {0}\nPress 1 to back to the main menu".
                                format(accounts[account]['avail_balance']),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        return JsonResponse(data)

            if stage == 5:
                print("wallet to account transasctions")
                """ account selected A2W  """
                account = int(body['ussd_body'])
                print(account, " the key the user typed")
                accounts = ast.literal_eval(super_log.accounts)
                print("the accounts saved during ussd session",accounts)
                try:
                    account = int(account)
                except ValueError:
                    print("wrong input")
                    info = ""
                    count = 0
                    for i in accounts:
                        print(i)
                        count = count + 1
                        account = i['account']
                        statement = "{0}. {1}\n".format(count, account)
                        info = info + statement
                    header = "Select an Account" + "\n" + info
                    data = {
                        "msg_type": "1",
                        "ussd_body": "{0}".format(header),
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    session_check.using("sql").update(stage=5)
                    return JsonResponse(data)
                else:
                    if account > len(accounts):
                        info = ""
                        count = 0
                        for i in accounts:
                            print(i)
                            count = count + 1
                            account = i['account']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        header = "Wrong Input \nSelect an Account" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        session_check.using("sql").update(stage=5)
                        return JsonResponse(data)
                    else:
                        account = int(account) - 1
                        account = accounts[account]['account']
                        try:
                            super_log.stage = 51
                            super_log.selected_account = str(account)
                            super_log.save(using="sql")
                        except Exception as e:
                            print(e)
                            print("cant save session obj")
                        else:
                            data = {
                                "msg_type": "1",
                                "ussd_body": "Wallet  To Account Transfer.\nPlease Type the Amount",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            return JsonResponse(data)
            if stage == 51:
                try:
                    amount = float(body['ussd_body'])
                except Exception as e:
                    print("error found",e)
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Wrong Input,please type an amount",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 51
                    super_log.save(using="sql")
                    return JsonResponse(data)
                else:
                    print("no error found")
                    print(amount, "amount is an int")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Do you want to Approve this Transaction \n1) Yes \n2) No",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 52
                    super_log.selected_amount = amount
                    super_log.save(using="sql")
                    return JsonResponse(data)
            if stage == 52:
                try:
                    answer = int(body['ussd_body'])
                except Exception as e:
                    print(e)
                    print("wrong input")
                    super_log.stage = 52
                    super_log.save(using="sql")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Do you want to Approve this Transaction \n1) Yes \n2) No",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)
                else:
                    if answer == 1:
                        phone_number = super_log.phone[4:]
                        net = "0{0}".format(super_log.phone[4:-7])
                        print(phone_number,net)
                        if net in MTN:
                            net = "MTN"
                        elif net in AIRTEL:
                            net = "AIR"
                        elif net in VODA:
                            net = "VOD"
                        elif net in TIGO:
                            net = "TIG"
                        print(net)
                        thread = USSDThread(super_log.phone,super_log.selected_account,net,super_log.selected_amount,super_log.body,super_log.id)
                        thread.start()
                        print("lets run")
                        message = "Dial *170# 2.Choose option 7 (Wallet) 3. Choose Option 3 (My Approvals) 4. Enter your MOMO Pin 5. Choose a pending transaction 6. Choose Option 1 to approve"
                        data = {
                            "msg_type": "2",
                            "ussd_body": message,
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                                    }
                        print("sending back to ussd server")
                        super_log.stage = 53
                        super_log.rec_account = ""
                        super_log.selected_amount = ""
                        super_log.save(using="sql")
                        return JsonResponse(data)
                        # try:
                        #     data = {
                        #     "app_trans_id": str(uuid.uuid4()),
                        #     'customer_number': phone_number,
                        #     'account_number': super_log.selected_account,
                        #     'nw': net,
                        #     'reference': "transfered money to {0}".format(phone_number),
                        #     'trans_type': "DR",
                        #     'amount': super_log.selected_amount,
                        #     "channel": "USSD",
                        #     }
                        #     url = "{0}/api/wallet".format(BASE_URL)
                        #     headers = {'Authorization':
                        #                    'Bearer {0}'.format(super_log.body)}
                        #     r = requests.post(url, headers=headers, data=data)
                        # except Exception as e:
                        #         print("connection error",e)
                        # else:
                        #     print("waiting on response")
                        #     print(r.text)
                        #     response = json.loads(r.text)
                        #     print(response)
                        #     if not response['result']:
                        #         print(response['message'])
                        #         message = response['message']
                        #         try:
                        #             super_log.stage = 52
                        #             super_log.save(using="sql")
                        #         except Exception as e:
                        #             print(e)
                        #         finally:
                        #             data = {
                        #                 "msg_type": "1",
                        #                 "ussd_body": message + "\n1) Go back \n2) Exit",
                        #                 "session_id": body['session_id'],
                        #                 "msisdn": body['msisdn'],
                        #                 "nw_code": body['nw_code'],
                        #                 "service_code": body['service_code'],
                        #             }
                        #             print("sending back to ussd server")
                        #             super_log.stage = 53
                        #             super_log.rec_account = ""
                        #             super_log.selected_amount = ""
                        #             super_log.save(using="sql")
                        #             return JsonResponse(data)
                        #     else:
                        #         print("successful")
                        #         try:
                        #             super_log.stage = 53
                        #             super_log.rec_account = ""
                        #             super_log.selected_amount = ""
                        #             super_log.save(using="sql")
                        #         except Exception as e:
                        #             print(e)
                        #             """this is bad, i know,,,just re-enforcing the code to save"""
                        #             super_log.stage = 53
                        #             super_log.rec_account = ""
                        #             super_log.selected_amount = ""
                        #             super_log.save(using="sql")
                        #         finally:
                        #             try:
                        #                 url = "{0}".format(BASE_URL) + "/api/sms/"
                        #                 print(url)
                        #                 data = {
                        #                     'PHONE': "+{0}".format(body['msisdn']),
                        #                     "MESSAGE": "Please accept the USSD Prompt to Continue with the funds transfer. Thank you for banking with SIS&L"
                        #                 }
                        #                 r = requests.post(url, data=data,
                        #                                   auth=('{0}'.format(auth_name), '{0}'.format(auth_pass)))
                        #             except Exception as e:
                        #                 print("cant hit the api",e)
                        #             else:
                        #                 response = json.loads(r.text)
                        #                 if not response['result']:
                        #                     pass
                        #                 else:
                        #                     print("sms sent successfully")

                    if answer == 2:
                        print("send back to home screen")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Welcome to Teksol Bank\nPlease select option\n1) Account to Wallet\n2) Wallet to Self Account\n3) Check Balance \n4) Change USSD Pin \n5) Mini statements\n6)Transfer to MoMo Account \n7)Press 7 for Menu Screen",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        super_log.stage = 2
                        super_log.save(using="sql")
                        return JsonResponse(data)
            if stage == 53:
                answer = int(body['ussd_body'])
                if answer == 1:
                    try:
                        super_log.stage = 2
                        super_log.save(using="sql")
                    except Exception as e:
                        """ trying again, just in case :-) """
                        super_log.stage = 2
                        super_log.save(using="sql")
                    finally:
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Welcome to Teksol Bank\nPlease select option\n1) Account to Self Wallet\n2) Wallet to Account\n3) Check Balance \n4) Change USSD Pin \n5) Mini statements\n6) Transfer to Mobile\n7) Next",
                            # "ussd_body": "Welcome to Teksol Bank\n1) Account to Wallet\n2) Wallet to Account\n3) Check Account Balance \n4) Change USSD Pin \n5) Mini statements",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        return JsonResponse(data)
                else:
                    data = {
                        "msg_type": "2",
                        "ussd_body": "Thank you for banking with Teksol Bank",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)
            if stage == 4:
                """ account selected A2W  """
                account = body['ussd_body']
                accounts = ast.literal_eval(super_log.accounts)
                print("the accounts saved during ussd session", accounts,type(accounts))
                try:
                    account = int(account)
                except ValueError:
                    print("wrong input")
                    info = ""
                    count = 0
                    for i in accounts:
                        print(i)
                        count = count + 1
                        account = i['account']
                        statement = "{0}. {1}\n".format(count, account)
                        info = info + statement
                    header = "Select an Account" + "\n" + info
                    data = {
                        "msg_type": "1",
                        "ussd_body": "{0}".format(header),
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    session_check.using("sql").update(stage=4)
                    return JsonResponse(data)
                else:
                    if account > len(accounts):
                        info = ""
                        count = 0
                        for i in accounts:
                            print(i)
                            count = count + 1
                            account = i['account']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        header = "Select an Account" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print(data)
                        session_check.using("sql").update(stage=4)
                        return JsonResponse(data)
                    else:
                        account = int(account) - 1
                        account = accounts[account]['account']
                        try:
                            super_log.stage = 41
                            super_log.selected_account = str(account)
                            super_log.save(using="sql")
                        except Exception as e:
                            print(e)
                            print("cant save session obj")
                        else:
                            data = {
                                "msg_type": "1",
                                "ussd_body": "Account To Wallet Transfer.\nPlease Type the Amount",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            return JsonResponse(data)
            if stage == 41:
                print("amount screen")
                print("lets verify if the amount is of a correct data type")
                try:
                    amount = float(body['ussd_body'])
                except:
                    print("error found")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Wrong Input,please type an amount",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 41
                    super_log.save(using="sql")
                    return JsonResponse(data)
                else:
                    print("no error found")
                    print(amount, "amount is an int")
                    try:
                        super_log.stage = 42
                        super_log.selected_amount = amount
                        super_log.save(using="sql")
                    except:
                        pass
                    else:
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Do you want to Approve this Transaction \n1) Yes \n2) No",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        return JsonResponse(data)
            if stage == 42:
                try:
                    answer = int(body['ussd_body'])
                except Exception as e:
                    print(e)
                    print("wrong input")
                    super_log.stage = 42
                    super_log.save(using="sql")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Do you want to Approve this Transaction \n1) Yes \n2) No",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)

                else:
                    if answer == 1:
                        phone_number = super_log.phone[4:]
                        net = "0{0}".format(super_log.phone[4:-7])
                        print(phone_number,net)
                        if net in MTN:
                            net = "MTN"
                        elif net in AIRTEL:
                            net = "AIR"
                        elif net in VODA:
                            net = "VOD"
                        elif net in TIGO:
                            net = "TIG"
                        print(net)
                        try:
                            data = {
                            "app_trans_id": str(uuid.uuid4()),
                            'customer_number': super_log.phone,
                            'account_number': super_log.selected_account,
                            'nw': net,
                            'reference': "transfered money to {0}".format(phone_number),
                            'trans_type': "CR",
                            'amount': super_log.selected_amount,
                            "channel": "USSD",
                            }
                            url = "{0}/api/wallet".format(BASE_URL)
                            headers = {'Authorization':
                                           'Bearer {0}'.format(super_log.body)}
                            r = requests.post(url, headers=headers, data=data)
                        except Exception as e:
                                print("connection error",e)
                        else:
                            print("waiting on response")
                            print(r.text)
                            response = json.loads(r.text)
                            print(response)
                            if not response['result']:
                                print(response['message'])
                                message = response['message']
                                try:
                                    super_log.stage = 42
                                    super_log.save(using="sql")
                                except Exception as e:
                                    print(e)
                                finally:
                                    data = {
                                        "msg_type": "1",
                                        "ussd_body": message + "\n1) Go back \n2) Exit",
                                        "session_id": body['session_id'],
                                        "msisdn": body['msisdn'],
                                        "nw_code": body['nw_code'],
                                        "service_code": body['service_code'],
                                    }
                                    print("sending back to ussd server")
                                    super_log.stage = 43
                                    super_log.rec_account = ""
                                    super_log.selected_amount = ""
                                    super_log.save(using="sql")
                                    return JsonResponse(data)
                            else:
                                print("successful")
                                try:
                                    super_log.stage = 43
                                    super_log.rec_account = ""
                                    super_log.selected_amount = ""
                                    super_log.save(using="sql")
                                except Exception as e:
                                    print(e)
                                    """this is bad, i know,,,just re-enforcing the code to save"""
                                    super_log.stage = 43
                                    super_log.rec_account = ""
                                    super_log.selected_amount = ""
                                    super_log.save(using="sql")
                                finally:
                                    data = {
                                        "msg_type": "1",
                                        "ussd_body": "{0} Thank you for banking with Teksol Bank \n1) Go Back \n2) Exit".format(response['message']),
                                        "session_id": body['session_id'],
                                        "msisdn": body['msisdn'],
                                        "nw_code": body['nw_code'],
                                        "service_code": body['service_code'],
                                    }
                                    print("sending back to ussd server")
                                    return JsonResponse(data)
            if stage == 43:
                try:
                    answer = int(body['ussd_body'])
                except Exception as e:
                    print(e)
                    data = {
                        "msg_type": "2",
                        "ussd_body": "Thank you for banking with Teksol Bank",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)
                else:
                    if answer == 1:
                        try:
                            super_log.stage = 2
                            super_log.save(using="sql")
                        except Exception as e:
                            """ trying again, just in case :-) """
                            super_log.stage = 2
                            super_log.save(using="sql")
                        finally:
                            data = {
                                "msg_type": "1",
                                "ussd_body": "Welcome to Teksol Bank\nPlease select option\n1) Account to Self Wallet\n2) Wallet to Account\n3) Check Balance \n4) Change USSD Pin \n5) Mini statements\n6) Transfer to Mobile\n7) Next",
                                # "ussd_body": "Welcome to Teksol Bank\n1) Account to Wallet\n2) Wallet to Account\n3) Check Account Balance \n4) Change USSD Pin \n5) Mini statements",
                                # "ussd_body": "***Welcome to SISL***\n1. Account to Wallet\n2. Wallet to Account\n3. Check Transactions \n4. Change USSD Pin",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            return JsonResponse(data)
                    else:
                        print("done for the session")
                        data = {
                            "msg_type": "2",
                            "ussd_body": "Thank you for banking with Teksol Bank",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        return JsonResponse(data)
            if stage == 2:
                selected_input = body['ussd_body']
                print(selected_input,"the number the user selected")
                print(type(selected_input))
                print("HOME SCREEN page")
                if int(body['ussd_body']) == 1:
                    print("Account to Wallet Session, listing all accounts")
                    try:
                        access_token = super_log.body
                        url = "{0}/api/userinfo".format(BASE_URL)
                        headers = {'Authorization':
                                       'Bearer {0}'.format(access_token)}
                        r = requests.get(url, headers=headers)
                    except Exception as e:
                        print("cant get userinfo or accounts")
                    else:
                        json_data = json.loads(r.text)
                        print("grabbed userinfo")
                        accounts = json_data['AccountTransactionses']
                        info = ""
                        count = 0
                        if len(accounts) == 0:
                            print("no account setup for user")
                            data = {
                                "msg_type": "2",
                                "ussd_body": "You don't have an account setup yet",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("ending session")
                            return JsonResponse(data)
                        log_accounts = []
                        for i in accounts:
                            count = count + 1
                            _account = {
                                "num": "{0}".format(count),
                                "account": i['Account']['ACCOUNTNO'],
                                "avail_balance": i['Account']['ACTUAL_AVAILABLE_BAL'],
                            }
                            log_accounts.append(_account)
                            print(i['Account']['ACCOUNTNO'])
                            account = i['Account']['ACCOUNTNO']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        print("custno is", session_check[0].custno)
                        print(log_accounts)
                        header = "Select an Account to Transfer From" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        session_check.using("sql").update(stage=4,accounts=log_accounts)
                        print("moving to screen 4")
                        return JsonResponse(data)

                if int(body['ussd_body']) == 2:
                    print("wallet to Account Session")
                    print("Wallet To Account, listing all accounts")
                    try:
                        access_token = super_log.body
                        url = "{0}/api/userinfo".format(BASE_URL)
                        headers = {'Authorization':
                                       'Bearer {0}'.format(access_token)}
                        r = requests.get(url, headers=headers)
                    except Exception as e:
                        print("cant get userinfo or accounts",e)
                    else:
                        json_data = json.loads(r.text)
                        print("grabbed userinfo",json_data)
                        accounts = json_data['AccountTransactionses']
                        info = ""
                        count = 0
                        if len(accounts) == 0:
                            print("no account setup for user")
                            data = {
                                "msg_type": "2",
                                "ussd_body": "You don't have an account setup yet",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("ending session")
                            return JsonResponse(data)
                        log_accounts = []
                        for i in accounts:
                            count = count + 1
                            _account = {
                                "num": "{0}".format(count),
                                "account": i['Account']['ACCOUNTNO']
                            }
                            log_accounts.append(_account)
                            print(i['Account']['ACCOUNTNO'])
                            account = i['Account']['ACCOUNTNO']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        print("custno is", session_check[0].custno)
                        print(log_accounts)
                        header = "Select an Account to Transfer To" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        session_check.using("sql").update(stage=5, accounts=log_accounts)
                        print("moving to screen 5")
                        return JsonResponse(data)

                if int(body['ussd_body']) == 3:
                    print("check balance on accounts")
                    try:
                        access_token = super_log.body
                        url = "{0}/api/userinfo".format(BASE_URL)
                        headers = {'Authorization':
                                       'Bearer {0}'.format(access_token)}
                        r = requests.get(url, headers=headers)
                    except:
                        print("cant get userinfo or accounts")
                    else:
                        json_data = json.loads(r.text)
                        print("grabbed userinfo",json_data)
                        accounts = json_data['AccountTransactionses']
                        info = ""
                        count = 0
                        if len(accounts) == 0:
                            print("no account setup for user")
                            data = {
                                "msg_type": "2",
                                "ussd_body": "You don't have an account setup yet",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("ending session")
                            return JsonResponse(data)
                        log_accounts = []
                        for i in accounts:
                            count = count + 1
                            _account = {
                                "num": "{0}".format(count),
                                "account": i['Account']['ACCOUNTNO'],
                                "avail_balance": i['Account']['ACTUAL_AVAILABLE_BAL'],
                            }
                            log_accounts.append(_account)
                            print(i['Account']['ACCOUNTNO'])
                            account = i['Account']['ACCOUNTNO']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        print("custno is", session_check[0].custno)
                        print(log_accounts)
                        header = "Select an Account" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        session_check.using("sql").update(stage=8, accounts=log_accounts)
                        print("moving to screen 8")
                        return JsonResponse(data)

                if int(body['ussd_body']) == 4:
                    print("change pin")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please type in your current USSD pin",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 7
                    super_log.save(using="sql")
                    return JsonResponse(data)

                if int(body['ussd_body']) == 5:
                    print("mini statements")
                    try:
                        access_token = super_log.body
                        url = "{0}/api/userinfo".format(BASE_URL)
                        headers = {'Authorization':
                                       'Bearer {0}'.format(access_token)}
                        r = requests.get(url, headers=headers)
                    except:
                        print("cant get userinfo or accounts")
                    else:
                        json_data = json.loads(r.text)
                        print("grabbed userinfo",json_data)
                        accounts = json_data['AccountTransactionses']
                        info = ""
                        count = 0
                        if len(accounts) == 0:
                            print("no account setup for user")
                            data = {
                                "msg_type": "2",
                                "ussd_body": "You don't have an account setup yet",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("ending session")
                            return JsonResponse(data)
                        log_accounts = []

                        for i in accounts:
                            count = count + 1
                            lists_of_transactions = []
                            for trans in i['Transaction'][:3]:
                                trans = {
                                    "date": trans['TRANS_DATE'][:10],
                                    "amount": trans["AMT_FOREIGN"],
                                    "narration": trans["TRANS_NARRATION"]
                                }
                                lists_of_transactions.append(trans)
                            # print(lists_of_transactions)

                            _account = {
                                "num": "{0}".format(count),
                                "account": i['Account']['ACCOUNTNO'],
                                "avail_balance": i['Account']['ACTUAL_AVAILABLE_BAL'],
                                "transactions": lists_of_transactions
                            }

                            log_accounts.append(_account)
                            # print(i['Account'])
                            # print(i['Account']['ACCOUNTNO'])
                            account = i['Account']['ACCOUNTNO']
                            statement = "{0}. {1}\n".format(count, account)
                            info = info + statement
                        print("custno is", session_check[0].custno)
                        print(log_accounts)
                        header = "Select an Account" + "\n" + info
                        data = {
                            "msg_type": "1",
                            "ussd_body": "{0}".format(header),
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("abt to save data")
                        # session_check.using("sql").update(stage=9,accounts=log_accounts)

                        # super_log.stage = 9
                        # super_log.accounts = log_accounts
                        # super_log.save(using="sql")
                        session_check.using("sql").update(stage=9,accounts=log_accounts)
                        print("moving to screen 9")
                        return JsonResponse(data)

                if selected_input == "6":
                    # print("mobile money transaction page")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please select the network of the Mobile Money Account\n 1)MTN \n 2)AIRTEL \n 3)TIGO \n 4)VODAFONE",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    # print("sending back to ussd server")
                    super_log.stage = 10
                    super_log.save(using="sql")
                    return JsonResponse(data)

                if selected_input == "7":
                    # print("second menu")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "1) Open Account\n2) Bill Payments \n3)Airtime \n4)Generate OTP \n5) Referral Scheme",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    super_log.stage = 200
                    super_log.save(using="sql")
                    return JsonResponse(data)

            if stage == 2011:
                data = {
                    "msg_type": "2",
                    "ussd_body": "Thanks for selecting this product.A confirmation message would be sent to you shortly",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                # print("sending back to ussd server")
                super_log.stage = 2012
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 2012:
                # print("Account type selected,type name")
                data = {
                    "msg_type": "2",
                    "ussd_body": "Thanks for selecting this product.A confirmation message would be sent to you shortly",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                # print("sending back to ussd server")
                super_log.stage = 2012
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 201:
                # print("Account type selected")
                answer = int(body['ussd_body'])
                if answer == 1:
                    # print("fixed dep selected")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please type an Account Name",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    # print("sending back to ussd server")
                    super_log.stage = 2011
                    super_log.save(using="sql")
                    return JsonResponse(data)

                if answer == 2:
                    print("saving selected")

                if answer == 3:
                    print("current account selected ")

            if stage == 2023:
                print("bill id need")
                bill_id = body['ussd_body']
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please select the account to withdraw from \n1)40000234556123 \n2)4000024582135",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                print("sending back to ussd server")
                super_log.stage = 2024
                super_log.save(using="sql")
                return JsonResponse(data)

            # if stage == 2024:
            #     print("bill id need")
            #     bill_id = body['ussd_body']
            #     data = {
            #         "msg_type": "1",
            #         "ussd_body": "Please type in the amount to pay",
            #         "session_id": body['session_id'],
            #         "msisdn": body['msisdn'],
            #         "nw_code": body['nw_code'],
            #         "service_code": body['service_code'],
            #     }
            #     print("sending back to ussd server")
            #     super_log.stage = 2025
            #     super_log.save(using="sql")
            #     return JsonResponse(data)

            if stage == 2024:
                print("bill id need")
                bill_id = body['ussd_body']
                data = {
                    "msg_type": "2",
                    "ussd_body": "Please your request is under processing. You will receive a message shortly",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                print("sending back to ussd server")
                super_log.stage = 2025
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 2022:
                print("bill id amount")
                bill_id = body['ussd_body']
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please type the amount",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                print("sending back to ussd server")
                super_log.stage = 2023
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 202:
                print("service providers menu")
                # answer = int(body['ussd_body'])
                # if answer == 1:
                #     print("water bills selected")
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please type your Bill ID",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                print("sending back to ussd server")
                super_log.stage = 2022
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 300:
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please type the amount",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                print("sending back to ussd server")
                super_log.stage = 301
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 301:
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please select the account to buy from \n1)4000047689124\n2)4000057912346",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                # print("sending back to ussd server")
                super_log.stage = 302
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 302:
                data = {
                    "msg_type": "1",
                    "ussd_body": "Please type the phone number",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                # print("sending back to ussd server")
                super_log.stage = 303
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 303:
                data = {
                    "msg_type": "2",
                    "ussd_body": "Your request is being processed. You will be notified shortly",
                    "session_id": body['session_id'],
                    "msisdn": body['msisdn'],
                    "nw_code": body['nw_code'],
                    "service_code": body['service_code'],
                }
                # print("sending back to ussd server")
                super_log.stage = 303
                super_log.save(using="sql")
                return JsonResponse(data)

            if stage == 200:
                # print('second menu selection')
                answer = int(body['ussd_body'])
                if answer == 1:
                    # print("open an account selected")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please select a product type \n1) Fixed Deposit \n2)Savings \n3)Current Account ",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    # print("sending back to ussd server")
                    super_log.stage = 201
                    super_log.save(using="sql")
                    return JsonResponse(data)

                if answer == 2:
                    # print("bill payment menu")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please select the Service Provider \n1)Water Bills\n2)DSTV Bills \n3)Kwese\n4)Electricity",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    # print("sending back to ussd server")
                    super_log.stage = 202
                    super_log.save(using="sql")
                    return JsonResponse(data)

                if answer == 3:
                    # print("buy airtime menu")
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please select the Service Provider \n1)MTN\n2)GLO\n3)Airtel\n4)9Mobile",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    # print("sending back to ussd server")
                    super_log.stage = 300
                    super_log.save(using="sql")
                    return JsonResponse(data)

                if answer == 4:
                    # print("generate OTP")
                    try:
                        url = "{0}".format(BASE_URL) + "/api/sms/"
                        # print(url)
                        data = {
                            'PHONE': "+{0}".format(body['msisdn']),
                            "MESSAGE": "Your generated OTP is {0}".format(random.randint(1001,9999))
                        }
                        r = requests.post(url, data=data,
                                          auth=('{0}'.format(auth_name), '{0}'.format(auth_pass)))
                    except Exception as e:
                        print("cant hit the api",e)
                        # print("")
                    else:
                        response = json.loads(r.text)
                        if not response['result']:
                            pass
                        else:
                            print("sms sent successfully")
                            pass
                    data = {
                        "msg_type": "2",
                        "ussd_body": "A message will be sent to you shortly with your generated OTP number",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    return JsonResponse(data)

                if answer == 5:
                    print("referral scheme")
                    data = {
                        "msg_type": "2",
                        "ussd_body": "Thank you for banking with Teksol Bank",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)

            if stage == 9:
                print("mini statement account selection")
                account = body['ussd_body']
                accounts = ast.literal_eval(super_log.accounts)
                print("the accounts saved during ussd session", accounts, type(accounts))
                try:
                    account = int(account)
                except ValueError:
                    print("wrong input")
                    info = ""
                    count = 0
                    for i in accounts:
                        print(i)
                        count = count + 1
                        account = i['account']
                        statement = "{0}. {1}\n".format(count, account)
                        info = info + statement
                    header = "Select an Account" + "\n" + info
                    data = {
                        "msg_type": "1",
                        "ussd_body": "{0}".format(header),
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    session_check.using("sql").update(stage=5)
                    return JsonResponse(data)
                else:
                    sel = int(account) - 1
                    account = accounts[sel]['account']
                    print("checking transactions on ", account)
                    trans = accounts[sel]['transactions']
                    info = ""
                    for transaction in trans:
                        print(transaction)
                        statement = "{0} {1} {2}\n".format(transaction['date'],transaction['amount'],transaction['narration'])
                        info = info + statement
                    header = "Recent Transactions \n" + info
                    try:
                        url = "{0}".format(BASE_URL) + "/api/sms/"
                        print(url)
                        data = {
                            'PHONE': "+{0}".format(body['msisdn']),
                            "MESSAGE": header
                        }
                        r = requests.post(url, data=data, auth=('{0}'.format(auth_name), '{0}'.format(auth_pass)))
                        data = json.loads(r.text)
                        print(data)
                    except Exception as e:
                        print("cant hit the api")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Please try again. Thank you \n1)Go Back \n2) Exit",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        super_log.stage = 53
                        super_log.save(using="sql")
                        return JsonResponse(data)
                    else:
                        print(r.text)
                        response = json.loads(r.text)
                        if not response['result']:
                            print(response['message'])
                            print("cant send sms")
                            data = {
                                "msg_type": "1",
                                "ussd_body": "Please try again. Thank you \n1)Go Back \n2) Exit",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            super_log.stage = 53
                            super_log.save(using="sql")
                            return JsonResponse(data)
                        else:
                            print("successful")
                            data = {
                                "msg_type": "1",
                                "ussd_body": "You will receive an SMS shortly with details of your transactions. Thank you \n1)Go Back \n2) Exit",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            super_log.stage = 53
                            super_log.save(using="sql")
                            print("sending the sms")
                            return JsonResponse(data)
            if stage == 7:
                # print("confirm ussd pin")
                ussd_pin = body['ussd_body']
                try:
                    user = Users.objects.using("sql").get(mobileno=body['msisdn'])
                    hashed_pin = user.ussd_pin
                except Exception as e:
                    print(e)
                    print("cant hit database for the hashed pin")
                else:
                    print(hashed_pin)
                    if check_password(hashed_pin, ussd_pin):
                        print("password matched with db password")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Please enter your new 4 digit pin",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        super_log.stage = 71
                        super_log.save(using="sql")
                        return JsonResponse(data)
                    else:
                        print("code didnt match with db")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Wrong Input,please try again",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        super_log.stage = 7
                        super_log.save(using="sql")
                        return JsonResponse(data)
            if stage == 71:
                print("new ussd pin is",body['ussd_body'])
                try:
                    ussd_pin = int(body['ussd_body'])
                except Exception as e:
                    print(e)
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Wrong Input,please try again",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 71
                    super_log.save(using="sql")
                    return JsonResponse(data)
                else:
                    print("new pin is an int")
                    if not len(str(ussd_pin)) == 4:
                        print("not the required len")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Wrong Input,please try again",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        super_log.stage = 71
                        super_log.save(using="sql")
                        return JsonResponse(data)
                    else:
                        new_pin = hash_password(str(ussd_pin))
                        print(new_pin)
                        try:
                            Users.objects.using("sql").filter(mobileno="+{0}".format(body['msisdn'])).update(ussd_pin=new_pin)
                            print("saved hashed password in db")
                        except:
                            print("cant access db to save user session")
                            data = {
                                "msg_type": "1",
                                "ussd_body": "Service error,please try again",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("sending back to ussd server")
                            super_log.stage = 71
                            super_log.save(using="sql")
                            return JsonResponse(data)
                        else:
                            data = {
                                "msg_type": "1",
                                "ussd_body": "Congratulations,you have changed your USSD pin successfully \n1) Go Back \n2) Exit",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("sending back to ussd server")
                            super_log.stage = 72
                            super_log.save(using="sql")
                            return JsonResponse(data)
            if stage == 72:
                print("able to change password successfully")
                answer = int(body['ussd_body'])
                print(answer)
                if answer == 1:
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Teksol Bank\nPlease select an option \n1) Account to Self Wallet\n2) Wallet to Account\n3) Check  Balance \n4) Change USSD Pin \n5) Mini statements\n6) Transfer to Mobile\n7) Next",
                        # "ussd_body": "Welcome to Teksol Bank\n1) Account to Wallet\n2) Wallet to Account\n3) Check Account Balance \n4) Change USSD Pin \n5) Mini statements",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 2
                    super_log.save(using="sql")
                    return JsonResponse(data)
                else:
                    data = {
                        "msg_type": "2",
                        "ussd_body": "Thank you for banking with Teksol Bank",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    return JsonResponse(data)
            if stage == 3:
                print("approved user, USSD pin stage")
                ussd_pin = body['ussd_body']
                try:
                    pin = int(ussd_pin)
                    if len(ussd_pin) != 4:
                        print("code entered isnt a number")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Wrong Input,please type a 4 digit pin",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        super_log.stage = 3
                        super_log.save(using="sql")
                        return JsonResponse(data)
                except ValueError:
                    print("input isnt an int",ussd_pin)
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Wrong Input,please type a 4 digit pin",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 3
                    super_log.save(using="sql")
                    return JsonResponse(data)

                else:
                    print(ussd_pin,"ussd pin is an int")
                    super_log.body = ussd_pin
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please confirm your USSD Pin",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 32
                    super_log.body = ussd_pin
                    super_log.save(using="sql")
                    return JsonResponse(data)
            if stage == 32:
                print("confirm ussd pin page")
                print("REAL HOME PAGE")
                ussd_pin = body['ussd_body']
                pin = super_log.body
                if pin == ussd_pin:
                    print("match in pin")
                    try:
                        user = Users.objects.using("sql").get(mobileno=body['msisdn'])
                        hashed_pin = user.ussd_pin
                    except Exception as e:
                        print(e)
                    else:
                        print(hashed_pin)
                        if check_password(hashed_pin,ussd_pin):
                            print(user.account_number)
                            print("password matched with db password")
                            print("danilo's api")
                            try:
                                url = "{0}".format(BASE_URL) + "/api/token"
                                print(url)
                                data = {
                                    'username': "{0}".format(user.account_number),
                                    "password": "{0}".format(hashed_pin),
                                    "grant_type": "password"
                                }
                                r = requests.post(url, data=data)
                                data = json.loads(r.text)
                                print(data)
                                access_token = data['access_token']
                            except Exception as e:  # This is the correct syntax
                                print("1st error cant connect to service or get token",)
                            else:
                                print(access_token)
                                super_log.body = access_token
                                print("saved the token ")
                                super_log.stage = 2
                                super_log.custno = user.customer_number
                                super_log.save(using="sql")
                                data = {
                                    "msg_type": "1",
                                    "ussd_body": "Teksol Bank\nPlease select an option\n1) Account to Self Wallet\n2) Wallet to Account\n3) Check Balance \n4) Change USSD Pin \n5) Mini statements\n6) Transfer to Mobile\n7) Next",
                                    # "ussd_body": "Welcome to Teksol Bank\n1) Account to Wallet\n2) Wallet to Account\n3) Check Account Balance \n4) Change USSD Pin \n5) Mini statements\n6) Transfer to Mobile",
                                    "session_id": body['session_id'],
                                    "msisdn": body['msisdn'],
                                    "nw_code": body['nw_code'],
                                    "service_code": body['service_code'],
                                }
                                return JsonResponse(data)
                        else:
                            print("password didnt match db password")
                            data = {
                                "msg_type": "2",
                                "ussd_body": "Sorry, failed to verify pin,Thank you",
                                "session_id": body['session_id'],
                                "msisdn": body['msisdn'],
                                "nw_code": body['nw_code'],
                                "service_code": body['service_code'],
                            }
                            print("sending back to ussd server")
                            super_log.body = ""
                            super_log.save(using="sql")
                            return JsonResponse(data)

                else:
                    print("input didnt match")
                    try:
                        super_log.stage = 32
                        super_log.save(using="sql")
                    except:
                        print("cant access db to save user session")
                    else:
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Wrong Input,Please confirm your USSD Pin Number",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        return JsonResponse(data)
            if stage == 6:
                print("registration screen")
                try:
                    url = "{0}".format(BASE_URL) + "/api/register/ussd/"
                    print(url)
                    data = {
                        'MOBILENO': "+{0}".format(body['msisdn']),
                        "ACCOUNT_NUMBER": body['ussd_body']
                    }
                    print(data)
                    # global auth_pass
                    # global auth_name
                    r = requests.post(url, data=data, auth=('{0}'.format(auth_name), '{0}'.format(auth_pass)))
                    data = json.loads(r.text)
                    print(data)
                except:
                    print("cant hit the api")
                    pass
                else:
                    print(data)
                    if data['message'] == "user registration successful":
                        print("registered user successfully")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Please setup your 4 Digit USSD Pin, This would be used for subsequent confirmation when initiating a transaction",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        super_log.stage = 61
                        super_log.save(using="sql")
                        return JsonResponse(data)

                    if data['message'][:30] == "These credentials do not exist":
                        print("user doesnt exist")
                        data = {
                            "msg_type": "2",
                            "ussd_body": "Your credentials do not exist",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        return JsonResponse(data)
            if stage == 61:
                ussd_pin = body['ussd_body']
                print(ussd_pin)
                try:
                    pin = int(ussd_pin)
                    if len(ussd_pin) != 4:
                        print("code entered isnt a number")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Wrong Input,please type a 4 digit pin",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        super_log.stage = 61
                        super_log.save(using="sql")
                        return JsonResponse(data)
                except ValueError:
                    print("input isnt an int",ussd_pin)
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Wrong Input,please type a 4 digit pin",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 61
                    super_log.save(using="sql")
                    return JsonResponse(data)

                else:
                    print(ussd_pin,"ussd pin is an int")
                    super_log.body = ussd_pin
                    data = {
                        "msg_type": "1",
                        "ussd_body": "Please confirm your USSD Pin Number",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.stage = 62
                    super_log.body = ussd_pin
                    super_log.save(using="sql")
                    return JsonResponse(data)
            if stage == 62:
                print("confirm")
                ussd_pin = body['ussd_body']
                pin = super_log.body
                if pin == ussd_pin:
                    print("match in pin")
                    data = {
                        "msg_type": "2",
                        "ussd_body": "Thanks for registering,your account is under approval, You will receieve a txt message shortly",
                        "session_id": body['session_id'],
                        "msisdn": body['msisdn'],
                        "nw_code": body['nw_code'],
                        "service_code": body['service_code'],
                    }
                    print("sending back to ussd server")
                    super_log.body = ""
                    hashed = hash_password(ussd_pin)
                    try:
                        Users.objects.using("sql").filter(mobileno="+{0}".format(body['msisdn'])).update(ussd_pin=hashed,ussd_sub="PENDING")
                        print("saved hashed password in db")
                    except:
                        print("cant access db to save user session")
                    else:
                        super_log.stage = 2
                        super_log.save(using="sql")
                    return JsonResponse(data)
                else:
                    print("input didnt match")
                    try:
                        super_log.stage = 62
                        super_log.save(using="sql")
                    except:
                        print("cant access db to save user session")
                    else:
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Please confirm your USSD Pin Number",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        return JsonResponse(data)
        else:
            print("new session object")
            try:
                UssdSession(body=body,date_created=today,type=body['msg_type']).save(using="sql")
                log = UssdLog(sessionid=session_id,phone="+{0}".format(body['msisdn']),message_type=body['msg_type'])
                log.save(using="sql")
                print("Saved logs")
                try:
                    url = "{0}".format(BASE_URL) + "/api/validate/phone"
                    print(url)
                    data = {
                        'MOBILENO': "+{0}".format(body['msisdn']),
                    }
                    print(data)
                    r = requests.post(url, data=data, auth=('{0}'.format(auth_name), '{0}'.format(auth_pass)))
                    data = json.loads(r.text)
                    print(data)
                except Exception as e:
                    print("cant hit the api",e)

                else:
                    additional_message = data['additional']
                    print(additional_message,type(additional_message))
                    if additional_message == "001":
                        print("new user")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Teksol Bank\nYou need To Register Before You can Access This Feature, Please Enter Your Account Number",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        log.stage = 6
                        log.save(using="sql")
                        return JsonResponse(data)

                    elif additional_message == "001":
                        print("new user")
                        data = {
                            "msg_type": "1",
                            "ussd_body": "Teksol Bank\nYou need To Register Before You can Access This Feature, Please Enter Your Account Number",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        log.stage = 6
                        log.save(using="sql")
                        return JsonResponse(data)

                    elif additional_message == "009":
                        print("Already registered for ussd,lets proceed")
                        try:
                            print(body['msisdn'])
                            user = Users.objects.using("sql").filter(mobileno="{0}".format(body['msisdn']))
                        except Exception as e:
                            print("cant hit database for existing user records")
                        else:
                            if user.exists():
                                print("user exists")
                                user = user[0]
                                print(user)
                                print(user.ussd_sub)
                                if user.ussd_sub == "PENDING":
                                    if user.ussd_pin is None:
                                        print("didnt finish setting up ussd pin process")
                                        log.stage = 61
                                        log.save(using="sql")
                                        data = {
                                            "msg_type": "1",
                                            "ussd_body": "Please finish setting up your USSD Pin to Continue",
                                            "session_id": body['session_id'],
                                            "msisdn": body['msisdn'],
                                            "nw_code": body['nw_code'],
                                            "service_code": body['service_code'],
                                        }
                                        return JsonResponse(data)
                                    if user.ussd_pin is not None:
                                        print("finished setting up process")
                                        data = {
                                            "msg_type": "2",
                                            "ussd_body": "Your account is still pending. We will notify you when the approval is done. Thank you.",
                                            "session_id": body['session_id'],
                                            "msisdn": body['msisdn'],
                                            "nw_code": body['nw_code'],
                                            "service_code": body['service_code'],
                                        }
                                        return JsonResponse(data)

                                if user.ussd_sub == "YES":
                                    print("an approved user, can make transaction")
                                    try:
                                        log.stage = 3
                                        log.save(using="sql")
                                    except Exception as e:
                                        print(e)
                                    else:
                                        data = {
                                            "msg_type": "1",
                                            "ussd_body": "Teksol Bank,Please enter your USSD Pin to Continue.",
                                            "session_id": body['session_id'],
                                            "msisdn": body['msisdn'],
                                            "nw_code": body['nw_code'],
                                            "service_code": body['service_code'],
                                        }
                                        return JsonResponse(data)

                    if data['additional'] == "005":
                        """registered for mobweb but not ussd"""
                        print("registered for mobweb but not ussd")

                        data = {
                            "msg_type": "1",
                            "ussd_body": "Please setup your 4 Digit USSD Pin, This would be used for subsequent confirmation when initiating a transaction",
                            "session_id": body['session_id'],
                            "msisdn": body['msisdn'],
                            "nw_code": body['nw_code'],
                            "service_code": body['service_code'],
                        }
                        print("sending back to ussd server")
                        log.stage = 61
                        log.save(using="sql")
                        return JsonResponse(data)

            except Exception as e:
                print("cant save session to db")
            else:
                pass

    data = {
        "message": "teksol ussd local"
    }
    return JsonResponse(data)

def test(request):
    print("hitting ussd")
    if request.method == "POST":
        print("hitting post request")
        data = {

        }

        return JsonResponse(data)
    data = {

    }

    return JsonResponse(data)
# todo grab the access_token from danilo and use it to implement the transaction
# todo use the main kyc table to grab the user with the mobileno
