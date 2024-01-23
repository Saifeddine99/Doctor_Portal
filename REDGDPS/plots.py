import plotly.graph_objects as go
from datetime import datetime
import streamlit as st

def test_results_time_series(test_results_dict, y_axis_name):
        
    if len(test_results_dict):
        dates= list(test_results_dict.keys())
        test_results= list(test_results_dict.values())

        # Convert dates to datetime objects
        date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

        # Create a Plotly figure
        fig = go.Figure()

        # Add a scatter plot for the time series
        fig.add_trace(go.Scatter(x=date_objects, y=test_results, mode='lines+markers', name= y_axis_name))

        # Update layout for better readability
        plot_title= y_axis_name + ' Time Series'
        fig.update_layout(title= plot_title,
                        xaxis_title='Date', 
                        yaxis_title= y_axis_name,
                        hovermode='x unified')

        # Show the plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"You don't have any value of {y_axis_name} stored in database")


def check_if_any_dict_not_empty(dictionary_list):
    for d in dictionary_list:
        if bool(d):
            return "not empty"
    return "empty"

def medications_list_table(list1, list2):
    if check_if_any_dict_not_empty(list1)=="not empty":
        # Create an empty list to store table rows
        table_rows = []

        # Define a gradient of blue colors progressing from sky blue to navy blue based on the number of rows
        sky_blue = [173, 216, 230]  # Sky blue color
        navy_blue = [0, 0, 128]      # Navy blue color

        def interpolate_color(i, total):
            r = int(sky_blue[0] + (navy_blue[0] - sky_blue[0]) * i / total)
            g = int(sky_blue[1] + (navy_blue[1] - sky_blue[1]) * i / total)
            b = int(sky_blue[2] + (navy_blue[2] - sky_blue[2]) * i / total)
            return f'rgba({r},{g},{b},0.7)'

        # Create an empty list to store color values for each row
        row_colors = []

        # Iterate through list1 and list2 simultaneously
        for i, (date, med_dict) in enumerate(zip(list2, list1)):
            # Check if the dictionary has more than one key-value pair
            if len(med_dict) > 1:
                # Add multiple rows for each key-value pair with the same date-specific color
                for key, value in med_dict.items():
                    row_cells = [date, key, value]
                    table_rows.append(row_cells)
                    row_colors.append(interpolate_color(i, len(list2)))
            else:
                # Add a row for the original dictionary with date-specific color
                key, value = list(med_dict.items())[0]
                row_cells = [date, key, value]
                table_rows.append(row_cells)
                row_colors.append(interpolate_color(i, len(list2)))

        # Define column names
        column_names = ["Date", "Medication", "Dose"]

        # Create a Plotly table with a row color gradient of blue colors
        fig = go.Figure(data=[go.Table(header=dict(values=column_names, fill_color='rgba(0, 100, 0, 0.7)', font=dict(color='black', size=14)),
                                    cells=dict(values=list(map(list, zip(*table_rows))),
                                                fill_color=[row_colors]))])

        # Update layout for better readability
        fig.update_layout(title='Medications List Table')
        # Show the plot
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.error("You don't have any recommended treatment stored in database")

if __name__=='__main__':
    # Example usage
    list1 = [
        {"METFORMIN": "MEDIUM DOSE"},
        {"METFORMIN": "FULL DOSE"},
        {"METFORMIN": "FULL DOSE", "SU": "MEDIUM DOSE", "PIO": "FULL DOSE"},
        {"METFORMIN": "FULL DOSE", "GLP1Ra": "MEDIUM DOSE"}
    ]
    list2 = ["2024-01-12", "2024-01-12", "2024-01-18", "2024-01-30"]

    medications_list_table(list1, list2)