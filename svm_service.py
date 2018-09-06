#!/usr/bin/python3
import csv
import json
from pprint import pprint

svm_header = ["row_id", "Client id","First Name","Last Name","Age","Gender","Location","Nationality",
              "Country of Domicile","Business Sponsor","Client Class Description","Product Name",
              "Product ISIN","Product Category","Trade Direction","Interaction DateTime",
              "HAPPYConfidence","ANGRYConfidence","CONFUSEDConfidence","SADConfidence",
              "SURPRISEDConfidence","CALMConfidence","MouthOpen","Confidence","SmileConfidence"]

svm_file = '/home/vikas/Programs/rekognition/static/support_vector_machine.csv'
    
class SVMClient(object):
    def __init__(self):
        self.svm_list = []
        with open (svm_file, "r") as svm_csv:
            svm_lines = svm_csv.readlines()
        for svm_line_raw in svm_lines:
            svm_line = ''.join(c for c in svm_line_raw.strip() if c <= '\u007E')
            if len(svm_line) > 0: 
                json_obj = {}
                indx = 0
                for f in svm_line.split (sep=","):
                    json_obj[svm_header[indx]] = f
                    indx += 1
                self.svm_list.append (json_obj)        

        print ("Initialized SVM Client Object")
        print ("Vector Size: ", len(self.svm_list))
        pprint (self.svm_list)

print ("svm client created")
svm_client = SVMClient()
        
def get_svm_data (product_id: str) -> 'list' :
    result = []
    for svm_row in svm_client.svm_list:
        if product_id == svm_row["Product ISIN"]:
            result.append (svm_row)
    return result

