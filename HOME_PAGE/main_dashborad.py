import streamlit as st

import pymongo as py

myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]

from encrypt import encrypt_data
from decrypt import decrypt_data

from HOME_PAGE.plots import gender_distribution, total_number, obesity_total, plot_horizontal_bar, hba1c_distribution, all_symptomatics, display_patient_info

def remove_duplicates(input_list):
    # Use set to remove duplicates and convert it back to a list
    unique_list = list(set(input_list))
    return unique_list

def main_dashboard_function():
    st.write("#")
    st.markdown("<h1 style='color: #0B5345;text-align: center;'>GlobalEHR DASHBOARD DEMO</h1>", unsafe_allow_html = True)
    st.write("#")

    cursor_demog= demographic_data_coll.find({})
    #Here, we'll be working on the distribution of patients based on gender
    all_genders=[]

    for cursor in cursor_demog:        
        gender=decrypt_data(cursor["demographic data"]["details"]["items"][3]["value"]["value"])
        all_genders.append(gender)

    #Here, we'll be working on displaying the comorbilities in a horizontal bar plot:

    total_number_diabetes= total_number("diabetes")
    total_number_anemia= total_number("anaemia")
    total_number_frailty= total_number("frailty")
    total_number_heart_failure= total_number("heart_failure")
    total_number_obesity= obesity_total()
    
    disease_names=["diabetes","Anaemia","Frailty","Heart_failure","Obesity"]
    patient_counts=[total_number_diabetes, total_number_anemia, total_number_frailty, total_number_heart_failure, total_number_obesity]

    left_plots,middle,right_plots=st.columns([2,0.2,4])

    with right_plots:
        list_uuids_over_9= hba1c_distribution()
        list_uuids_over_9= remove_duplicates(list_uuids_over_9)

        symptomatics_uuids_list= all_symptomatics()
        symptomatics_uuids_list= remove_duplicates(symptomatics_uuids_list)

        plot_horizontal_bar(disease_names, patient_counts)

    with left_plots:
        st.info(f"Till now, The total number of patients in our dataset is {len(all_genders)}")
        gender_distribution(all_genders)
        display_patient_info(list_uuids_over_9 ,symptomatics_uuids_list)

    

