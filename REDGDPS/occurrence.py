import streamlit as st
import pymongo as py
from collections import Counter

from encrypt import encrypt_data
from decrypt import decrypt_data

myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]

# Function to get top 10 patients with highest occurrence
def get_top_patients_uuids():
    all_patients = medical_data_coll.find({}, {"uuid": 1})  # Assuming "uuid" is the field containing patient UUIDs
    patient_uuids = [patient["uuid"] for patient in all_patients]

    top_patients = Counter(patient_uuids).most_common(10)
    top_patient_uuids = [patient[0] for patient in top_patients]

    return top_patient_uuids

def identify_patient(top_patient_uuids):

    patients_list=[]

    for patient_uuid in top_patient_uuids:
        query= demographic_data_coll.find_one({"uuid": patient_uuid})
        patient_name=decrypt_data(query["demographic data"]["identities"][0]["details"]["items"][0]["value"]["value"])
        patient_surname=decrypt_data(query["demographic data"]["identities"][0]["details"]["items"][1]["value"]["value"])
        phone_number=decrypt_data(query["phone number"])
        gender=decrypt_data(query["demographic data"]["details"]["items"][3]["value"]["value"])
        
        symbol="Mrs"
        if gender=="MALE":
            symbol="Mr"
        
        detailed_ident= symbol + " " + patient_name + " " + patient_surname +", Phone number:("+phone_number+")"

        patients_list.append(detailed_ident)
    return patients_list