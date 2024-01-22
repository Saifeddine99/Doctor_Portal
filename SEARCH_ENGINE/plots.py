import streamlit as st
import pandas as pd
import plotly.express as px

def plotting(df):
    left_plots,middle,right_plots=st.columns([2,0.2,4])

    with left_plots:
        fig_gender = px.pie(df, names=df.columns[0], hole=0.3, title= "Gender Distribution:")
        st.plotly_chart(fig_gender, use_container_width=True)

        # Create a pie chart
        fig_vital_status = px.pie(df, names=df.columns[2], hole=0.3, title= "Vital Status Distribution:")
        # Display the chart
        st.plotly_chart(fig_vital_status, use_container_width=True)

    with right_plots:
        selected_hba1c_rows = df.loc[df['HbA1c'] != "UNKNOWN" , 'HbA1c'].tolist()
        # Define intervals
        bins = [float('-inf'), 6.49, 7, 8, 9, float('inf')]
        labels = ['<6.5', '6.5-6.99', '7-7.99', '8-8.99', '>=9']
        # Convert float values to categorical intervals
        interval_labels = pd.cut(selected_hba1c_rows, bins=bins, labels=labels)
        # Create a DataFrame to count the occurrences of each interval
        interval_counts = pd.value_counts(interval_labels, sort=False).reset_index()
        interval_counts.columns = ['HbA1c', 'Count']

        custom_colors = ['#2ca02c', '#1f77b4', '#9467bd', '#ff7f0e', '#d62728']
        fig = px.bar(interval_counts, x='HbA1c', y='Count',title="HbA1c Stats:", color='HbA1c', color_discrete_sequence=custom_colors)
        st.plotly_chart(fig, use_container_width=True)
        #----------------------------------------------------------------------------------
        spec_df=df.loc[df['HbA1c'] != "UNKNOWN" , ['HbA1c','Age']]
        bins = [0, 40, 50, 65, 80, float('inf')]
        labels = ['<40', '40-50', '50-65', '65-80', '>=80']

        # Categorize ages into intervals
        spec_df['AgeGroup'] = pd.cut(spec_df['Age'], bins=bins, labels=labels, right=False)

        # Create a box plot using Plotly Express
        fig = px.box(spec_df, x='AgeGroup', y='HbA1c', title="HbA1c Distribution by Age Interval:",
                    labels={'AgeGroup': 'Age Interval', 'HbA1c': 'HbA1c'})

        # Customize layout if needed
        fig.update_layout(xaxis_title="Age Interval", yaxis_title="HbA1c")

        # Display the chart
        st.plotly_chart(fig)