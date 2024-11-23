# Understand session handling

import streamlit as st

##### simple counter
counter = 0
counter += 1
st.write(f"No Session State: {counter}")

##### session counter
if "counter" not in st.session_state:
    st.session_state.counter = 0


st.session_state.counter += 1

st.write(f"With Session State: {st.session_state.counter}")

st.button("Run it again")

