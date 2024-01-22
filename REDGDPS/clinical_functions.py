import streamlit as st

medium_dose="medium dose"
full_dose= "full dose"
#----------------------------------------------------------------------------------------------

# Let's ask about the clinical condition :
def additional_clinical_cond():
    st.sidebar.title("Clinical condition:")
    
    # frailty:
    frailty = st.sidebar.selectbox(
        "Frailty:",
        ('NO', 'YES'))
    
    # Heart Failure:
    heart_failure = st.sidebar.selectbox(
        "Heart Failure:",
        ('NO', 'YES'))
    
    # Established CVD:
    established_CVD = st.sidebar.selectbox(
        "Established CVD:",
        ('NO', 'YES'))
    
    #Hepatic Steatosis:
    hepatic_steatosis = st.sidebar.selectbox(
        "Hepatic Steatosis:",
        ('NO', 'YES'))
    
    #Strokes:
    strokes = st.sidebar.selectbox(
        "Strokes:",
        ('NO', 'YES'))
    
    return(frailty,heart_failure,established_CVD,hepatic_steatosis,strokes)

#------------------------------------------------------------------------------------------------------------------------
def current_hba1c():
    st.subheader("HbA1c(%):")
    current_HbA1c=st.number_input("current HbA1c value:",min_value=0.00,step=0.01)
    if (current_HbA1c==0):
        st.warning(": You entered nothing!" ,icon="⚠️")
    st.write("#")
    return(current_HbA1c)
#----------------------------------------------------------------------------------------------------
def symptomatic():
    st.subheader("Symptoms :")
    symptoms = st.selectbox(
                "Are you symptomatic now?",
                ('NO', 'YES'))
    if(symptoms=='YES'):
        st.write('You selected: Symptomatic')
    else:
        st.write('You selected: Asymptomatic')    
    return(symptoms)
#---------------------------------------------------------------------------------------------------------------
def other_analyses_records():
    col001, col002, col003 = st.columns([2,0.25,2])
    with col001:
        #Getting eGFR value:
        st.subheader("eGFR(ml/min):")
        current_eGFR=st.number_input("enter your current eGFR: estimated glomerular filtration rate (ml/min):",min_value=0.00,step=0.01)
        if (current_eGFR==0):
            st.warning(": You entered nothing!" ,icon="⚠️")
    with col003:
        #Getting UACR value:
        st.subheader("UACR(mg/g):")
        current_UACR=st.number_input("enter your current UACR: urine albumin/creatinine ratio (mg/g):",min_value=0.00,step=0.01)
        if (current_UACR==0):
            st.warning(": You entered nothing!" ,icon="⚠️")

    #Getting the Height and weight of the patient
    col0001, col0002, col0003 = st.columns([1,0.25,1])
    with col0001:
        #Getting Height value:
        st.subheader("Height(cm):")
        height=st.number_input("enter your current Height in 'cm':",min_value=0.00,step=0.01)
        if (height==0):
            st.warning(": You entered nothing!" ,icon="⚠️")
    with col0003:
        #Getting Height value:
        st.subheader("Weight(Kg):")
        weight=st.number_input("enter your current Weight in 'Kg':",min_value=0.00,step=0.01)
        if (weight==0):
            st.warning(": You entered nothing!" ,icon="⚠️")

    #Getting BMI value:
    current_BMI=0
    if (height>0 and weight>0):
        st.subheader("BMI(Kg/m²):")
        height_m=height/100
        current_BMI=round(weight/(height_m*height_m), 2)
        sentence="Body Mass Index= "+str(current_BMI)
        st.info(sentence)
    # I will add a separation line here
    st.markdown("""---""")

    return(current_BMI,height,weight,current_eGFR,current_UACR)
#-----------------------------------------------------------------------------------------
def get_CVRFs(current_BMI, current_eGFR,current_UACR):
    st.subheader("Cardiovascular risk factors:")
    CVRFs = st.multiselect(
                    'Select your cardiovascular risk factors:',
                    ['High_blood_pressure','hypercholesterolemia','smoking','albuminuria','family history of early CVD'])
    
    if (isinstance(current_BMI, float)):
        if (current_BMI>=30):
            CVRFs.append('Obesity')

    if (isinstance(current_eGFR, float)):
        if (current_eGFR<60):
            CVRFs.append('eGFR <60 ml/min')

    if (isinstance(current_UACR, float)):
        if (current_UACR>30):
            CVRFs.append('UACR > 30 mg/g')

    if(len(CVRFs)==0):
        st.subheader('You selected nothing!')
    else:
        st.subheader('Here are your cardiovascular risk factors:')
        st.write(CVRFs)

    return(CVRFs)
