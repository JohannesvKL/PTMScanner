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

def delete_all_pages(main_script_path_str: str) -> None:
    """
    Delete all pages except the main page from an app's configuration.

    Args:
        main_script_path_str (str): The name of the main page, typically the app's name.

    Returns:
        None

    """
    # Get all pages from the app's configuration
    current_pages = get_pages(main_script_path_str)
    
    # Create a list to store keys pages to delete
    keys_to_delete = []

    # Iterate over all pages and add keys to delete list if the desired page is found
    for key, value in current_pages.items():
        if value['page_name'] != main_script_path_str:
            keys_to_delete.append(key)

    # Delete the keys from current pages
    for key in keys_to_delete:
        del current_pages[key]

    # Refresh the pages configuration
    _on_pages_changed.send()

def delete_page(main_script_path_str: str, page_name: str) -> None:
    """
    Delete a specific page from an app's configuration.

    Args:
        main_script_path_str (str): The name of the main page, typically the app's name.
        page_name (str): The name of the page to be deleted.

    Returns:
        None
    """
    # Get all pages
    current_pages= get_pages(main_script_path_str)

    # Iterate over all pages and delete the desired page if found
    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]

    # Refresh the pages configuration
    _on_pages_changed.send()


def restore_all_pages(main_script_path_str: str) -> None:
    """
    restore all pages found in the "pages" directory to an app's configuration.

    Args:
        main_script_path_str (str): The name of the main page, typically the app's name.

    Returns:
        None
    """
    # Get all pages
    pages = get_pages(main_script_path_str)

    # Obtain the path to the main script
    main_script_path = Path(main_script_path_str)

    # Define the directory where pages are stored
    pages_dir = main_script_path.parent / "pages"

    # Iterate over all .py files in the "pages" directory
    for script_path in pages_dir.glob("*.py"):
        script_path_str = str(script_path.resolve())

        # Calculate the MD5 hash of the script path
        psh = calc_md5(script_path_str)

        # Obtain the page icon and name
        pi, pn = page_icon_and_name(script_path)

        # Add the new page configuration
        pages[psh] = {
            "page_script_hash": psh,
            "page_name": pn,
            "icon": pi,
            "script_path": script_path_str,
        }

    # Refresh the page configuration
    _on_pages_changed.send()


def add_page(main_script_path_str: str, page_name: str) -> None:
    """
    Add a new page to an app's configuration.

    Args:
        main_script_path_str (str): The name of the main page, typically the app's name.
        page_name (str): The name of the page to be added.

    Returns:
        None
    """
    # Get all pages
    pages = get_pages(main_script_path_str)

    # Obtain the path to the main script
    main_script_path = Path(main_script_path_str)

    # Define the directory where pages are stored
    pages_dir = main_script_path.parent / "pages"

    # Find the script path corresponding to the new page
    script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())

    # Calculate the MD5 hash of the script path
    psh = calc_md5(script_path_str)

    # Obtain the page icon and name
    pi, pn = page_icon_and_name(script_path)

    # Add the new page configuration
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }

    # Refresh the page configuration
    _on_pages_changed.send()


length_captcha = 5
width = 400
height = 180

# define the function for the captcha control
def captcha_control() -> None:
    """
    Captcha control function to verify if the user is not a robot.

    This function displays a captcha image and allows the user to enter the captcha text.
    It verifies whether the entered captcha text matches the generated captcha.

    Returns:
        None
    """
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
   