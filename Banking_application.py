import re
import pymysql
import random
import datetime
connection = pymysql.connect(host='localhost', database='banking', user='root', password='')
class User:
    def __init__(self):
        self.user_details=[]
        self.bal=0
        self.new_bal=0
        self.loggedin=False
    def register(self, name, password, email_id, aadhar_no, phone_no, address, gender, account_no):
        bal = self.bal
        condition = True
        if re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', name):
            print()
        else:
            print("Invalid Name")
            condition=False
            
        if re.fullmatch('^[A-Za-z0-9@#$%^&+=]{8,}$', password):
            print()
        else:
            print("Invalid password(Password should be of atleast 8 digit!)")
            condition=False
            
        if re.fullmatch('^[a-z0-9.]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email_id):
            print()
        else:
            print("Invalid email id")
            condition=False
            
        if re.fullmatch('^\d{4}\d{4}\d{4}$', aadhar_no):
            print()
        else:
            print("Invalid Aadhar no.")
            condition=False
            
        if re.fullmatch(r'(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}', phone_no):
            print()
        else:
            print("Invalid phone no.\n")
            condition=False
            
        if condition==True:
            self.user_details = [name, password, email_id, aadhar_no, phone_no, address, gender, account_no, bal]
            with open(f"{name}.txt","w") as f:
                for details in self.user_details:
                    f.write(str(details)+"\n")
            f.close()

            try:
                mycursor=connection.cursor()
                data1 = (name,password,email_id,aadhar_no,phone_no,address,gender,account_no, bal)
                sql = "insert into registration values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(sql,(data1))
                print("Account Created Successfully!\n")
                connection.commit()
            except:
                print("Oops! Something went wrong\n")
                    
    def login(self, password, email_id):
        
        with open(f"{name}.txt","r") as f:
                details = f.read()
                self.user_details=details.split("\n")
        mycursor=connection.cursor()
        sql = 'select * from registration where password =%s and email_id=%s'
        mycursor.execute(sql,(password, email_id))
        result=mycursor.fetchall()
        for i in result:
            self.loggedin=True

        if self.loggedin==True:
            print(f"{name} logged in \n")
            self.bal=int(self.user_details[8])
            self.name=name

        else:
            print("Account does nit exist\n")
        
    def deposit_money(self, deposit_amount, transactionfilename, name, account_no):
        prev_bal=self.bal
        new_bal=self.new_bal
        try:
            deposit_amount % 100 == 0
            new_bal = prev_bal + deposit_amount
            with open(transactionfilename,'a') as file:
                prev_bal = str(prev_bal)
                new_bal = str(new_bal)
                deposit_amount = str(deposit_amount)
                file.write('\nPrevious balance: '+prev_bal+'. Deposit amount is: '+deposit_amount+'. New balance: '+new_bal+'. date_time: '+str(datetime.datetime.now())+'\n')

            with open(f"{self.name}.txt","r") as f:
                details_2 = f.read()
                self.user_details = details_2.split("\n")
               
            with open(f"{self.name}.txt","w") as f:
                f.write(details_2.replace(str(self.user_details[8]),str(new_bal)))
            file.close()
            with connection.cursor() as cursor:
                sql1 = "insert into transaction(name,account_no, deposit_amount, prev_bal, new_bal) values (%s,%s,%s,%s,%s)"
                cursor.execute(sql1,(name,account_no, deposit_amount, prev_bal, new_bal))
                print("Amount Deposited Successfully")
            self.bal = int(new_bal)
            mycursor=connection.cursor()
            sql2="update registration set bal=%s where account_no=%s"
            mycursor.execute(sql2,(self.bal, account_no))
            print("Balance updated!\n")
            connection.commit()
            
        except:
            print("Enter amount in multiple of 100\n")
        

    def withdraw_money(self, withdraw_amount, transactionfilename, name, account_no):
        prev_bal=self.bal
        new_bal=self.new_bal
        try:
            withdraw_amount < int(prev_bal)
            new_bal = int(prev_bal) - withdraw_amount
            with open(transactionfilename,'a') as file:
                prev_bal = str(prev_bal)
                new_bal = str(new_bal)
                withdraw_amount = str(withdraw_amount)
                file.write('\nPrevious balance: '+prev_bal+'. Withdraw amount is: '+withdraw_amount+'. New balance: '+new_bal+'. date_time: '+str(datetime.datetime.now())+'\n')
        
            with open(f"{self.name}.txt","r") as f:
                details_2 = f.read()
                self.User_details = details_2.split("\n")
            
            with open(f"{self.name}.txt","w") as f:
                f.write(details_2.replace(str(self.user_details[8]),str(new_bal)))
            file.close()
            try:
                with connection.cursor() as cursor:
                    sql = "insert into transaction(name, account_no, withdraw_amount, prev_bal, new_bal) values (%s,%s,%s,%s,%s)"
                    cursor.execute(sql,(name, account_no, withdraw_amount, prev_bal, new_bal))
                    print("Amount Withdrawn Successfully\n")
                connection.commit()
            except:
                print("Oops! Something went wrong")
                
            self.bal = int(new_bal)
            mycursor=connection.cursor()
            sql="update registration set bal = %s where account_no = %s"
            mycursor.execute(sql,(self.bal, account_no))
            print("Balance Updated!\n")
            connection.commit()
        except:
            print("Insufficient balance")
    
    
    def password_change(self, new_password, account_no):
        if re.fullmatch('^[A-Za-z0-9@#$%^&+=]{8,}$', new_password):
            with open(f"{self.name}.txt","r") as f:
                details = f.read()
                self.user_detailst = details.split("\n")                                      

            with open(f"{self.name}.txt","w") as f:
                f.write(details.replace(str(self.user_details[1]),str(new_password)))
            mycursor=connection.cursor()
            sql="update registration set password = %s where account_no= %s"
            mycursor.execute(sql,(new_password, account_no))
            print("New Password Updated Successfully!\n")
            connection.commit()
            connection.close()
        else:
            print("Invalid password\n")

    def email_change(self, new_email, account_no):
        if re.fullmatch('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', new_email):
            with open(f"{self.name}.txt","r") as f:
                details = f.read()
                self.user_details = details.split("\n")                                      

            with open(f"{self.name}.txt","w") as f:
                f.write(details.replace(str(self.user_details[2]),str(new_email)))
            mycursor=connection.cursor()
            sql="update registration set email_id = %s where account_no= %s"
            mycursor.execute(sql,(new_email, account_no))
            print("New email Updated Successfully!\n")
            connection.commit()
            connection.close()
        else:
            print("Invalid email id\n")

    def phone_change(self, new_phone, account_no):
        if re.fullmatch(r'(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}', new_phone):
            with open(f"{self.name}.txt","r") as f:
                details = f.read()
                self.user_details = details.split("\n")                                      

            with open(f"{self.name}.txt","w") as f:
                f.write(details.replace(str(self.user_details[4]),str(new_phone)))
            mycursor=connection.cursor()
            sql="update registration set phone_no = %s where account_no= %s"
            mycursor.execute(sql,(new_phone, account_no))
            print("New Phone no. Updated Successfully!\n")
            connection.commit()
            connection.close()
        else:
            print("Invalid phone no.\n")

    def address_change(self, new_address, account_no):
        with open(f"{self.name}.txt","r") as f:
            details = f.read()
            self.user_details = details.split("\n")                                      

        with open(f"{self.name}.txt","w") as f:
            f.write(details.replace(str(self.user_details[5]),str(new_address)))
        mycursor=connection.cursor()
        sql="update registration set address = %s where account_no= %s"
        mycursor.execute(sql,(new_address, account_no))
        print("New Address Updated Successfully!\n")
        connection.commit()
        connection.close()
    
        
        
if __name__ == "__main__":
    while True:
        User_object = User()
        print('*'*100,'\n')
        print("Welcome to HANA Bank\n")
        print("What do you want to do?")
        print("1.Login\n2.Register\n3.About us\n4.Exit\n")
        print('*'*100,'\n')
        choice = int(input("Enter your choice: "))

        if choice==1:
            print("Logging in")
            name = input("Enter Name: ")
            password = input("Enter Password: ")                                    
            email_id = input("Enter Email Id: ")
            User_object.login(password, email_id)
            while True:
                if User_object.loggedin:
                    print('*'*100,"\n")
                    print("1.Deposit Money")
                    print("2.Withdraw Money")
                    print("3.Show Balance")
                    print("4.Show Transaction")
                    print("5.Show Profile")
                    print("6.Edit Profile")
                    print("7.Delete Account")
                    print("8.Logout\n")
                    print("*"*100,"\n")
                    login_user = int(input("Enter your choice: "))
                    if login_user == 1:
                        print("Balance:",User_object.bal)
                        deposit_amount=int(input("Enter amount to deposit: "))
                        name = input("Enter Name: ")
                        account_no = input("Enter Account no.: ")
                        transactionfilename = name+'_transactionhistory.txt'
                        User_object.deposit_money(deposit_amount, transactionfilename, name, account_no)
                        continue

                    elif login_user == 2:
                        print("Balance:",User_object.bal)
                        withdraw_amount=int(input("Enter amount to withdraw: "))
                        name = input("Enter Name: ")
                        account_no = input("Enter Account no.: ")
                        transactionfilename = name+'_transactionhistory.txt'
                        User_object.withdraw_money(withdraw_amount, transactionfilename, name, account_no)
                        continue

                    elif login_user == 3:
                        print("Balance:",User_object.bal)
                        continue

                    elif login_user == 4:
                        name = input("Enter name: ")
                        transactionfilename = name+'_transactionhistory.txt'
                        transactionfile = open(transactionfilename,'a')
                        with open (transactionfilename,'r') as file:
                            file.seek(0)
                            if file.read(1):
                                print(file.read())
                                file.close()
                            else:
                                print("There is no transaction history")
                                continue

                    elif login_user == 5:
                        name = input("Enter Name: ")
                        mycursor=connection.cursor()
                        sql = "select * from registration where name=%s"
                        mycursor.execute(sql,(name))
                        result = mycursor.fetchone()
                        print("\n",'-'*100)
                        print("\nAccount details:")
                        print("Name:",result[0])
                        print("Password:",result[1])
                        print("Email id:",result[2])
                        print("Aadhar no.:",result[3])
                        print("Phone no.:",result[4])
                        print("Address:",result[5])
                        print("Gender:",result[6])
                        print("Account no.:",result[7])
                        print("Balance:",result[8])
                        print("\n",'-'*100)
                        connection.commit()
                        continue

                    elif login_user == 6:
                        print("\n1.Change Password\n2.Change Email id\n3.Change Phone no.\n4.Change Address\n")
                        edit_profile = int(input("Enter choice: "))
                            
                        if edit_profile == 1:
                            new_password = input("Enter new password: ")
                            account_no = input("Enter account number: ")
                            User_object.password_change(new_password, account_no)
                            continue
                        elif edit_profile == 2:
                            new_email = input("Enter new Email id: ")
                            account_no = input("Enter account number: ")
                            User_object.email_change(new_email, account_no)
                            continue

                        elif edit_profile == 3:
                            new_phone = int(input("Enter new Phone Number: "))
                            account_no = input("Enter account number: ")
                            User_object.phone_change(new_phone, account_no)
                            continue

                        elif edit_profile == 4:
                            new_address = input("Enter new Address: ")
                            account_no = input("Enter account number: ")
                            User_object.address_change(new_address, account_no)
                            continue

                    elif login_user == 7:
                        account_no = input("Enter Account No: ")
                        name = input("Enter Name: ")
                        transactionfilename = name+'_transactionhistory.txt'
                        import os  
                        os.remove(f"{name}.txt")
                        os.remove(transactionfilename)
                        mycursor=connection.cursor()
                        sql1 = 'delete from registration where account_no = %s'
                        sql2 = 'delete from transaction where account_no = %s'
                        mycursor.execute(sql1,(account_no))
                        mycursor.execute(sql2,(account_no))
                        connection.commit()
                        connection.close()
                        print("Account has been deleted!\n")
                        break

                    elif login_user == 8:
                        print("You have been logged out!\n")
                        break
            continue    
                   

        if choice == 2:
            name = input("Enter Name: ")
            password = input("Enter Password: ")
            email_id = input("Enter Email id: ")
            aadhar_no = input("Enter aadhar no: ")
            phone_no = input("Enter phone no: ")
            address = input("Enter address: ")
            gender = input("Enter gender: ")
            have_account = int(input("Do you have account number?\n1.Yes\n2.No\n"))
            if have_account == 1:
                print("Enter Your account no:")
                account_no =input()
            elif have_account == 2:
                print("Your account number is:")
                account_no = random.randrange(1111111111,9999999999)
                print(account_no)
            User_object.register(name,password,email_id,aadhar_no,phone_no,address,gender,account_no)
            continue
        
        if choice == 3:
            print("Welcome to HANA Bank")
            mycursor=connection.cursor()
            sql1 = "select count(name) from registration"
            mycursor.execute(sql1)
            result=mycursor.fetchall()
            print("Number of Customers:",result[0][0])
            mycursor.execute('select sum(bal) from registration')
            print("Total Money in Bank: Rs.",mycursor.fetchall()[0][0])
            sql2 = 'select name from registration'
            mycursor.execute(sql2)
            print("Customer Names:\n",mycursor.fetchall())
            connection.commit()
            connection.close()
            continue
        
        if choice == 4:
            print("Thank you for visiting!")
            break
            
            
                             
                    

                 
                    

            
                    
                    
        
        
          
    
