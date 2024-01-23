import plotly.express as px

import streamlit as st
import pandas as pd

import pymongo as py

from encrypt import encrypt_data
from decrypt import decrypt_data

import matplotlib.pyplot as plt
import numpy as np

myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]


from paths import parameter_to_directory

def gender_distribution(gender_list):
    # Create a DataFrame from the list
    df = pd.DataFrame({"gender": gender_list})
    # Create the pie chart
    fig_gender = px.pie(df, names=df.columns[0], hole=0.3, title="Gender Distribution:")
    # Display the chart using Streamlit
    st.plotly_chart(fig_gender, use_container_width=True)


def total_number(medical_disease):
    total_number_of_patient=0
    key="problem list"
    query_med_data={key:{"$elemMatch":{
                            parameter_to_directory("Clinical desease"): encrypt_data(medical_disease.upper())}
                        }}
    
    cursor=medical_data_coll.find(query_med_data)
    for item in cursor:
        total_number_of_patient+=1
    
    return(total_number_of_patient)

def obesity_total():
    total_number_obesity=0

    query = medical_hist_coll.find()
    for doc in query:
        try:
            value_path=doc["analytics"][1]["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]
            decrypted_value= float(decrypt_data(value_path))
            
            if decrypted_value>=30:
                total_number_obesity+=1

        except:
            pass

    return total_number_obesity

def plot_horizontal_bar(disease_names, patient_counts):
    # Check if the lengths of both lists are the same
    if len(disease_names) != len(patient_counts):
        raise ValueError("The lengths of the two lists must be the same.")

    # Create a Pandas DataFrame from the lists
    df = pd.DataFrame({'Disease': disease_names, 'Patients': patient_counts})

    # Create a horizontal bar plot using Plotly Express with unique colors
    fig = px.bar(df, x='Patients', y='Disease', orientation='h', text='Patients',
                 labels={'Patients': 'Number of Patients'},
                 title='Disease Distribution',
                 color=df['Disease'])  # Assign a unique color to each bar based on the disease name

    # Display the plot using Streamlit
    st.plotly_chart(fig, use_container_width=True)

def hba1c_distribution():
    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): encrypt_data("hba1c".upper())}
                    }}
    
    query = medical_hist_coll.find(query_med_hist)

    hba1c_values_list=[]
    uuids_list=[]
    
    for doc in query:
        for index, iter1 in enumerate(doc["analytics"][0]):
            if iter1["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]== encrypt_data("hba1c".upper()):
                encrypted_value = iter1["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]
                decrypted_value= float(decrypt_data(encrypted_value))
                if decrypted_value>9:
                    uuids_list.append(doc["uuid"])
                break

        hba1c_values_list.append(decrypted_value)
    
    # Define intervals
    bins = [float('-inf'), 6.49, 7, 8, 9, float('inf')]
    labels = ['<6.5', '6.5-6.99', '7-7.99', '8-8.99', '>=9']
    # Convert float values to categorical intervals
    interval_labels = pd.cut(hba1c_values_list, bins=bins, labels=labels)
    # Create a DataFrame to count the occurrences of each interval
    interval_counts = pd.value_counts(interval_labels, sort=False).reset_index()
    interval_counts.columns = ['HbA1c', 'Count']

    custom_colors = ['#2ca02c', '#1f77b4', '#9467bd', '#ff7f0e', '#d62728']
    fig = px.bar(interval_counts, x='HbA1c', y='Count',title="HbA1c Stats:", color='HbA1c', color_discrete_sequence=custom_colors)
    st.plotly_chart(fig, use_container_width=True)
    
    return uuids_list

def all_symptomatics():
    query_med_data={parameter_to_directory("Symptoms"): encrypt_data("YES") }

    query = medical_data_coll.find(query_med_data)

    symptomatics_uuids=[]

    for doc in query:
        symptomatics_uuids.append(doc["uuid"])

    return symptomatics_uuids

def display_patient_info(hba1c_gt_9_uuids, symptomatic_uuids):
    # Create a DataFrame with patient UUIDs
    all_uuids = set(hba1c_gt_9_uuids + symptomatic_uuids)
    df = pd.DataFrame({'UUID': list(all_uuids)})

    # Add a column indicating the situation
    df['Situation'] = 'None'

    # Update the 'Situation' column based on conditions
    df.loc[df['UUID'].isin(hba1c_gt_9_uuids), 'Situation'] = 'HbA1c > 9'
    df.loc[df['UUID'].isin(symptomatic_uuids), 'Situation'] = 'Symptomatic'
    df.loc[df['UUID'].isin(hba1c_gt_9_uuids) & df['UUID'].isin(symptomatic_uuids), 'Situation'] = 'HbA1c > 9 & Symptomatic'

    # Display the table using Streamlit
    st.info(f"The total number of Symptomatic patients or suffering from HbA1c>9 is: {len(df)}")
    st.dataframe(df[['UUID', 'Situation']])