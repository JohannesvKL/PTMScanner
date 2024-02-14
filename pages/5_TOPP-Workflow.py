import streamlit as st
from src.common import page_setup
from src.Workflow import Workflow

# The rest of the page can, but does not have to be changed
if __name__ == "__main__":
    
    params = page_setup()

    wf = Workflow()

    st.title(wf.name)

    t = st.tabs(["📁 **File Upload**", "⚙️ **Configure**", "🚀 **Run**", "📊 **Results**"])
    with t[0]:
        wf.ui.show_file_upload_section()

    with t[1]:
        wf.ui.show_parameter_section()

    with t[2]:
        wf.ui.show_execution_section()
        
    with t[3]:
        wf.ui.show_results_section()

