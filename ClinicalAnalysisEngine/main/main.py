## main.py
# Primary Owner: Clinical Analysis Team


from time import gmtime, strftime
import checkPythonVersion
import processRequest
import parseCLA
import logger
import socket
import sys
import os

#from ClinicalAnalysisEngine import Cat
#from ClinicalAnalysisEngine import sql_utils

###
### Check python version running this script
###
checkPythonVersion.ConfirmPythonVersion3()


###
### Get command line args (host and port)
###
host, port = parseCLA.Server_HostPort()


###
### Save this sessions settings to text file
###
f = open("pidport.conf", 'w')
f.write(str(os.getpid()) + "," + str(port))
f.close()


###
### Setup the socket
###
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))


###
### Main program loop (wait for a request)
###
while True:
    s.listen(1)
    conn, addr = s.accept()

    logger.PrintLog("Connected by: " + str(addr))

    try:
        rawData = conn.recv(1024)
        if not rawData: continue


        data = rawData.decode('utf-8')

        completedRequest = processRequest.ProcessRequest(data)
        #query = "SELECT * FROM pet WHERE " + completedRequest
        #print(query)

        #sql_data = sql_utils.get_dict(query)
        #cats = Cat.sql_data_to_cats(sql_data)
        #completedRequest = Cat.cats_to_json(cats)


        if(completedRequest == None):
            returnMsg = "ERROR: completed request was none"
            conn.sendall(returnMsg.encode('utf-8'))
        else:
            conn.sendall(completedRequest.encode('utf-8'))


    except socket.error:
        print("Error Occured. Did a client connect but not send anything?")
        continue

    finally:
        conn.close()
