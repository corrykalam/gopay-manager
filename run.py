import requests, json, random, sys, os, time, os.path
"""
Gopay Accounts Manager
Author: @corrykalam
Date: 06/09/2019
"""
uniqueid = "ac03e5d1e7c3b%s"%(random.randint(000,999));
base_url = "https://api.gojekapi.com"
headers = {
    "Content-Type": "application/json",
    "X-AppVersion": "2.28.2",
    "X-Uniqueid": "%s"%(uniqueid),
    "X-Location": "-6.180495,106.824992"
}
def backupConfig():
    with open('config.json','w') as fp:
        json.dump(config,fp,ensure_ascii=True,indent=4)

def restart():
    backupConfig()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def sendOtp(phone):
    data = '{"phone":"%s"}'%(phone)
    req = requests.post(base_url+"/v3/customers/login_with_phone", data=data, headers=headers).text
    jsonq = json.loads(req)
    if jsonq["success"] == True:
        print("Succes send OTP!")
        return jsonq["data"]["login_token"]
    else:
        print("Failed send OTP | %s"%jsonq["errors"][0]["message"])
        return False

def login(logintoken, otp, nameconfig, pin):
    data = '{"scopes":"gojek:customer:transaction gojek:customer:readonly","grant_type":"password","login_token":"%s","otp":"%s","client_id":"gojek:cons:android","client_secret":"83415d06-ec4e-11e6-a41b-6c40088ab51e"}'%(logintoken, otp)
    req = requests.post(base_url+"/v3/customers/token", data=data, headers=headers).text
    jsonq = json.loads(req)
    if jsonq["success"] == True:
        print("Success save your token")
        config.append({nameconfig:{"token":jsonq["data"]["access_token"],"pin":pin, "uniqueid": uniqueid}})
        backupConfig()
        return True
    else:
        print("Failed login | %s"%(jsonq["errors"][0]["message"]))
        return False

def checkWalletCode(phone,token, uniqueid):
    if phone[0] == "6":
        headers["Authorization"] = "Bearer %s"%(token)
        headers["X-Uniqueid"] = uniqueid
        print(headers)
        req = requests.get(base_url+"/wallet/qr-code?phone_number=%2B%s"%(phone), headers=headers).text
        jsonq = json.loads(req)
        if jsonq["success"] == True:
            return jsonq["data"]["qr_id"]
        else:
            print("Failed check walletcode | %s"%(jsonq["errors"][0]["message"]))
            return False
    else:
        headers["Authorization"] = "Bearer %s"%(token)
        headers["X-Uniqueid"] = uniqueid
        req = requests.get(base_url+"/wallet/qr-code?phone_number=%2B62"+phone[1:], headers=headers).text
        jsonq = json.loads(req)
        if jsonq["success"] == True:
            return jsonq["data"]["qr_id"]
        else:
            print("Failed check walletcode | %s"%(jsonq["errors"][0]["message"]))
            return False

def sendWallet(qrcode, token, pin, uniqueid):
    headers["Authorization"] = "Bearer %s"%(token)
    headers["pin"] = pin
    headers["X-Uniqueid"] = uniqueid
    headers["User-Agent"] = "Gojek/3.34.1 (com.go-jek.ios; build:3701278; iOS 12.3.1) Alamofire/4.7.3"
    data = '{"qr_id":"%s","amount":"1","description":"💰"}'%(qrcode)
    req = requests.post(base_url+"/v2/fund/transfer", data=data.encode('utf-8'), headers=headers).text
    jsonq = json.loads(req)
    if jsonq["success"] == True:
        return "Success send gopay :)"
    else:
        return "Failed send gopay | %s"%(jsonq["errors"][0]["message"])

def sendWalletOtherAmount(qrcode, token, pin, uniqueid, amount):
    headers["Authorization"] = "Bearer %s"%(token)
    headers["pin"] = pin
    headers["X-Uniqueid"] = uniqueid
    data = '{"qr_id":"%s","amount":"%s","description":"💰"}'%(qrcode, amount)
    req = requests.post(base_url+"/v2/fund/transfer", data=data.encode('utf-8'), headers=headers).text
    jsonq = json.loads(req)
    if jsonq["success"] == True:
        return "Success send gopay :)"
    else:
        return "Failed send gopay | %s"%(jsonq["errors"][0]["message"])

def checkBalance(token, uniqueid):
    headers["Authorization"] = "Bearer %s"%(token)
    headers["X-Uniqueid"] = uniqueid
    req = requests.get(base_url+"/wallet/profile", headers=headers).text
    jsonq = json.loads(req)
    if jsonq["success"] == True:
        print("Your balance is Rp.%s"%jsonq["data"]["balance"])
        return True
    else:
        return False
banner = """
 ██████╗  ██████╗ ██████╗  █████╗ ██╗   ██╗
██╔════╝ ██╔═████╗██╔══██╗██╔══██╗╚██╗ ██╔╝
██║  ███╗██║██╔██║██████╔╝███████║ ╚████╔╝ 
██║   ██║████╔╝██║██╔═══╝ ██╔══██║  ╚██╔╝  
╚██████╔╝╚██████╔╝██║     ██║  ██║   ██║   
 ╚═════╝  ╚═════╝ ╚═╝     ╚═╝  ╚═╝   ╚═╝   
            Accounts Manager                                   
           @author: corrykalam
"""
menu = """
[1] Check Balance
[2] Send Rp.1
[3] Send Rp.1 (Mass Sender)
[4] Send other amount
[5] Send other amount (Mass Sender)
[6] Change pin account (Only change json)
[7] Add accounts
[8] Delete accounts
[0] Exit
"""
if os.path.exists('config.json') == False:
    print("Creating config file!")
    f = open('config.json', 'w')
    f.write("[]")
    f.close()
    python = sys.executable
    os.execl(python, python, *sys.argv)
