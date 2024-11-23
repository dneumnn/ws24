"""
# First app using magic commands
# st.write() is called with msome magic!
# run the app with streamlit run ./streamlit/app1.py
First attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df