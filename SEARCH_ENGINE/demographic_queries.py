import streamlit as st
from paths import parameter_to_directory
import datetime

from encrypt import encrypt_data

values_strings_demographics=["Name","Surname","DNI","Gender","Country of birth","Province of birth","Town of birth","Street name","Postal Code","Country","Province","Town"]
values_dates_demographics=["Birth date",]

def demographic_queries_list(chosen_parameters_demog):
    query_demog_list=[]
    if len(chosen_parameters_demog)>0:
        for value in chosen_parameters_demog:
            st.header(value.upper()+":")
            query_demog={}

            #If the value is a string:
            if value in values_strings_demographics:
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
                    query_demog={parameter_to_directory(value): encrypt_data(input_value)}
                else:
                    query_demog={parameter_to_directory(value): {'$ne': encrypt_data(input_value) }}

            #If the value is a date:
            elif value in values_dates_demographics:
                col01,col02,col03 = st.columns([1.25,.25,2])
                with col01:
                    selected=st.selectbox(
                        "Condition for "+value+" :",
                        ("equal","not equal","greater","lower","greater or equal","lower or equal", "between")
                    )
                with col03:
                    if selected=="between":
                        lower_value = st.date_input(
                            "Lower value of "+value+":",
                            min_value=datetime.date(1923,1,1),
                            max_value=datetime.date.today()
                            )
                        
                        higher_value = st.date_input(
                            "Higher value of "+value+":",
                            min_value=lower_value,
                            max_value=datetime.date.today()
                            )
                    else:
                        input_value = st.date_input(
                        "Value of "+value+":",
                        min_value=datetime.date(1923,1,1),
                        max_value=datetime.date.today()
                        )

                if selected=="equal":
                    query_demog={parameter_to_directory(value): encrypt_data(str(input_value))}
                elif selected== "not equal":
                    query_demog={parameter_to_directory(value): {"$ne": encrypt_data(str(input_value))}}
                elif selected== "greater":
                    query_demog={parameter_to_directory(value): {"$gt": str(input_value)}}
                elif selected== "greater or equal":
                    query_demog={parameter_to_directory(value): {"$gte": str(input_value)}}
                elif selected== "lower":
                    query_demog={parameter_to_directory(value): {"$lt": str(input_value)}}
                elif selected== "lower or equal":
                    query_demog={parameter_to_directory(value): {"$lte": str(input_value)}}
                elif selected=="between":
                    query_demog={"$and":[{parameter_to_directory(value): {"$gte": str(lower_value)}},
                                {parameter_to_directory(value): {"$lte": str(higher_value)}}
                                ]
                        }
                    
            #Here we gonna add the specific query related to this chosen condition to the list of queries           
            query_demog_list.append(query_demog)
    
    return(query_demog_list)