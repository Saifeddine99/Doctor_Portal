import streamlit as st
from encrypt import encrypt_data
from paths import parameter_to_directory


def patient_data():

    st.info(": Enter the Name and/or the Phone Number of the Patient you want to receive his data!", icon="⬇️")
    st.write("#")

    col_1,col_a,col_2,col_b,col_3=st.columns([3,0.5,3,0.5,2])
    with col_1:
        #Getting patient's name:
        st.subheader("Name:")
        name=st.text_input("enter your name:",label_visibility ="collapsed")
        if (len(name)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        st.write("#")

    with col_2:
        st.subheader("Phone Number:")
        phone_number=st.text_input("enter your phone number:",label_visibility ="collapsed")
        if len(phone_number)==0:
            st.warning(": You entered nothing !" ,icon="⚠️")
            st.write("#") 
        
    with col_3:
        #Getting patient's gender:
        st.subheader("Gender:")
        gender = st.radio("", ('MALE', 'FEMALE'))
        st.write("#")
    

    st.write("#")    

    return(name.upper(), gender.upper(), phone_number.upper())

#-----------------------------------------------------------------------
def query_patient(name, phone_number, gender):
    queries_list=[]
    if name!="":
        condition = {parameter_to_directory("Name"): encrypt_data(name)}
        queries_list.append(condition)

    if phone_number!="":
        condition = {'phone number': encrypt_data(phone_number)}
        queries_list.append(condition)

    condition = {parameter_to_directory("Gender"): encrypt_data(gender)}
    queries_list.append(condition)

    query_cond={"$and": queries_list}

    return query_cond