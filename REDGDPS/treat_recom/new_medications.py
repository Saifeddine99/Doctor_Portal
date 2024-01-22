import streamlit as st
import pandas as pd

def new_med(proposed_med, next_date, therapeutic_precautions):
    # I will add a separation line here
    st.markdown("""---""")

    #Here we show the proposed medications:
    st.subheader("Below is your recommended treatment:")
    df = pd.DataFrame(list(proposed_med.items()),columns = ['recommended_Drug','recommended_Dose'])
    st.dataframe(df,use_container_width=True)

    #therapeutic_precautions always shown:
    st.subheader("Always keep aware of these points:")
    for index,precaution in enumerate(therapeutic_precautions):
        st.write(f"{index}: {precaution}")

    # I will add a separation line here
    st.markdown("""---""")

    #Reminder for user to Check every 3-6 months
    st.subheader("Next check:")
    st.text(next_date)

    st.write("#")