import streamlit as st
import pymongo as py

from paths import parameter_to_directory

from encrypt import encrypt_data
from decrypt import decrypt_data

myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]

def create_age_condition():
    
    condition_list=[]

    st.header("AGE:")
    col01,col02,col03 = st.columns([1.25,.25,2])
    
    with col01:
        selected=st.selectbox(
            "Condition for Age:",
            ("equal","not equal","greater","lower","greater or equal","lower or equal", "between")
        )

    with col03:
        if selected=="between":

            lower_value = st.number_input(
                "Lower value of Age:",
                step=1
                )
            
            higher_value = st.number_input(
                "Higher value of Age:",
                min_value=lower_value,
                step=1
                )
            
            lower_value = lower_value
            higher_value = higher_value
           
        else:
            input_value = st.number_input(
                "Value of Age:",
                step=1
                )
            
    condition_list.append(selected)
    if selected=="between":
        condition_list.append(lower_value)
        condition_list.append(higher_value)

    else:
        condition_list.append(input_value)

    return condition_list
#--------------------------------------------------------------------------
def query_age(age_condition_list):
    uuids_list=[]

    selected=age_condition_list[0]
    if selected != "between":
        input_value= age_condition_list[1] 

    if selected=="equal":
        input_value=str(input_value)
        condition = {parameter_to_directory("Age"): encrypt_data(input_value)}
        query = medical_data_coll.find(condition)
        for doc in query:
            uuids_list.append(doc["uuid"])

    elif selected=="not equal":
        input_value=str(input_value)
        condition = {parameter_to_directory("Age"): {"$ne": encrypt_data(input_value)}}
        query = medical_data_coll.find(condition)
        for doc in query:
            uuids_list.append(doc["uuid"])
    
    else:

        query = medical_data_coll.find()

        ages_list=[]
        all_uuids=[]
        for doc in query:

            decrypted_age = int(decrypt_data(doc["age"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]))
            ages_list.append(decrypted_age)
            all_uuids.append(doc["uuid"])
            
        
        if selected=="between":
            lower_value = age_condition_list[1]
            higher_value = age_condition_list[2]
            for index,age_value in enumerate(ages_list):
                
                if (lower_value <= age_value) & ( age_value <= higher_value) :
                    uuids_list.append(all_uuids[index])
        
        elif selected == "greater":
            for index,age_value in enumerate(ages_list):
                
                if age_value > input_value :
                    uuids_list.append(all_uuids[index])

        elif selected == "greater or equal":
            for index,age_value in enumerate(ages_list):
                
                if age_value >= input_value :
                    uuids_list.append(all_uuids[index])
        
        elif selected == "lower":
            for index,age_value in enumerate(ages_list):
                
                if age_value < input_value :
                    uuids_list.append(all_uuids[index])

        elif selected == "lower or equal":
            for index,age_value in enumerate(ages_list):
                
                if age_value <= input_value :
                    uuids_list.append(all_uuids[index])

    return(uuids_list)