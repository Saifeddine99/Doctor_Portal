import streamlit as st 
import pandas as pd

from REDGDPS.treat_recom.no_clinical_conditions.normal_case import normal_case
from REDGDPS.treat_recom.clinical_condition import clinical_priorities,ckd_ob_cvr
from REDGDPS.treat_recom.one_clinical_disease.obesity_case import obese
from REDGDPS.treat_recom.one_clinical_disease.elderly_frailty_case import elderly_frailty
from REDGDPS.treat_recom.one_clinical_disease.heart_failure_case import heart_failure_
from REDGDPS.treat_recom.one_clinical_disease.established_cvd_case import established_cvd
from REDGDPS.treat_recom.one_clinical_disease.chronic_kidney_disease import non_critical_chronic_kidney_disease_,critical_chronic_kidney_disease_

def main_get_treat(frailty,heart_failure,established_CVD,hepatic_steatosis,strokes,symptoms,current_UACR,current_eGFR,current_BMI,current_drugs,hba1c_records,CVRFs,previous_state):
    
    st.markdown("<h1 style='text-align: center; color: #0d325c;'>Treatment Recommendation</h1>", unsafe_allow_html = True)
    st.write('#')
    st.write('#')

    chronic_kidney_disease,obesity,High_CVR=ckd_ob_cvr(current_eGFR,current_UACR,current_BMI,CVRFs)

    #----------------------------------------------------------------------------------------------------------------------
    columns_=["obesity","frailty","chronic_kidney_disease","heart_failure","established_CVD","CVRFs","High_CVR","hepatic_steatosis","strokes","symptoms","current_UACR","current_eGFR","current_BMI","hba1c_records","current_drugs"]
    values_=[obesity,frailty,chronic_kidney_disease,heart_failure,established_CVD,CVRFs,High_CVR,hepatic_steatosis,strokes,symptoms,current_UACR,current_eGFR,current_BMI,hba1c_records,current_drugs]
    types=[]
    for item in values_:
        types.append(type(item))
    #here we create a dataframe to show all new medical data  
    data={"Value":values_,"Type":types}
    st.subheader("Below is patient's data:")
    df = pd.DataFrame(data,index=columns_)    
    st.dataframe(df,use_container_width=True)
    #----------------------------------------------------------------------------------------------------------------------

    # Let's ask about the clinical condition :
    # condition is variable containing patient's most prioritary disease in addition to diabetes 
    #visit the "clinical_priorities" function to understand more
    condition=clinical_priorities(obesity,frailty,chronic_kidney_disease,heart_failure,established_CVD,High_CVR,current_eGFR,current_UACR)
    st.write(condition)
    #----------------------------------------------------------------------------------------------------------------
    #Here we display in interface the most prioritary clinical condition:
    if(condition[0]=='No other clinical conditions'):
        st.title("Fortunately,You are not suffering from any other clinical disease in addition to diabetes !")
    elif(condition[0]=='established_cvd_or_high_cvr'):
        st.title('In your case the treatment priority goes for: "{}"'.format(condition[1]))
    else:
        st.title('In your case the treatment priority goes for: "{}"'.format(condition[0]))
    #--------------------------------------------------------------------------------------------------------------------------------------

    if(condition[0]=="No other clinical conditions"):
        proposed_med,next_date=normal_case(previous_state,hba1c_records,symptoms,current_drugs)
    elif(condition[0]=="obesity"):
        proposed_med,next_date=obese(hba1c_records,previous_state,current_BMI,current_drugs)
    elif(condition[0]=="frailty"):
        proposed_med,next_date=elderly_frailty(hba1c_records,previous_state,current_drugs)   
    elif(condition[0]=="heart_failure"):
        proposed_med,next_date=heart_failure_(hba1c_records,previous_state,current_drugs)   
    elif(condition[0]=="established_cvd_or_high_cvr"):
        proposed_med,next_date=established_cvd(hba1c_records,previous_state,current_drugs)  
    elif(condition[0]=="critical_chronic_kidney_disease"):
        proposed_med,next_date=critical_chronic_kidney_disease_(hba1c_records,previous_state,current_drugs) #Not_righttttt
    elif(condition[0]=="non_critical_chronic_kidney_disease"):
        proposed_med,next_date=non_critical_chronic_kidney_disease_(hba1c_records,previous_state,current_eGFR,current_UACR,current_drugs) #Not_righttttt
        
    return(proposed_med,next_date) 