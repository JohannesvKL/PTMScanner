import streamlit as st
from captcha.image import ImageCaptcha
from src.common import *
from streamlit.web import cli
from pathlib import Path
from src.captcha_ import *

params = page_setup(page="main")

def main():
    st.title("Template App")
    st.markdown("## A template for an OpenMS streamlit app.")
    if Path("OpenMS-App.zip").exists():
        st.markdown("## Installation")
        with open("OpenMS-App.zip", "rb") as file:
            st.download_button(
                    label="Download for Windows",
                    data=file,
                    file_name="OpenMS-App.zip",
                    mime="archive/zip",
                )
    save_params(params)

## In local mode no captcha 
if "local" in sys.argv:
    main()

##if docker or online mode
else: 

    # WORK LIKE MULTIPAGE APP         
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        #delete pages
        delete_page("app", "File_Upload")
        delete_page("app", "View_Raw_Data")
        delete_page("app", "Workflow")
        #apply captcha
        captcha_control()
    else:
        #run main
        main()
        #add all pages back
        add_page("app", "File_Upload")
        add_page("app", "View_Raw_Data")
        add_page("app", "Workflow")