with open('config.json') as fp:
    config = json.load(fp)
print(banner)
if  config == []:
    configname = input('Enter name config: ')
    number = input('Enter number (62xxx or 1xxx): ')
    otptoken = sendOtp(number)
    if otptoken == False:
        sys.exit(0)
    else:
        otp_log = input('Enter OTP: ')
        pin_log = input('Enter PIN: ')
        login_log = login(otptoken, otp_log, configname, pin_log)
        if login_log == True:
            restart()
else:
    print(menu)
    menu_log = input('Select menu: ')
    if menu_log == "1":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            token = ""
            pin = ""
            unique = ""
            for key in config[int(accounts_enter)-1].keys():
                token += config[int(accounts_enter)-1][key]["token"]
                pin += config[int(accounts_enter)-1][key]["pin"]
                unique += config[int(accounts_enter)-1][key]["uniqueid"]
        else:
            print("Accounts not found!")
            sys.exit(0)
        checkBalance(token, unique)
    elif menu_log == "2":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            token = ""
            pin = ""
            unique = ""
            for key in config[int(accounts_enter)-1].keys():
                token += config[int(accounts_enter)-1][key]["token"]
                pin += config[int(accounts_enter)-1][key]["pin"]
                unique += config[int(accounts_enter)-1][key]["uniqueid"]
        else:
            print("Accounts not found!")
            sys.exit(0)
        number_log = input('Number to send Rp.1: ')
        wallet_log = checkWalletCode(number_log, token, unique)
        if wallet_log == False:
            sys.exit(0)
        else:
            print(sendWallet(wallet_log, token, pin, unique))     
    elif menu_log == "3":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            token = ""
            pin = ""
            unique = ""
            for key in config[int(accounts_enter)-1].keys():
                token += config[int(accounts_enter)-1][key]["token"]
                pin += config[int(accounts_enter)-1][key]["pin"]
                unique += config[int(accounts_enter)-1][key]["uniqueid"]
        else:
            print("Accounts not found!")
            sys.exit(0)
        number_logx = input('Number to send Rp.1 Mass (Delimiter `,`): ')
        for numbermass in number_logx.split(","):
            wallet_logx = checkWalletCode(numbermass, token, unique)
            if wallet_logx == False:
                pass
            else:
                time.sleep(random.randint(1,10))
                print(numbermass +" | "+ sendWallet(wallet_logx, token, pin, unique))
    elif menu_log == "4":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            token = ""
            pin = ""
            unique = ""
            for key in config[int(accounts_enter)-1].keys():
                token += config[int(accounts_enter)-1][key]["token"]
                pin += config[int(accounts_enter)-1][key]["pin"]
                unique += config[int(accounts_enter)-1][key]["uniqueid"]
        else:
            print("Accounts not found!")
            sys.exit(0)
        number_log = input('Number to send: ')
        amount_log = input('Amount: ')
        wallet_log = checkWalletCode(number_log, token, unique)
        if wallet_log == False:
            sys.exit(0)
        else:
            print(sendWalletOtherAmount(wallet_log, token, pin, unique, amount_log)) 
    elif menu_log == "5":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            token = ""
            pin = ""
            unique = ""
            for key in config[int(accounts_enter)-1].keys():
                token += config[int(accounts_enter)-1][key]["token"]
                pin += config[int(accounts_enter)-1][key]["pin"]
                unique += config[int(accounts_enter)-1][key]["uniqueid"]
        else:
            print("Accounts not found!")
            sys.exit(0)
        number_logx = input('Number to send Rp.1 Mass (Delimiter `,`): ')
        amount_logx = input('Amount: ')
        for numbermass in number_logx.split(","):
            wallet_logx = checkWalletCode(numbermass, token, unique)
            if wallet_logx == False:
                pass
            else:
                time.sleep(random.randint(1,10))
                print(numbermass +" | "+ sendWalletOtherAmount(wallet_logx, token, pin, unique, amount_logx))      
    elif menu_log == "6":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            token = ""
            pin = ""
            unique = ""
            for key in config[int(accounts_enter)-1].keys():
                token += config[int(accounts_enter)-1][key]["token"]
                pin += config[int(accounts_enter)-1][key]["pin"]
                unique += config[int(accounts_enter)-1][key]["uniqueid"]
        else:
            print("Accounts not found!")
            sys.exit(0)
        new_pin = input('Enter new pin: ')
        config[int(accounts_enter)-1][key]["pin"] = new_pin
        print("Success change pin!")
        backupConfig()
    elif menu_log == "7":
        configname = input('Enter name config: ')
        number = input('Enter number (62xxx or 1xxx): ')
        otptoken = sendOtp(number)
        if otptoken == False:
            sys.exit(0)
        else:
            otp_log = input('Enter OTP: ')
            pin_log = input('Enter PIN: ')
            login_log = login(otptoken, otp_log, configname, pin_log)
            if login_log == True:
                restart()
    elif menu_log == "8":
        no = 0
        username = ""
        for key in config:
            for anjay in key.keys():
                no += 1
                username += "[%s]%s \n"%(str(no), anjay)
        print(username)
        accounts_enter = input('Select accounts: ')
        if int(accounts_enter) < len(config)+1:
            del config[int(accounts_enter)-1]
            backupConfig()
            print("Success delete accounts!")
            restart()
        else:
            print("Accounts not found!")
            sys.exit(0)
    elif menu_log == "0":
        print("Thank you for use tool ^_^")
        sys.exit(0)
    else:
        print("Index out of range!")
        sys.exit(0)
