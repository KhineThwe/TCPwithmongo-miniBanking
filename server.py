import json
from datetime import datetime
import socket
import random
import pymongo

class TCPserver():
    def __init__(self):
        self.server_ip='localhost'
        self.server_port = 9997
        self.userInfoDict = {}
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        try:
            """MongoClient() is a method,it contains ip,port"""
            self.connection = pymongo.MongoClient("localhost", 27017)
            self.database = self.connection["myTestDB"]
            self.collection = self.database["myCollection"]
            print("Connection Successful")
        except Exception as err:
            print(err)
	    
    def main(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen(1)
        print(f'[*] Listening on {self.server_ip}:{self.server_port} >:')
        while True:
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            self.handle_client(client)

    def insertData(self,data={}):
        try:
            result = self.collection.insert_one(data)
            print("Data are inserted!!!", result.inserted_id)
        except Exception as err:
            print(err)

    def userDuplicateChecking(self,c_username):
        try:
            query = {"username":c_username}
            result = self.collection.find_one(query)
            if result:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            
    def checkingLoginInfo(self,username,password):
        try:
            query = {"username": username,"password":password}
            result = self.collection.find(query)
            for i in result:
                idNo = i.get("_id")
                print("Id No: ",idNo)
            return idNo
        except Exception as err:
            print(err)
    
    def get_amount(self, loginId):
        try:
            query = {"_id": loginId}
            result = self.collection.find(query)
            for i in result:
                amount = i.get("amount")
                print("Amount: ", amount)
            return amount
        except Exception as err:
            print(err)
    
    def updateAmount(self,idNo,amount):
        try:
            oAmount = self.get_amount(idNo)
            query = {"_id": idNo,"amount":oAmount}
            newQuery = {"$set":{"_id": idNo,"amount":amount}}
            self.collection.update_one(query,newQuery)
            print("Updating amount successful!!!")
        except Exception as err:
            print(err)
    
    def returnId(self, username):
        try:
            query = {"username": username}
            result = self.collection.find(query)
            for i in result:
                idNo = i.get("_id")
                print("Return id: ", idNo)
            return idNo
        except Exception as err:
            print(err)
    
    def get_name(self, loginId):
        try:
            query = {"_id": loginId}
            result = self.collection.find(query)
            for i in result:
                name = i.get("username")
                print("Name: ", name)
            return name
        except Exception as err:
            print(err)
            
    def updateName(self, loginId, nName):
        try:
            oldName = self.get_name(loginId)
            query = {"_id": loginId, "username": oldName}
            newQuery = {"$set": {"_id": loginId, "username": nName}}
            self.collection.update_one(query, newQuery)
            print("Updating name: {} to {} successful!!!".format(oldName, nName))
        except Exception as err:
            print(err)

    def updatePassword(self ,loginId ,nPwd) :
        try :
            oldPwd = self.get_password(loginId)
            query = {"_id" : loginId ,"password" : oldPwd}
            newQuery = {"$set" : {"_id" : loginId ,"password" : nPwd}}
            self.collection.update_one(query ,newQuery)
            print("Updating password: {} to {} successful!!!".format(oldPwd ,nPwd))
        except Exception as err :
            print(err)
    
    def print_all_accounts_details(self):
        try:
            result = self.collection.find({}, {"_id": 0})
            # flag = None
            # for i in result:
            #     print(i)
            #     flag = i
            return result
        except Exception as err:
            print(err)

    def handle_client(self,client_socket):
        with client_socket as sock:
            request = sock.recv(4096)
            print(f'[*] Received: {request.decode("utf-8")}')
            #need to decode clientinfo data
            clientInfo =request.decode("utf-8")
            print("Checking clientInfo",clientInfo,type(clientInfo))
            if clientInfo !="":
                clientInfo = json.loads(clientInfo)
                option = clientInfo['option']
                if option == 1:
                   c_username = clientInfo ['username']
                   c_password = clientInfo ['password']
                   c_amount = clientInfo ['amount']
                   randomNo = random.randint(100,999)
                   flag = self.userDuplicateChecking(c_username)
                   if flag:
                       data = '400' + ' ' + 'UsernameDuplicated' + ' ' + '0'
                       sock.send(bytes(data,'utf-8'))
                   else:
                       dataForm = {"_id":randomNo,"username": c_username ,"password": c_password ,"amount": c_amount}
                       self.userInfoDict.update(dataForm)
                       print(self.userInfoDict)
                       self.insertData(self.userInfoDict)
                       data = '201' + ' ' + 'SuccessRegistration' + ' ' + c_username
                       print('Data inserted into mongoDB:'+c_username)
                       sock.send(bytes(data,'utf-8'))
                elif option == 2:
                    # userOption = clientInfo['userOption']
                    c_username = clientInfo ['username']
                    c_password = clientInfo ['password']
                    loginId = self.checkingLoginInfo(c_username ,c_password)
                    print("Checking loginId",loginId,type(loginId))
                    if loginId :
                        print("Working here!!!")
                        data = '200' + ' ' + 'LoginSuccess' + ' ' + str(loginId)
                        print('Login Successful with loginId: ' ,loginId)
                        sock.send(bytes(data,'utf-8'))
                    else:
                        data = '404' + ' ' + 'LoginFail' + ' ' + "str(loginId)"
                        sock.send(bytes(data ,'utf-8'))
                
                elif option == 3:
                    loginId = clientInfo ['senderLoginId']
                    senderName = self.get_name(loginId)
                    receiverName = clientInfo ['receiverName']
                    receiverId = self.returnId(receiverName)
                    transferAmount = clientInfo ['transferAmount']
                    
                    senderAmount =self.get_amount(loginId)
                    receiverAmount = self.get_amount(receiverId)
                    if transferAmount < int(senderAmount):
                        fsenderAmount = int(senderAmount) - transferAmount
                        freceiverAmount = int(receiverAmount) + transferAmount
                        
                        self.updateAmount(loginId,fsenderAmount)
                        self.updateAmount(receiverId,freceiverAmount)

                        print(f'Transaction completed. Current Balance of sender: ₹{fsenderAmount}' ,senderName)
                        print(f'Transaction completed. Current Balance of receiver: ₹{freceiverAmount}' ,receiverName)

                        data = '301' + ' ' + 'Transfer_Transition_Successful!' + ' ' + 'amount'
                        sock.send(bytes(data ,'utf-8'))
                    else:
                        print("Insufficient amount to transfer")
                        data = '302' + ' ' + 'Transfer_Transition_Fail!' + ' ' + 'Insufficient_amount_to_transfer'
                        sock.send(bytes(data ,'utf-8'))
                
                elif option == 4:
                    loginId = clientInfo ['senderLoginId']
                    senderName = self.get_name(loginId)
                    depositAmount = clientInfo ['depositAmount']
                    senderAmount = self.get_amount(loginId)
                    fsenderAmount = int(senderAmount) + depositAmount
                    self.updateAmount(loginId ,fsenderAmount)
                    print(f'Transaction completed. Current Balance of sender: ₹{fsenderAmount}' ,senderName)
                    data = '303' + ' ' + 'Deposit_Transition_Successful!' + ' ' + 'amount'
                    sock.send(bytes(data ,'utf-8'))
                
                elif option == 5:
                    loginId = clientInfo ['senderLoginId']
                    senderName = self.get_name(loginId)
                    withdrawAmount = clientInfo ['withdrawAmount']
                    senderAmount = self.get_amount(loginId)
                    if withdrawAmount < int(senderAmount) :
                        fsenderAmount = int(senderAmount) - withdrawAmount
                        self.updateAmount(loginId ,fsenderAmount)
                        print(f'Transaction completed. Current Balance of sender: ₹{fsenderAmount}' ,senderName)
                        data = '304' + ' ' + 'Withdraw_Transition_Successful!' + ' ' + 'amount'
                        sock.send(bytes(data ,'utf-8'))
                    else:
                        print("Insufficient amount to withdraw")
                        data = '305' + ' ' + 'Withdraw_Transition_Fail!' + ' ' + 'Insufficient_amount_to_withdraw'
                        sock.send(bytes(data ,'utf-8'))
                
                elif option == 6:
                    loginId = clientInfo ['senderLoginId']
                    # oldName = self.get_name(loginId)
                    newName = clientInfo['newName']
                    self.updateName(loginId,newName)
                    data = '306' + ' ' + 'Update_Name_Success!' + ' ' + 'amount'
                    sock.send(bytes(data ,'utf-8'))
                
                elif option == 7:
                    loginId = clientInfo ['senderLoginId']
                    # oldName = self.get_name(loginId)
                    newPassword = clientInfo['newPassword']
                    self.updatePassword(loginId,newPassword)
                    data = '307' + ' ' + 'Update_Password_Success!' + ' ' + 'amount'
                    sock.send(bytes(data ,'utf-8'))
                
                elif option == 8:
                    data = self.print_all_accounts_details()
                    mydata=''
                    for i in data:
                        print("Checking all account data: ",i)
                        name , password ,amount = i["username"],i["password"],i["amount"]
                        print('test....',name , password , amount)
                        mydata =mydata + name+'+'+password+'+'+amount+'+'
                    print('-----',mydata)
                    
                    data = '308' + ' ' + 'All_Accounts_Fetching_Success!'+' '+ mydata
                    sock.send(bytes(data ,'utf-8'))
                    
                        
if __name__ == '__main__':
    Myserver = TCPserver()
    Myserver.main()
