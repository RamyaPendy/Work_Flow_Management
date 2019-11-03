'''
Created on 3 Nov 2019

@author: ramya.pendyala
'''
import pytest
import xml.etree.cElementTree as ET
import shutil
import json 
import requests
from config import *

@pytest.mark.WorkFlowEngine_test
class MM_Validation:
    @pytest.mark.run(order=1)
    def __init__(self):
        self.user = USERNAME
        self.token = API_TOKEN
        self.password = PASSWORD
        
    '''
    Assuming all operations  in work flow engine must be authorized
    '''
    #Authenticate before accessing QTS and MM
    @pytest.mark.run(order=2)
    def auth(self):
        try:
            requests.get('https://login/wfe', auth=(self.user,self.token))
            self.headers = {'Authorization': 'token ' + self.token}
        except:
            raise Exception('Cannot connect to the server')
    
    #xml file creation for program
    @pytest.mark.run(order=3)
    def file_creation(self):
    
        root = ET.Element("program")

        ET.SubElement(root, "name").text = "Friends"
        ET.SubElement(root, "start_time").text = "12:01:00"
        ET.SubElement(root, "end_time").text = "12:30:00"
        ET.SubElement(root, "duration").text = "29 minutes"
        ET.SubElement(root, "service_name").text = "Comedy Central"
        ET.SubElement(root, "service_id").text = "100"

        self.tree = ET.ElementTree(root)
        self.tree.write("Friends.xml")
        
    #Move the xml file to QTS folder
    @pytest.mark.run(order=4)
    def file_Ingestion(self):
        shutil.move('Friends.xml', '../qts_watch_folder/')
    
    #Check if the process is running
    @pytest.mark.run(order=5)    
    def process_Validate(self):
        response = requests.get('https://wfe/processes' , headers=self.headers)
        json_data = json.loads(response.text)
        if (response.status_code == 200 ):
            for sub_dict in json_data:
                if 'running' in sub_dict['status']:
                    print('process is still running')
                elif 'completed' in sub_dict['status']:
                    print('process completed')
                    #Check if data is created in Media Manager once the process is completed
                    MM_Validation.Validate_MM_Entity(self)
                    break
                    '''
                    Processed xml file will be deleted from the work flow engine.
                    '''
        else:
            raise Exception('Cannot connect to the server')
    
    #Verify data is created in Media Manager after the process is completed
    @pytest.mark.run(order=6)
    def Validate_MM_Entity(self):
        response = requests.get('https://mm/entities/program/Friends' , headers=self.headers)
        json_data = json.loads(response.data)
        if (response.status_code == 200):
            assert 'data' in json_data
            assert 'type' in json_data['type']
            assert 'name' in json_data['name']
            assert 'program_id' in json_data['program_id']
        elif (response.status_code == 404):
            print('Entity not found in the Media Manager')
        else:
            raise Exception('Cannot connect to the server')
            
        
            
        
        
    

