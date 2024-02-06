from src.TOPPWorkflow import TOPPWorkflow
from src.common import page_setup

# This page does not need to be changed

params = page_setup()

wf = TOPPWorkflow()

wf.show_file_upload_section()
