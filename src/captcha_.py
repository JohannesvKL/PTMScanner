from pathlib import Path
import streamlit as st
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)
from captcha.image import ImageCaptcha
import random, string

def delete_page(main_script_path_str, page_name):
    """
    delete page from app

    Args:
        main_script_path_str: main page (e-g app)
        page_name: Page want to delete (e-g Analyze)

    Returns:
        None
    """
    #get all pages
    current_pages = get_pages(main_script_path_str)

    #iterate over all pages and del if desire page found
    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass

    #refresh the pages config
    _on_pages_changed.send()
    
def add_page(main_script_path_str, page_name):
    """
    add page in app

    Args:
        main_script_path_str: main page (e-g app)
        page_name: Page want to delete (e-g Analyze)

    Returns:
        None
    """
    #get all pages    
    pages = get_pages(main_script_path_str)
    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "pages"
    script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)

    psh = calc_md5(script_path_str)

    #add new page config
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }

    #refresh the page config
    _on_pages_changed.send()


length_captcha = 5
width = 400
height = 180

# define the function for the captcha control
def captcha_control():
    #control if the captcha is correct
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        st.title("Makesure you are not a robot🤖")
        
        # define the session state for control if the captcha is correct
        st.session_state['controllo'] = False
        col1, col2 = st.columns(2)
        
        # define the session state for the captcha text because it doesn't change during refreshes 
        if 'Captcha' not in st.session_state:
                st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))
        
        #setup the captcha widget
        image = ImageCaptcha(width=width, height=height)
        data = image.generate(st.session_state['Captcha'])
        col1.image(data)
        capta2_text = col2.text_area('Enter captcha text', height=20)
        
        
        if st.button("Verify the code"):
            capta2_text = capta2_text.replace(" ", "")
            # if the captcha is correct, the controllo session state is set to True
            if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                del st.session_state['Captcha']
                col1.empty()
                col2.empty()
                st.session_state['controllo'] = True
                st.experimental_rerun() 
            else:
                # if the captcha is wrong, the controllo session state is set to False and the captcha is regenerated
                st.error("🚨 Captch is wrong")
                del st.session_state['Captcha']
                del st.session_state['controllo']
                st.experimental_rerun()
        else:
            #wait for the button click
            st.stop()
