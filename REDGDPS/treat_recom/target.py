import streamlit as st 

def target(previous_state,treatment_data):
    target_=7.0
    if (previous_state== "Already getting treatment"):
        if(len(treatment_data.keys())==1):
            elderly = st.selectbox(
                "Are you a young patient?",
                ('NO', 'YES'))
            recent_diabetes= st.selectbox(
                "Are you a recently diagnosed diabetic ?",
                ('NO', 'YES'))
            if(elderly=="YES" and recent_diabetes=="YES"):
                target_=6.5     

    return(target_)
