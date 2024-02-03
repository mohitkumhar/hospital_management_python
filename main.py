import re
from dotenv import load_dotenv
import os
import maskpass
from datetime import datetime
import pymongo
from tabulate import tabulate
import smtplib

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['Hospital']
mycol = mydb['Patient Details']

schedule_col = mydb['Schedule Patient Details']

load_dotenv()


def send_schedule_patient_mail(email, timing):
    HOST = 'smtp.gmail.com'
    PORT = 465
    FROM_EMAIL = os.environ['FROM_EMAIL']
    PASSWORD = os.environ['PASSWORD']
    TO_EMAIL = email

    MESSAGE = f'''Subject: ABC Hospital

    Your Meeting is Scheduled Successfully on {timing}

    Please be on Time

    Thanks
    '''

    smtp = smtplib.SMTP_SSL(HOST, PORT)

    smtp.login(FROM_EMAIL, PASSWORD)
    smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)


def isValidEmail(email):
    check = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(check, email)


print("Hello..!! Its Glade to See You Again :)")
print("Please Login: ")

while (True):
    new_admin_email = input("Enter Your Email: ").lower()

    if (isValidEmail(new_admin_email)):
        new_admin_password = maskpass.askpass(
            prompt="Enter Yore Password: ", mask='*')
    else:
        print("Please, Enter Correct Email...")
        continue

    if (new_admin_email == os.environ['admin_login_email'] and new_admin_password == os.environ['admin_login_password']):
        break
    else:
        print("Entered Password or Email is Wrong..!! Please Try Again")
        continue


