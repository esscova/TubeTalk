import streamlit as st
from UI.index import UI
from configs.streamlit_config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)

if __name__ == "__main__":
    ui = UI()
    ui.run()