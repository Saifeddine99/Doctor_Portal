import streamlit as st
import pymongo as py
import datetime
import uuid

import re
import ast

from REDGDPS.demographics import demographic_data,correct_dni,add_demographic_data
from encrypt import encrypt_data
from decrypt import decrypt_data

myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#----------------------------------------------------------------------------
# This function turns the "clinical_interface" state_session to True (Take a look on st.state_session if you are not familiar with it)
def callback():
    #Button was clicked!
    st.session_state.clinical_interface= True
    st.session_state.add_new_patient=False

def callback_false():
    st.session_state.clinical_interface= False

def callback_new_patient():
    st.session_state.add_new_patient=True

def callback_no_new_patient():
    st.session_state.add_new_patient=False

def main_redgdps_function():

    #----------------------------------------------------------------------------
    if "clinical_interface" not in st.session_state:
        st.session_state.clinical_interface=False

    if "uuid" not in st.session_state:
        st.session_state.uuid=""

    if "add_new_patient" not in st.session_state:
        st.session_state.add_new_patient=False
    #----------------------------------------------------------------------------
    m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: rgb(204, 225, 229);
        }
        </style>""", unsafe_allow_html=True)

    #----------------------------------------------------------------------------
    if st.session_state.clinical_interface == False:

        if st.session_state.add_new_patient==False:

            #--------------------------------------------------------------------------------------------------
            st.sidebar.info(': Click on the "Add a New Patient" button below, to add a new patient',icon="⛔")
            st.sidebar.button("Add a New Patient", on_click= callback_new_patient)
            #--------------------------------------------------------------------------------------------------

            from REDGDPS.occurrence import get_top_patients_uuids, identify_patient
            from REDGDPS.patient_finder import patient_data,query_patient
            from REDGDPS.query_clinical_data import plots_displaying


            patients_list = ["None"]
            top_patient_uuids = get_top_patients_uuids()
            patients_list.extend(identify_patient(top_patient_uuids))

            selected_patient=st.selectbox("You can choose your patient from here:", patients_list, index=0)
            
            if selected_patient==None or selected_patient=="None":

                name, gender, phone_number = patient_data()

                if len(phone_number)==0 or len(name)==0:
                    st.error(": You must enter the Name and the Phone Number of the patient!", icon="🚨")
                else:
                    query_condition = query_patient(name, phone_number, gender)
                    plots_displaying(query_condition)
            #----------------------------------------------------------------------------------------------
            #here we work on the case of choosing a patient from the suggested list:
            else:
                patient_uuid=top_patient_uuids[patients_list.index(selected_patient)-1]
                query_condition={"uuid": patient_uuid}
                plots_displaying(query_condition)

        #--------------------------------------------------------------------------------------------------
        #Here we'll be working on the creation of a new patient:
        else:

            st.sidebar.info(': To cancel the addition of a new patient click on the "Cancel" button below',icon="⛔")
            col21, col22, col23 = st.sidebar.columns([1,2,1])
            with col22:
                no_new_patient = st.sidebar.button("Cancel", on_click= callback_no_new_patient)

            st.info("Welcome! please fill carefully the demographic form below")

            st.markdown("<h1 style='color: #0B5345;'>Phone Number:</h1>", unsafe_allow_html = True)
            phone_number=st.text_input("enter your phone number:",label_visibility ="collapsed")
            if len(phone_number)==0:
                st.warning(": You entered nothing !" ,icon="⚠️")

            name,surname,dni,status,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,correct_postal_code,country,province,town=demographic_data()
            if( len(phone_number)>0 and len(name)>0 and len(surname)>0 and correct_dni(dni) and len(province_birth)>0 and len(country_of_birth)>0 and len(town_birth)>0 and len(street_name)>0 and street_number>0 and correct_postal_code and len(country)>0 and len(province)>0 and len(town)>0):                
                #demographic data:
                json_object_demographic_data=add_demographic_data(name,surname,dni,status,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town)
                
                st.write("#")
                col1, col2, col3 = st.columns([4,2,3])
                with col2:    
                    save_demographics = st.button("Done")
                
                if save_demographics:
                    st.session_state.uuid=str(uuid.uuid4())

                    demographic_doc={
                    "uuid": st.session_state.uuid,
                    "phone number": encrypt_data(phone_number),
                    "current date": encrypt_data(str(datetime.date.today())),
                    "demographic data": json_object_demographic_data
                    }
                    demographic_data_coll.insert_one(demographic_doc)
                    st.success(f"Patient's data added to database, uuid={st.session_state.uuid}",icon="✅")

                    st.warning("CLick on the button below to move to clinical interface" ,icon="⚠️")
                    col1, col2, col3 = st.columns([4,2,3])
                    with col2:
                        move_to_clinical = st.button("Move to Clinical Interface",on_click=callback)

                    st.title("Actual OpenEHR (.json) demographic register:")
                    st.json(json_object_demographic_data)
                    
    #--------------------------------------------------------------------------------------------------
    else:
        #--------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------
        # Here we'll check the existance of this UID in the clinical data db:
        # "Previous state" is an imporant variable that allows us to know the number of previous uses:

        st.sidebar.button("Back to Demographic Interface",on_click=callback_false)
        occurence=medical_data_coll.count_documents({"uuid":st.session_state.uuid})
        if occurence==0:
            previous_state="First time"
        elif occurence==1:
            previous_state="Second time"
        else:
            previous_state="Two previous times or more"
        #---------------------------------------------------------------------------------------------
        st.info(f"Your total number of clinical documents found in database is: {occurence}")
        #--------------------------------------------------------------------------------------------
        from REDGDPS.clinical_data_form import clinical_data_
        current_HbA1c,symptoms,current_BMI,height,weight,current_eGFR,current_UACR,CVRFs,frailty,heart_failure,established_CVD,hepatic_steatosis,strokes=clinical_data_()
        #--------------------------------------------------------------------------------------------
        #Here we'll extract the user's current drugs from database + his previous HbA1c records:
        #These 3 big if conditions need decryption !!!!

        current_drugs={}
        if previous_state!="First time":
            try:
                extracted_medication_list = medical_data_coll.find_one(
                {'uuid': st.session_state.uuid},
                sort=[( '_id', py.DESCENDING )]
                )["medication list"]
            except:
                extracted_medication_list = []

            for drug_json_file in extracted_medication_list:
                drug=decrypt_data(drug_json_file["content"][0]["items"][0]["description"]["items"][0]["value"]["value"])
                dose=decrypt_data(drug_json_file["content"][0]["items"][0]["description"]["items"][2]["items"][3]["value"]["value"])
                current_drugs[drug]=dose
        
            #------------------------------------------------------------------------------------------------------
            # Here we'll add a selection box allowing user to choose the actual chosen treatment from the proposed list:
            list_current_drugs = list(current_drugs)
            for recommendation in list_current_drugs:
                item_list = []
                if "YOU CAN CHOOSE ANY ITEM FROM THIS LIST" in recommendation:
                    match = re.search(r'\[(.*?)\]', recommendation)
                    if match:
                        # Extract the matched string
                        list_str = match.group(0)
                        # Safely evaluate the string to a list
                        item_list = ast.literal_eval(list_str)
                
                elif " OR " in recommendation:
                    item_list = recommendation.split(' OR ')

                if item_list:
                    selected_drug = st.selectbox("Select the chosen drug from the previous proposed list:", item_list)

                    # Update the key
                    current_drugs[selected_drug] = current_drugs.pop(recommendation)

                    st.write("Current drugs: ", current_drugs)


        #---------------------------------------------------------------------------------------------------------------
        #Here we'll extract the user's previous HbA1c records from database:
        hba1c_records=[current_HbA1c]
        if previous_state=="Second time":
            extracted_hba1c_records_list = medical_hist_coll.find_one(
            {'uuid': st.session_state.uuid},)["analytics"][0][0]
            previous_hba1c=float(decrypt_data(extracted_hba1c_records_list["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]))
            hba1c_records=[current_HbA1c,previous_hba1c]

        if previous_state=="Two previous times or more":
            cursor = medical_hist_coll.find({'uuid': st.session_state.uuid}).sort("_id", py.DESCENDING).limit(2)
            hba1c_list=[]
            # Iterate through the results
            for document in cursor:
                hba1c_list.append(document)
            
            previous_hba1c=float(decrypt_data(hba1c_list[0]["analytics"][0][0]["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]))
            before_previous_hba1c=float(decrypt_data(hba1c_list[1]["analytics"][0][0]["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]))
            hba1c_records=[current_HbA1c, previous_hba1c, before_previous_hba1c]

        #--------------------------------------------------------------------------------------------
        st.markdown("""---""")
        st.write("#")
        #Here we'll test if form is filled correctly or not:    
        if (current_HbA1c>0) and (current_eGFR>0) and (current_UACR>0) and (current_BMI>0):

            from REDGDPS.treat_recom.main_treat_recom import main_get_treat
            from REDGDPS.treat_recom.new_medications import new_med
            #This function determines the new recommended treatment + next checking date
            proposed_med,next_date=main_get_treat(frailty,heart_failure,established_CVD,hepatic_steatosis,strokes,symptoms,current_UACR,current_eGFR,current_BMI,current_drugs,hba1c_records,CVRFs,previous_state)
            
            #This function displays the new recommended treatment + next checking date
            therapeutic_precautions=["Nutrition","Physical activity","self-management education and support"]        
            new_med(proposed_med, next_date, therapeutic_precautions)

            col1, col2, col3 = st.columns([4,2,3])
            with col2:
                #This is a download button that allows to download the created new treatment file
                save_to_db_button = st.button('Save to database')

            if save_to_db_button:

                from REDGDPS.demographics import calculate_age
                birthdate=decrypt_data(demographic_data_coll.find_one({"uuid": st.session_state.uuid})["demographic data"]["details"]["items"][0]["items"][0]["value"]["value"])
                age=str(round(calculate_age(birthdate)))
                
                from REDGDPS.treat_recom.saving_todb_preprocessing import save_symptoms,save_laboratory_test_results,save_bmi,save_problem_list,save_risk_factors,save_medication_list,save_age_to_compo
                laboratory_test_results_list = save_laboratory_test_results(current_HbA1c,current_eGFR,current_UACR)
                json_object_bmi = save_bmi(current_BMI,height,weight)
                problem_list = save_problem_list(frailty,heart_failure,established_CVD,hepatic_steatosis,strokes)
                risk_factors = save_risk_factors(CVRFs)
                medication_list = save_medication_list(proposed_med)
                json_object_encounter_symptoms = save_symptoms(symptoms)
                age_json_compo = save_age_to_compo(age)

                current_date=str(datetime.date.today())

                medical_data_dict={
                    "uuid": st.session_state.uuid,
                    "check date": encrypt_data(current_date),
                    "problem list": problem_list,
                    "risk factors": risk_factors,
                    "medication list": medication_list,
                    "therapeutic precautions": [encrypt_data(precaution) for precaution in therapeutic_precautions],
                    "symptoms": json_object_encounter_symptoms,
                    "age": age_json_compo
                }

                medical_history_dict={
                    "uuid": st.session_state.uuid,
                    "check date": encrypt_data(current_date),
                    "analytics": [laboratory_test_results_list, json_object_bmi],
                }

                medical_data_coll.insert_one(medical_data_dict)
                medical_hist_coll.insert_one(medical_history_dict)

                st.write("#")
                st.success(f": File saved well, uuid={st.session_state.uuid}" ,icon="✅")
            
        else:
            st.error(
                ": One of the values you entered is invalid, Please check them carefully!",icon="⛔"
                )