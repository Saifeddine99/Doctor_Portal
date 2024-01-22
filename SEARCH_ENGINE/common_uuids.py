def extract_common_elements(array1, array2, array3):
    set1 = set(array1)
    set2 = set(array2)
    set3 = set(array3)

    # Find common elements using set intersection
    common_elements = list(set1.intersection(set2, set3))
    
    return common_elements

def create_csv_and_display(data_dict):
    import pandas as pd
    import streamlit as st

    df = pd.DataFrame(data_dict)
    st.dataframe(df)
    return df