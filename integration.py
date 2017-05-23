import pymysql.cursors
import requests
import json



#select callerid from call_entry;
#INSERT INTO contact (cedula_ruc, name, telefono, apellido) VALUES ("1090436676", "Diego Castro", "3168759827", "OpenBCO");

connection = pymysql.connect(host='192.168.100.34',
                             user='sap',
                             password='clavesap894518',
                             db='call_center',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

connection2qstats = pymysql.connect(host='192.168.100.34',
                             user='sap',
                             password='clavesap894518',
                             db='qstats',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def obtainTelNumbersFromHistory():

    try:
        with connection.cursor() as cursor:
            sql = "SELECT callerid from call_entry"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result
    except pymysql.InternalError as error:
        print ("Error: unable to fetch data")

def compareNumber(number):

    with connection2qstats.cursor() as cursor:
        query = "SELECT * FROM Contacts WHERE PhoneNumer=%s"
        cursor.execute(query, number )
        result = cursor.fetchall()
        print(result)
        if result:
            print "Se encontro el numero"
            return True
        else:
            print "No se encontro"
            return False

def createContactInCallCenter(contactData):
    #t = ('1090435567', 'Test', '232322', 'Empresa')
    jsonObj = json.loads(contactData)
    t = (jsonObj[0]['nitNumber'], jsonObj[0]['firstName'], jsonObj[0]['number'], jsonObj[0]['companyName'])

    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO contact (cedula_ruc, name, telefono, apellido) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, t)
            connection.commit()
            print ("Contacto creado en CallCenter")
    except pymysql.InternalError as error:
        print ("Error: unable to create contact")

def createContactInQstats(contactData):
    print ("Voy a crear contacto")
    print contactData
    try:
        jsonObj = json.loads(contactData)
        print (jsonObj[0])
        t = (jsonObj[0]["firstName"], jsonObj[0]["companyName"], jsonObj[0]["number"])
    except:
        print ("No se encontraron contactos por cargar")

    #t = (str(contactData['nitNumber']), str(contactData['FirstName']), str(contactData['number']), str(contactData['companyName']))


    try:
        with connection2qstats.cursor() as cursor:
            query = "INSERT INTO Contacts (FirstName, CompanyName, PhoneNumer) VALUES (%s, %s, %s)"
            cursor.execute(query, t)
            #cursor.execute(query)
            connection.commit()
            print ("Contacto creado en Qstats")
    except pymysql.InternalError as error:
        print ("Error: unable to create contact")


def createContact(number):
    #Busco la info del contacto en SAP
    print (number)
    searchParams = {
        "phoneNumber":number
    }
    API_URL = "http://localhost:1337/contact/getCostumerInfo"
    r = requests.get(API_URL, params=searchParams)

    print ("Response: ")
    print (r.text)
    createContactInQstats(r.text)
    createContactInCallCenter(r.text)

def ObtainUnansweredCalls():

    searchParams = {
        "start":"2017-04-10",
        "end":"2017-04-12"
    }

    URL = "https://192.168.100.34/stats/rest/index.php?entity=reports/unanswered_calls_detail"
    URL = "https://192.168.100.34/stats/rest/index.php?entity=reports/answered_calls_detail"

    r = requests.get(URL, params=searchParams, verify=False, auth=('admin','telconet894518'))
    print r.text
    dataObj = json.loads(r.text)

    rows = dataObj['rows']
    for row in rows:
        number = row['callerid']
        if (compareNumber(number)):
            print ("Numero ya existe, no hago nada")
        else:
            print ("Debo crear numero en contactos")
            try:
                createContact(number)
            except Exception as e:
                print (e)
                pass




#obtainTelNumbers()
#compareNumber("23")
#createContact()
ObtainUnansweredCalls()
