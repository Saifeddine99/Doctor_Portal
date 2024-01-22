import streamlit as st
import pymongo as py

from paths import parameter_to_directory

from encrypt import encrypt_data
from decrypt import decrypt_data

#-----------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

analytics_med_hist=["HbA1c", "UACR", "eGFR", "BMI", "Creatinine_Phosphokinase", "Ejection_fraction", "Platelets", "Serum_Creatinine", "Serum_Sodium"]

def create_med_hist_condition(chosen_parameters_med_hist):

    conditions_list=[]
    if len(chosen_parameters_med_hist)>0:
        for value in chosen_parameters_med_hist:
            value_condition=[]

            st.header(value.upper()+":")

            col01,col02,col03 = st.columns([1.25,.25,2])
            with col01:
                selected=st.selectbox(
                    "Condition for "+value+" :",
                    ("equal","not equal","greater","lower","greater or equal","lower or equal", "between")
                )
            with col03:

                if selected=="between":
                    lower_value = st.number_input(
                        "Lower value of "+value+":"
                        )
                    
                    higher_value = st.number_input(
                        "Higher value of "+value+":",
                        min_value=lower_value
                        )

                else:
                    input_value = st.number_input(
                        "Value of "+value+":"
                        )

            value_condition.append(value)        
            value_condition.append(selected)
            if selected=="between":
                value_condition.append(lower_value)
                value_condition.append(higher_value) 
            else:
                value_condition.append(input_value)

            conditions_list.append(value_condition)    

    return conditions_list

def med_hist_queries_list(conditions_list):
    #query_med_hist_list is a list of all medical history queries
    uuids_list=[]
    if len(conditions_list)>0:
        uuidzz_all_iterations=[]
        for condition in conditions_list:
            uuidzz_one_iteration=[]

            value = condition[0]
            selected = condition[1]
            if selected !="between":
                input_value= condition[2]
            
            if value == "BMI":

                if selected=="equal":

                    input_value= str(input_value)
                    query_med_hist={parameter_to_directory(value): encrypt_data(input_value)}
                    query= medical_hist_coll.find(query_med_hist)
                    for doc in query:
                        uuidzz_one_iteration.append(doc["uuid"])

                elif selected== "not equal":

                    input_value= str(input_value)
                    query_med_hist={parameter_to_directory(value): {"$ne": encrypt_data(input_value)}}
                    query= medical_hist_coll.find(query_med_hist)
                    for doc in query:
                        uuidzz_one_iteration.append(doc["uuid"])

                else:
                     
                    query = medical_hist_coll.find()
                    value_list=[]
                    all_uuids=[]

                    for doc in query:
                        try:
                            value_path=doc["analytics"][1]["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]
                            decrypted_value= float(decrypt_data(value_path))
                            value_list.append(decrypted_value)
                            all_uuids.append(doc["uuid"])
                        except:
                            pass

                    if selected=="between":

                        lower_value = condition[2]
                        higher_value = condition[3]

                        for index,actual_value in enumerate(value_list):
                            
                            if (lower_value <= actual_value) & ( actual_value <= higher_value) :
                                uuidzz_one_iteration.append(all_uuids[index])
                    
                    elif selected == "greater":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value > input_value :
                                uuidzz_one_iteration.append(all_uuids[index])

                    elif selected == "greater or equal":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value >= input_value :
                                uuidzz_one_iteration.append(all_uuids[index])
                    
                    elif selected == "lower":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value < input_value :
                                uuidzz_one_iteration.append(all_uuids[index])

                    elif selected == "lower or equal":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value <= input_value :
                                uuidzz_one_iteration.append(all_uuids[index])


            #------------------------------------------------------------------------------------------
            else:
                
                if selected == "equal":

                    input_value= str(input_value)
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): encrypt_data(value.upper()),
                        parameter_to_directory("laboratory test result"): encrypt_data(input_value)}
                    }}
                    query= medical_hist_coll.find(query_med_hist)
                    for doc in query:
                        uuidzz_one_iteration.append(doc["uuid"])

                elif selected == "not equal":
                    input_value= str(input_value)
                    query_med_hist={"$or":[{"analytics.0":
                    {"$elemMatch":
                       {parameter_to_directory("laboratory test name"): encrypt_data(value.upper()),
                        parameter_to_directory("laboratory test result"): {"$ne": encrypt_data(input_value)}}
                    }},
                    {"analytics.0"+"."+parameter_to_directory("laboratory test name"):{"$ne": encrypt_data(value.upper())}}
                    ]}
                    query= medical_hist_coll.find(query_med_hist)
                    for doc in query:
                        uuidzz_one_iteration.append(doc["uuid"])
                
                else:
                    
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): encrypt_data(value.upper())}
                    }}

                    query = medical_hist_coll.find(query_med_hist)

                    value_list=[]
                    all_uuids=[]
                    for doc in query:
                            for index, iter1 in enumerate(doc["analytics"][0]):
                                if iter1["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]== encrypt_data(value.upper()):
                                    encrypted_value = iter1["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]
                                    decrypted_value= float(decrypt_data(encrypted_value))
                                    break

                            value_list.append(decrypted_value)
                            all_uuids.append(doc["uuid"])

                    if selected=="between":
                        
                        lower_value = condition[2]
                        higher_value = condition[3]

                        for index,actual_value in enumerate(value_list):
                            
                            if (lower_value <= actual_value) & ( actual_value <= higher_value) :
                                uuidzz_one_iteration.append(all_uuids[index])
                    
                    elif selected == "greater":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value > input_value :
                                uuidzz_one_iteration.append(all_uuids[index])

                    elif selected == "greater or equal":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value >= input_value :
                                uuidzz_one_iteration.append(all_uuids[index])
                    
                    elif selected == "lower":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value < input_value :
                                uuidzz_one_iteration.append(all_uuids[index])

                    elif selected == "lower or equal":
                        for index,actual_value in enumerate(value_list):
                            
                            if actual_value <= input_value :
                                uuidzz_one_iteration.append(all_uuids[index])
                

            uuidzz_all_iterations.append(uuidzz_one_iteration)
        
        # Using set intersection to find common uuids
        common_uuidzz = set(uuidzz_all_iterations[0]).intersection(*uuidzz_all_iterations[1:])
        uuids_list=list(common_uuidzz)

            #Here we gonna add the specific query related to this chosen condition to the list of queries
    else:
        query=medical_hist_coll.find()
        for doc in query:
            uuids_list.append(doc["uuid"])

    return(uuids_list)