while (True):
    print(
        '''Enter Your Choice:
        [1]. Enter New Patient Details
        [2]. Check Registered Patient Details
        [3]. Schedule Appointment
        [4]. Update Patient Details
        [5]. View Scheduled Appointment List
        [6]. Check All Patient List
        [7]. Exit'''
    )

    user = int(input("Enter Above Options: "))

    if user == 1:

        name = input("Enter Your Full Name: ").capitalize()
        while (True):
            email = input("Enter Your Email: ").lower()
            if (isValidEmail(email)):

                used_email = mycol.find_one({"Email": email})
                if (used_email):
                    print("Patient is Already Registered")
                    print("You Can Check Old Details, If You Want")

                break
            else:
                print("Please Enter Valid Email")
                continue

        while (True):
            try:
                dob_str = input("Enter Your Date of Birth(YYYY-MM-DD): ")
                dob = datetime.strptime(dob_str, '%Y-%m-%d')
                current_year = datetime.now().year
                if dob.year < current_year-120 and dob.year > current_year:
                    print("Please Enter Valid Date Of Birth")
                    continue
                else:
                    break
            except:
                print("Please Enter Date in Valid Format")

        while (True):
            gender = input("Enter Your Gender (Male/Female/Other): ").lower()
            if (gender == 'male' or gender == 'female' or gender == 'other'):
                break

            elif(gender == 'm'):
                gender = 'male'
                break

            elif(gender == 'f'):
                gender = 'female'
                break

            elif(gender == 'o'):
                gender = 'other'
                break

            else:
                print("Please Enter Correct Gender")

        while (True):
            number = input("Enter Your Mobile Number: ")
            if number.isdigit() and len(number) == 10:
                break
            else:
                print("Please Enter Correct Contact Number...")

        street = input("Enter Your Address: ").lower()
        district = input("Enter Your District: ").lower()
        state = input("Enter Your State: ").lower()

        new_patient = {"name": name, "email": email, "date of birth": dob_str, "gender": gender,
                       "contact number": number, "address": {"street": street, "district": district, "state": state}}

        mycol.insert_one(new_patient)

    if user == 2:
        while (True):
            email = input("Enter Patient Email: ").lower()
            if (isValidEmail(email)):
                patient = mycol.find_one({"email": email}, {
                                         '_id': 0, 'name': 1, 'email': 1, 'date of birth': 1, 'gender': 1, 'contact number': 1, 'address': 1})
                if patient:
                    address_details = patient['address']

                    registered_patient_data = {

                        'Name': [patient.get('name', 'Name Not Found')],
                        'E-Mail': [patient.get('email', 'Email Not Found')],
                        'Contact': [patient.get('contact number', 'Contact Details Not Found')],
                        'Date of Birth': [patient.get('date of birth', "DOB Not Found")],
                        'Gender': [patient.get('gender', 'Gender Not Found')],
                        'Street': [address_details.get('street', '   - ')],
                        'District': [address_details.get('district', '   - ')],
                        'State': [address_details.get('state', '   - ')],
                    }

                    print(tabulate(registered_patient_data,
                          headers='keys', tablefmt='psql', showindex='always'))
                    break

                else:
                    print("Patient Details Not Found")
                    break
            else:
                print("Please Enter Valid Email")
                continue

    if user == 3:
        print(
            " # # # # # # # # Enter Your Details for Schedule Appointment # # # # # # # # ")
        print()
        name = input("Enter Your Full Name: ").capitalize()

        while (True):
            email = input("Enter Your Email: ").lower()
            if (isValidEmail(email)):

                used_email = mycol.find_one({"Email": email})
                if (used_email):
                    print("Patient is Already Registered")
                    print("You Can Check Old Details, If You Want")

                break
            else:
                print("Please Enter Valid Email")
                continue

        while (True):
            try:
                schedule_time = input(
                    "Enter Your Timing Schedule (YYYY-MM-DD HH:MM): ")
                st = datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
                if st < datetime.now():
                    print("Please Enter Valid Date...")
                else:
                    break

            except ValueError:
                print("Please Enter Timing in Given Format")
                continue

        while (True):
            try:
                dob_str = input("Enter Your Date of Birth(YYYY-MM-DD): ")
                dob = datetime.strptime(dob_str, '%Y-%m-%d')
                current_year = datetime.now().year
                if dob.year < current_year-120 and dob.year > current_year:
                    print("Please Enter Valid Date Of Birth")
                    continue
                else:
                    break
            except:
                print("Please Enter Date in Valid Format")

        while (True):
            gender = input("Enter Your Gender (Male/Female/Other): ").lower()
            if (gender == 'male' or gender == 'female' or gender == 'other'):
                break
            
            elif(gender == 'm'):
                gender = 'male'
                break

            elif(gender == 'f'):
                gender = 'female'
                break

            elif(gender == 'o'):
                gender = 'other'
                break

            else:
                print("Please Enter Correct Gender")


        while (True):
            number = input("Enter Your Mobile Number: ")
            if number.isdigit() and len(number) == 10:
                break
            else:
                print("Please Enter Correct Contact Number...")

        street = input("Enter Your Address: ").lower()
        district = input("Enter Your District: ").lower()
        state = input("Enter Your State: ").lower()

        new_patient = {"name": name, "email": email, "pending schedule": schedule_time, "date of birth": dob_str,
                       "gender": gender, "contact number": number, "address": {"street": street, "district": district, "state": state}}

        schedule_col.insert_one(new_patient)
        send_schedule_patient_mail(email, schedule_time)

    if user == 4:
        updation_data = {}
        while (True):
            update_patient_information_by_email = input(
                "To Update Patient Information Please Enter Patient Email: ").lower()
            if (isValidEmail(update_patient_information_by_email)):
                break
            else:
                print("Please Enter Valid Email")
                continue

        exist_email_updation_informaiton = mycol.find_one(
            {'email': update_patient_information_by_email})

        if exist_email_updation_informaiton:

            name = input(
                "Enter Your Full Name(Leave Black For No Changes): ").capitalize()
            if name:
                updation_data['name'] = name

            while (True):
                email = input(
                    "Enter Your Email(Leave Black For No Changes): ").lower()
                if email:

                    if (isValidEmail(email)):
                        updation_data['email'] = email
                        break
                    else:
                        print("Please Enter Valid Email")
                        continue
                else:
                    break

            while (True):
                try:
                    dob_str = input(
                        "Enter Your Date of Birth (YYYY-MM-DD)(Leave Black For No Changes): ")
                    if dob_str:
                        dob = datetime.strptime(dob_str, '%Y-%m-%d')
                        current_year = datetime.now().year
                        if dob.year < current_year-120 and dob.year > current_year:
                            print("Please Enter Valid Date Of Birth")
                            continue
                        else:
                            updation_data['date of birth'] = dob_str
                            break
                    else:
                        break
                except:
                    print("Please Enter Date in Valid Format")

            while (True):
                gender = input(
                    "Enter Your Gender (Male/Female/Other)(Leave Black For No Changes): ").lower()
                if gender:
                    if (gender == 'male' or gender == 'female' or gender == 'other' or gender == 'm' or gender == 'f' or gender == 'o'):
                        updation_data['gender'] = gender
                        break
                    else:
                        print("Please Enter Correct Gender")
                        continue
                else:
                    break

            while (True):
                number = input(
                    "Enter Your Mobile Number(Leave Black For No Changes): ")
                if number:
                    if number.isdigit() and len(number) == 10:
                        updation_data['contact number'] = number
                        break
                    else:
                        print("Please Enter Correct Contact Number...")
                else:
                    break

            street = input(
                "Enter Your Address(Leave Black For No Changes): ").lower()
            if street:
                updation_data['street'] = street

            district = input(
                "Enter Your District(Leave Black For No Changes): ").lower()
            if street:
                updation_data['street'] = street

            state = input(
                "Enter Your State(Leave Black For No Changes): ").lower()
            if street:
                updation_data['street'] = street

        print(updation_data)
        mycol.update_one({'email': update_patient_information_by_email}, {
                         '$set': updation_data})
        print("Information Updated")

        print(tabulate(data, headers='keys', tablefmt='psql', showindex='always'))

    if user == 5:
        all_data = []
        print("List of Scheduled Patient is: ")

        for i in schedule_col.find():
            address_det = i['address']
            data = {
                'Name': i.get('name', 'Name Not Found'),
                'Email': i.get('email', 'Email Not Found'),
                'Pending Schedule': i.get('pending schedule', 'Schedule Not Found'),
                'Contact Number': i.get('contact number', 'Contact Number Not Found'),
                'Date Of Birth': i.get('date of birth', "Date of Birth Not Found"),
                'Gender': i.get('gender', 'Gender Not Found'),
                'Street': address_det.get('street', 'Street Not Found'),
                'District': address_det.get('district', 'District Not Found'),
                'State': address_det.get('state', 'State Not Found'),
            }
            all_data.append(data)

        print(tabulate(all_data, headers='keys',
              tablefmt='psql', showindex='always'))

    if user == 6:
        print("The List of All Patient is: ")
        main_data_all_patient_details = []

        for i in mycol.find():
            address_details = i['address']
            all_patient_data = {
                'Name': i.get('name', 'Name Not Found'),
                'E-Mail': i.get('email', 'E-Mail Not Found'),
                'Contact Number': i.get('contact number', 'Contact Number Not Found'),
                'Gender': i.get('gender', 'Gender Not Found'),
                'Date of Birth': i.get('date of birth', 'Date of Birth Not Found'),
                'Street': address_details.get('street', 'Street Details Not Found'),
                'District': address_details.get('district', 'District Details Not Found'),
                'State': address_details.get('state', 'State Details Not Found'),
            }
            main_data_all_patient_details.append(all_patient_data)
        print(tabulate(main_data_all_patient_details, headers='keys', tablefmt='psql', showindex='always'))

    if user == 7:
        break
    else:
        print("Please, Enter Correct Options")
print("Thanks You, See You Soon")


