import streamlit as st
import pandas as pd
import base64
from rapidfuzz import process, fuzz

# Load metadata
metadata = pd.read_csv('data/metadata.csv')

st.title("PDF Finder")

# User input fields
id_input = st.text_input("Enter ID (optional)")
name_input = st.text_input("Enter Name")

# Initialize selected_name variable
selected_name = None

# Fuzzy match name in real-time and filter dropdown options
if name_input:
    names = metadata['name'].unique()
    matched_names = process.extract(name_input, names, scorer=fuzz.partial_ratio, limit=5)  # Limit to top 5 matches
    filtered_names = [match[0] for match in matched_names if match[1] > 60]  # Filter with a threshold score

    if filtered_names:
        selected_name = st.selectbox("Select Name", filtered_names)
    else:
        st.write("No names match your input.")
else:
    st.write("Please enter a name to search.")

# Filter metadata based on ID or selected fuzzy-matched name
filtered_metadata = metadata.copy()

if id_input:
    filtered_metadata = filtered_metadata[filtered_metadata['id'] == int(id_input)]
elif selected_name:
    filtered_metadata = filtered_metadata[filtered_metadata['name'] == selected_name]

# Show available dates as dropdown
if not filtered_metadata.empty:
    available_dates = filtered_metadata['date'].unique()
    selected_date = st.selectbox("Select Date", available_dates)

    # Filter based on the selected date
    filtered_metadata = filtered_metadata[filtered_metadata['date'] == selected_date]
    
    if not filtered_metadata.empty:
        # Display matched PDF
        pdf_path = filtered_metadata['pdf_path'].values[0]
        st.write(f"Displaying PDF for: {filtered_metadata['name'].values[0]}")
        st.write(f"PDF Path: {pdf_path}")

        # Display PDF using iframe
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.write("No match found for the selected date.")
else:
    if not id_input and not selected_name:
        st.write("Please enter an ID or name to begin.")
    else:
        st.write("No match found for the provided ID or Name.")
