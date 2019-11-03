'''
Created on 3 Nov 2019

@author: ramya.pendyala
'''
#Test execution file
from TestCases.TC_01_Valid_Program_MM import MM_Validation
import threading

Validation = MM_Validation()
#Authentication
Validation.auth()

#xml file creation     
Validation.file_creation()

#Ingesting xml file to QTS
Validation.file_Ingestion()

#Check for the process every 5 seconds.
#On the 1st 5 sec, the process will still be running and 
#every 5 sec it tells user that process is still running until it is completed
WAIT_TIME_SECONDS = 5
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    Validation.process_Validate()
