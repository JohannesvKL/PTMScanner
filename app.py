import streamlit as st
from captcha.image import ImageCaptcha
from src.common import *
from streamlit.web import cli
from pathlib import Path
import sys

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

# Check if the script is run in local mode (e.g., "streamlit run app.py local")
if "local" in sys.argv:
    # In local mode, run the main function without applying captcha
    main()

# If not in local mode, assume it's hosted/online mode
else:
    length_captcha = 5
    width = 400
    height = 180

    # define the function for the captcha control
    def captcha_control():
        #control if the captcha is correct
        if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
            st.title("Make sure you are not a robot🤖")
            
            # define the session state for control if the captcha is correct
            st.session_state['controllo'] = False
            
            # define the session state for the captcha text because it doesn't change during refreshes 
            if 'Captcha' not in st.session_state:
                    st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))
            
            #setup the captcha widget
            image = ImageCaptcha(width=width, height=height)
            data = image.generate(st.session_state['Captcha'])
            st.image(data)
            col1, col2 = st.columns([20, 80])
            capta2_text = col1.text_input('Enter captcha text')
            
            v_space(1, col2)
            if col2.button("Verify the code", type="primary"):
                capta2_text = capta2_text.replace(" ", "")
                # if the captcha is correct, the controllo session state is set to True
                if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                    del st.session_state['Captcha']
                    col1.empty()
                    st.session_state['controllo'] = True
                    st.rerun() 
                else:
                    # if the captcha is wrong, the controllo session state is set to False and the captcha is regenerated
                    st.error("🚨 Captch is wrong")
                    del st.session_state['Captcha']
                    del st.session_state['controllo']
                    st.rerun()
            else:
                #wait for the button click
                st.stop()
        
    # WORK LIKE MULTIPAGE APP
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        # hide app pages as long as captcha not solved
        delete_all_pages("app")

        # Apply captcha control to verify the user
        captcha_control()

    else:     
        # Run the main function
        main()

        # Restore all pages (assuming "app" is the main page)
        restore_all_pages("app")
        

