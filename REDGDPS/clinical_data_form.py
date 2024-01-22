import streamlit as st

from REDGDPS.clinical_functions import additional_clinical_cond,current_hba1c,other_analyses_records,symptomatic,get_CVRFs

def clinical_data_():

    st.markdown("<h1 style='color: #0B5345;'>Clinical data:</h1>", unsafe_allow_html = True)
    st.write("#")
    cola1, cola2, cola3 = st.columns([2,.5,2])
    with cola1:
        #This function returns a the current of HbA1C record
        current_HbA1c=current_hba1c()
    with cola3:
        #This function returns information about current symptoms situation 
        symptoms=symptomatic()
    st.markdown("""---""")  
    current_BMI,height,weight,current_eGFR,current_UACR=other_analyses_records()
    #This function returns information about patient's cardiovascular risks
    CVRFs=get_CVRFs(current_BMI, current_eGFR,current_UACR)
    # Let's ask about the clinical condition :
    frailty,heart_failure,established_CVD,hepatic_steatosis,strokes=additional_clinical_cond()

    return(current_HbA1c,symptoms,current_BMI,height,weight,current_eGFR,current_UACR,CVRFs,frailty,heart_failure,established_CVD,hepatic_steatosis,strokes)