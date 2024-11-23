"""
# First app using st.write()
# run the app with streamlit run ./streamlit/app2.py
Second attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

st.write("Second attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))