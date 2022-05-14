import socket
import json
import sys

class Client:
    def __init__(self):
        self.target_host = 'localhost'
        self.target_port = 9997

    def runClient(self,data):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_host, self.target_port))

        client.send(data)

        recvSMSMfromServer = client.recv(4096)
        recvSMSMfromServer=recvSMSMfromServer.decode("utf-8")
        status,message,amount = recvSMSMfromServer.split(' ')

        if status == '400':
            print(status,message)
        elif status == '201':
            print(status,message)
            print("Data are inserted into mongoDB",amount)
        elif status == '404':
            print(status,message)
        elif status == '301':
            print("Transfer Transition complete")
            print(status,message)
        elif status == '302':
            print(status,message,amount)
        elif status == '303':
            print("Deposit Transition complete")
            print(status,message)
        elif status == '304':
            print("Withdraw Transition complete")
            print(status,message)
        elif status == '305':
            print(status,message,amount)
        elif status == '306':
            print(status,message)
        elif status == '307':
            print(status,message)
        elif status == '308':
            print(status,message,amount)
            # name,password,a_amount = amount.split('+')
            # print(name,password,a_amount)
        elif status == '200':
            print(status , message)
            print("Checking loginuser's loginId: ",int(amount))
            print("you can do transition now ")
            #kzt
            print(" ")
            print(
                "Welcome User : Avilable options are:")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("3) Transfer money")
            print("4) Deposit")
            print("5) Withdraw")
            print("6) Update customer's Name")
            print("7) Update customer's Password")
            print("8) Print all customers detail")
            print("9) Sign out")
            print(" ")
            option = int(input("Choose your option: "))
            if option==3:
                acceptName = input("Enter acceptName to transfer: ")
                r_amount = int(input("Enter amount to transfer: "))
                data = {'option': 3, 'senderLoginId': int(amount), 'receiverName': acceptName,"transferAmount":r_amount}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                # self.runClient(msg)
                # data = '3' + ' ' + message + ' ' + acceptName+' '+str(amount)
                # data = bytes(data, 'utf-8')
                try:
                    self.runClient(msg)
                    print('success')
                except Exception as err:
                    print(err)
            
            elif option == 4 :
                # message ka sender uname pr lr tr
                r_amount = int(input("Enter amount to deposit: "))
                data = {'option': 4, 'senderLoginId': int(amount), "depositAmount":r_amount}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                try :
                    self.runClient(msg)
                    print('success')
                except Exception as err :
                    print(err)
            
            elif option == 5 :
                # message ka sender uname pr lr tr
                r_amount = int(input("Enter amount to withdraw: "))
                data = {'option': 5, 'senderLoginId': int(amount), "withdrawAmount":r_amount}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                try :
                    self.runClient(msg)
                    print('success')
                except Exception as err :
                    print(err)
            
            elif option == 6 :
                # message ka sender uname pr lr tr
                newName = input("Enter new name to update: ")
                data = {'option': 6, 'senderLoginId': int(amount), "newName":newName}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                try :
                    self.runClient(msg)
                    print('success')
                except Exception as err :
                    print(err)
            
            elif option == 7 :
                # message ka sender uname pr lr tr
                newPassword = input("Enter new password to update: ")
                data = {'option': 7, 'senderLoginId': int(amount), "newPassword":newPassword}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                try :
                    self.runClient(msg)
                    print('success')
                except Exception as err :
                    print(err)
            
            elif option == 8 :
                data = {'option': 8}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                try :
                    self.runClient(msg)
                    print('success')
                except Exception as err :
                    print(err)
            
            elif option == 9:
                print("Bye Bye for now!!!")
                sys.exit()
            
            
        
       
        client.close()
        
    

    def option(self):
        option = int(input("[+]Press-1 to Register\n[+]Press-2 to Login!"))
        if option == 1:
                username = input("Enter username to register: ")
                password = input("Enter password to register: ")
                password1 = input("Enter password again to confirm: ")
                if password == password1:
                    amount = input("Enter amount to register: ")
                    data = {'option': 1, 'username': username, 'password': password,"amount":amount}
                    data = json.dumps(data)
                    msg = bytes(data,'utf-8')
                    self.runClient(msg)
                else:
                    print("Passwords don't match!!Please try again!!!")
                
        
        elif option == 2:
                username = input("Enter username to login: ")
                password = input("Enter password to login: ")
                data = {'option': 2, 'username': username, 'password': password}
                data = json.dumps(data)
                msg = bytes(data,'utf-8')
                self.runClient(msg)


if __name__ == "__main__":
    tcpClient:Client=Client()
    while True:
        tcpClient.option()
