import streamlit as st
import datetime
import json

def demographic_data():
    st.write("#")

    st.markdown("<h1 style='color: #0B5345;'>Identity:</h1>", unsafe_allow_html = True)
    

    col_1,col_2,col_3=st.columns([2,0.5,2])
    with col_1:
        #Getting patient's name:
        st.subheader("Name:")
        name=st.text_input("enter your name:",label_visibility ="collapsed")
        if (len(name)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        st.write("#")

        #Getting patient's DNI:
        st.subheader("DNI:")
        dni=st.text_input("enter your national identifier:",label_visibility ="collapsed")
        if (len(dni)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        elif (correct_dni(dni) is False):
            st.error(": DNI must be composed of 8 numbers and a capital letter at the end" ,icon="❌")
        st.write("#")
    
    with col_3:
        #Getting patient's name:
        st.subheader("Surname:")
        surname=st.text_input("",label_visibility ="collapsed")
        if (len(surname)==0):
            st.warning(": You entered nothing !" ,icon="⚠️") 
        st.write("#") 
        
        #Getting patient's gender:
        st.subheader("Gender:")
        gender = st.radio("", ('MALE', 'FEMALE'))
        st.write("#")
#----------------------------------------------------------------------------------------------------
    st.markdown("<h1 style='color: #0B5345;'>Birth data:</h1>", unsafe_allow_html = True)
    st.write("#")
    
    col_1,col_2,col_3=st.columns([2,0.5,2])
    with col_1:
        
        #Getting patient's birth day:
        st.subheader("Birth date:")
        birthday = st.date_input(
            "",
            min_value=datetime.date(1923,1,1),
            max_value=datetime.date.today(),
            label_visibility ="collapsed"
            )
        st.write('Your birth date is on:',birthday)

        #Getting Province:
        st.subheader("Province of birth:")
        province_birth=st.text_input("State/territory/province:")
        if (len(province_birth)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")  
    
    with col_3:
        #Getting Country of birth:
        st.subheader("Country of birth:")
        country_of_birth=st.text_input(":",label_visibility ="collapsed")
        if (len(country_of_birth)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        else:
            st.write("#")
            st.write("#")

        #Getting Town:
        st.subheader("Town of birth:")
        town_birth=st.text_input("City/town/locality:")
        if (len(town_birth)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        
#------------------------------------------------------------------------------------------------------
    st.markdown("<h1 style='color: #0B5345;'>Address:</h1>", unsafe_allow_html = True)
    st.write("#")

    col_1,col_2,col_3,col_4,col_5=st.columns([2,0.1,2,0.1,2])
    with col_1:
        #Getting Street name:
        st.subheader("Street name:")
        street_name=st.text_input(":sde",label_visibility ="collapsed")
        if (len(street_name)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        st.write("#")

        #Getting Country :
        st.subheader("Country:")
        country=st.text_input("Current_country Identifier",label_visibility ="hidden")
        if (len(country)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")

    with col_3:
        #Getting Street number:
        st.subheader("Street N°:")
        street_number=st.number_input(":h",min_value=0,step=1,label_visibility ="collapsed")
        if (street_number==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        st.write("#")

        #Getting Province:
        st.subheader("Province:")
        province=st.text_input("Current State/territory/province:")
        if (len(province)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        st.write("#")

    with col_5:
        #Getting patient's postal_code:
        st.subheader("Postal Code:")
        postal_code=st.text_input("enter your postal code:",label_visibility ="collapsed")
        correct_postal_code=True
        if (len(postal_code)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
            correct_postal_code=False
        elif (postal_code.isnumeric() is False or len(postal_code)!=5):
            st.error("Postal code must be composed of 5 numbers" ,icon="❌")
            correct_postal_code=False
        st.write("#")

        #Getting Town:
        st.subheader("Town:")
        town=st.text_input("Current Suburb/town/locality:")
        if (len(town)==0):
            st.warning(": You entered nothing !" ,icon="⚠️")
        st.write("#")
    return(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,correct_postal_code,country,province,town)
    
#This function adds the submitted demographic_data to the demographics json file 
def add_demographic_data(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town):
    from encrypt import encrypt_data
    #'patient.v0_20230713112750_000001_1.json': This is a json file containing standard demographic data in the OpenEHR standards form
    full_path_demographic_data = 'patient.v0_20230713112750_000001_1.json'
    #Demographic data file:
    with open(full_path_demographic_data, 'r') as openfile:
        # Reading from json file
        json_object_demographic_data = json.load(openfile)
    #Birth data:
    json_object_demographic_data["details"]["items"][0]["items"][0]["value"]["value"]=encrypt_data(str(birthday))
    json_object_demographic_data["details"]["items"][0]["items"][1]["value"]["value"]=encrypt_data(country_of_birth.upper())
    json_object_demographic_data["details"]["items"][0]["items"][2]["value"]["value"]=encrypt_data(province_birth.upper())
    json_object_demographic_data["details"]["items"][0]["items"][3]["value"]["value"]=encrypt_data(town_birth.upper())
    json_object_demographic_data["details"]["items"][0]["items"][4]["value"]["value"]=encrypt_data(gender.upper())
    json_object_demographic_data["details"]["items"][0]["items"][5]["value"]["value"]=encrypt_data(dni.upper())

    #Other data:
    json_object_demographic_data["details"]["items"][3]["value"]["value"]=encrypt_data(gender.upper())

    #Address:
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][0]["items"][0]["value"]["value"]=encrypt_data(street_name.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][0]["items"][1]["value"]["value"]=encrypt_data(str(street_number).upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][1]["value"]["value"]=encrypt_data(postal_code.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][2]["value"]["value"]=encrypt_data(town.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][3]["value"]["value"]=encrypt_data(province.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][4]["value"]["value"]=encrypt_data(country.upper())

    #Identity:
    json_object_demographic_data["identities"][0]["details"]["items"][0]["value"]["value"]=encrypt_data(name.upper())
    json_object_demographic_data["identities"][0]["details"]["items"][1]["value"]["value"]=encrypt_data(surname.upper())

    return(json_object_demographic_data)

#This function checks if the user submitted a right DNI or not
def correct_dni(dni):
    try:
        value=int(dni[:8])
    except:
        return(False)
    if(len(dni)==9 and dni[len(dni)-1].isupper() ):
        return(True)
    else :
        return(False)
    
#This function calculates the age of a person based on his Birthdate
def calculate_age(birthdate):
    # Assuming birthdate is in the format 'YYYY-MM-DD'
    birthdate_obj = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
    current_date = datetime.datetime.now()
    
    # Calculate age
    age = current_date.year - birthdate_obj.year - ((current_date.month, current_date.day) < (birthdate_obj.month, birthdate_obj.day))
    
    return age