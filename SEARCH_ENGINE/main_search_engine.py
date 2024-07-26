import streamlit as st
import pymongo as py

from SEARCH_ENGINE.demographic_queries import demographic_queries_list
from SEARCH_ENGINE.medical_data_queries import med_data_queries_list
from SEARCH_ENGINE.medical_history_queries import med_hist_queries_list, create_med_hist_condition
from SEARCH_ENGINE.age_querying import query_age,create_age_condition

from SEARCH_ENGINE.common_uuids import extract_common_elements,create_csv_and_display
from SEARCH_ENGINE.verification import previous_decision
from SEARCH_ENGINE.dictionary_generation import dict_generation
from SEARCH_ENGINE.plots import plotting

from decrypt import decrypt_data

#-----------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]

#Consents collection:
consents_coll=myclient["Consents"]["Consents Collection"]
#-----------------------------------------------------------------------------

def main_search_engine_function():
    values_strings_demographics=["Name","Surname","DNI","Gender","Country of birth","Province of birth","Town of birth","Street name","Postal Code","Country","Province","Town"]
    #values_dates_demographics=["Birth date",]

    all_demog_values_list= values_strings_demographics #+ values_dates_demographics

    chosen_parameters_demog=st.multiselect(
        'Choose demographic conditions combo:',
        (all_demog_values_list)
    )

    st.write("#")
    clinical_data_list=["Age","Vital status","Symptoms", "Clinical desease", "cardiovascular risk factors"]

    chosen_parameters_med_data=st.multiselect(
        'Choose medical data conditions combo:',
        (clinical_data_list)
    )

    st.write("#")
    analytics_med_hist=["HbA1c", "UACR", "eGFR", "BMI", "Creatinine_Phosphokinase", "Ejection_fraction", "Platelets", "Serum_Creatinine", "Serum_Sodium"]

    chosen_parameters_med_hist=st.multiselect(
        'Choose medical history conditions combo:',
        (analytics_med_hist)
    )

    chosen_parameters = chosen_parameters_demog + chosen_parameters_med_data + chosen_parameters_med_hist

    #query_demog_list is a list of all demographic queries
    query_demog_list= demographic_queries_list(chosen_parameters_demog)

    if "Age" in chosen_parameters_med_data:
        age_condition_list=create_age_condition()

    #query_med_data_list is a list of all medical data queries
    query_med_data_list = med_data_queries_list(chosen_parameters_med_data)

    #query_med_hist_list is a list of all medical history queries
    query_med_hist_list = create_med_hist_condition(chosen_parameters_med_hist)

    if len(chosen_parameters):
        st.write("#")
        st.write("#")

        #Adding a button to launch search engine once clicked.
        col1, col2, col3 = st.columns([4,2,3])
        with col2:
            get_result = st.button('GET QUERY RESULT')

        if get_result :

            #Querying the demographic data based on conditions:
            query_demog={}
            if len(query_demog_list):
                query_demog={"$and": query_demog_list}

            cursor_demog = demographic_data_coll.find(query_demog)

            query_demog_result=[]
            for doc in cursor_demog:
                query_demog_result.append(doc["uuid"])


            #Querying the medical data based on conditions:
            query_med_data={}
            if len(query_med_data_list):
                query_med_data={"$and": query_med_data_list}

            cursor_med_data = medical_data_coll.find(query_med_data)

            query_med_data_result=[]
            for doc in cursor_med_data:
                query_med_data_result.append(doc["uuid"])

            if "Age" in chosen_parameters_med_data:
                age_uuids = query_age(age_condition_list)

                query_med_data_result=list(set(query_med_data_result) & set(age_uuids))


            #Querying the medical history data based on conditions:
            query_med_hist_result = med_hist_queries_list(query_med_hist_list)


            #Matching "uuid":
            #this function extracts the list of common "uuid"s.
            common_uuid=extract_common_elements(query_demog_result,query_med_data_result,query_med_hist_result)
            
            #consent_uuids is the list of "uuid" of all patients that accepted to share their medical data (Anonymized)
            if len(common_uuid)<=3:
                #extracting uuids of patients with consents:
                consent_uuids=[]
                for uuid_value in common_uuid:
                    patient_name = decrypt_data(demographic_data_coll.find_one({"uuid":uuid_value})["demographic data"]["identities"][0]["details"]["items"][0]["value"]["value"])
                    decision=previous_decision(patient_name,uuid_value)
                    if decision!= "NO":
                        consent_uuids.append(uuid_value)
            else:
                consent_uuids=common_uuid

            st.write("#")

            if consent_uuids:

                csv_dict=dict_generation(consent_uuids)
                df=create_csv_and_display(csv_dict)
                plotting(df)
                
            else:
                st.error("No result found for this query")


    else:
        st.warning("You need to choose a variable to create a condition")
