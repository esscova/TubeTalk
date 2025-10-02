import streamlit as st
from UI import UI

if __name__ == "__main__":
    st.set_page_config(page_title="TubeTalk", page_icon=":robot_face:", layout="centered")
    ui = UI()
    ui.run()