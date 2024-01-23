import pymongo as py
import streamlit as st

from decrypt import decrypt_data

from REDGDPS.plots import test_results_time_series, medications_list_table

#-----------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#-----------------------------------------------------------------------
def query_treatment(uuid):
    cursor_med_data = medical_data_coll.find({"uuid": uuid})
    medication_list=[]

    for cursor in cursor_med_data:
        #Here we put in a dictionary the list of recommended drugs for each time.
        drugs_dict={}
        try:
            for drug_json_file in cursor["medication list"]:
                drug=decrypt_data(drug_json_file["content"][0]["items"][0]["description"]["items"][0]["value"]["value"])
                dose=decrypt_data(drug_json_file["content"][0]["items"][0]["description"]["items"][2]["items"][3]["value"]["value"])
                drugs_dict[drug]=dose
        except:
            pass

        medication_list.append(drugs_dict)
        
    return medication_list

#------------------------------------------------------------------------
def query_analyses(uuid):
    cursor_med_hist = medical_hist_coll.find({"uuid": uuid})

    storage_dates_med_hist=[]
    hba1c_results_dict={}
    bmi_values_dict={}
    for cursor in cursor_med_hist:

        #Here we'll be extracting the date of storage of each document.
        try:
            decrypted_date=decrypt_data(cursor["check date"])
        except:
            decrypted_date=decrypt_data(cursor["saving date"])
        storage_dates_med_hist.append(decrypted_date)

        if len(cursor["analytics"][0]):
            #Here we'll be creting a list containing all the HbA1c records stored in Mongo.
            for test in cursor["analytics"][0]:
                test_name = decrypt_data(test["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"])
                if test_name == "HBA1C":
                    try:
                        test_value=float(decrypt_data(test["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]))
                        hba1c_results_dict[decrypted_date] = test_value
                        break

                    except:
                        pass
        try:                      
            if len(cursor["analytics"][1]):
                #Here we'll be creting a list containing all the BMI values stored in Mongo.
                
                bmi_value=float(decrypt_data(cursor["analytics"][1]["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]))
                bmi_values_dict[decrypted_date] = bmi_value
        except:
            pass
    
    return storage_dates_med_hist, hba1c_results_dict, bmi_values_dict

#--------------------------------------------------------------------
def callback():
    st.session_state.clinical_interface= True
    st.session_state.add_new_patient=False

def plots_displaying(query_condition):
    cursor_patient = demographic_data_coll.find_one(query_condition)

    if cursor_patient:
        patient_uuid=cursor_patient["uuid"]
        patient_name=decrypt_data(cursor_patient["demographic data"]["identities"][0]["details"]["items"][0]["value"]["value"])
        patient_surname=decrypt_data(cursor_patient["demographic data"]["identities"][0]["details"]["items"][1]["value"]["value"])
        gender=decrypt_data(cursor_patient["demographic data"]["details"]["items"][3]["value"]["value"])
        symbol="Mrs"
        if gender=="MALE":
            symbol="Mr"

        st.success(f": Hello {symbol} {patient_name} {patient_surname}!", icon="➡️")

        st.session_state.uuid=patient_uuid

        storage_dates_med_hist, hba1c_results_dict, bmi_values_dict = query_analyses(patient_uuid)
        
        st.write(storage_dates_med_hist)
        test_results_time_series(hba1c_results_dict,"HbA1c")
        test_results_time_series(bmi_values_dict,"BMI")
        
        medication_list=query_treatment(patient_uuid)
        medications_list_table(medication_list, storage_dates_med_hist)
        st.warning(": CLick on the button below to move to clinical interface" ,icon="⚠️")
        col1, col2, col3 = st.columns([4,2,3])
        with col2:    
            move_to_clinical = st.button("Move to Clinical Interface",on_click=callback)

    #-----------------------------------------------------------------------------------    
    else:
        st.error(": There is no patient with the following demographic data", icon="😕")
#--------------------------------------------------------------------------------------------