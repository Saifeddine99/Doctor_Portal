import streamlit as st
from paths import parameter_to_directory

from encrypt import encrypt_data

clinical_data_list=["Clinical desease","cardiovascular risk factors"]
vital_status_symptoms=["Vital status","Symptoms"]

def med_data_queries_list(chosen_parameters_med_data):
    #query_med_data_list is a list of all demographic queries
    query_med_data_list=[]

    if len(chosen_parameters_med_data)>0:
        for value in chosen_parameters_med_data:
            if value == "Age":
                 pass
            
            else:
                st.header(value.upper()+":")
                query_med_data={}

                #If the value is a string:
                if value in clinical_data_list:
                    col01,col02,col03 = st.columns([1.25,.25,2])
                    with col01:
                        selected=st.selectbox(
                            "Condition for "+value+" :",
                            ("equal","different")
                        )
                    with col03:
                        input_value= st.text_input("Value of " + value + ":")
                        input_value=input_value.upper()

                    key="problem list"
                    if value=="cardiovascular risk factors":
                        key="risk factors"

                    if selected=="equal":
                        query_med_data={key:{"$elemMatch":{
                            parameter_to_directory(value): encrypt_data(input_value)}
                        }}

                    else:
                        query_med_data={"$or":[{key+"."+parameter_to_directory(value):{
                            "$ne": encrypt_data(input_value)}
                        },
                        {key: []}]
                        }

                #If the value is a string:
                elif value in vital_status_symptoms :
                    
                    col01,col02,col03 = st.columns([1.25,.25,2])
                    with col01:
                        selected=st.selectbox(
                            "Condition for "+value+" :",
                            ("equal","different")
                        )
                    with col03:
                        input_value=(st.text_input("Value of " + value + ":"))
                        input_value=input_value.upper()
                        
                    if selected=="equal":
                        query_med_data={parameter_to_directory(value): encrypt_data(input_value) }
                    else:
                        query_med_data={parameter_to_directory(value): {'$ne': encrypt_data(input_value)}}
                        
                #Here we gonna add the specific query related to this chosen condition to the list of queries           
                query_med_data_list.append(query_med_data)
    
    return(query_med_data_list)