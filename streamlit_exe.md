# create .exe of streamlit app
Tested with streamlit v1.25, python v3.11.4</br>
## virtual environment 

``` 
# create an environment
python -m venv <myenv>

# activate an environment
.\myenv\Scripts\Activate.bat 

# deactivate an environment
.\myenv\Scripts\deactivate.bat 

# install libraries (you will use)
pip install streamlit pyinstaller
```

## streamlit files

create an app.py file as example and add content.<br />
some example file is here<br />
```
import streamlit as st
from streamlit.web import cli

if __name__ == "__main__":
    st.header("Hello World")
```

create a run_app.py and add this lines of codes<br />
```
from streamlit.web import cli

if __name__=='__main__':
    cli._main_run_clExplicit('app.py', 'streamlit run')
    # we will create this function inside our streamlit framework

```

## write function in cli.py

Now, navigate to the inside streamlit environment <br />
here you go<br />
```
<myenv>\Lib\site-packages\streamlit\web\cli.py
```
for using our virtual environment, add this magic function to cli.py file: <br />
```
#can be modify name as given in run_app.py
#use underscore at beginning 
def _main_run_clExplicit(file, command_line, args=[], flag_options=[]):
    main._is_running_with_streamlit = True
    bootstrap.run(file, command_line, args, flag_options)
```

## Hook folder
Now, need to hook to get streamlit metadata<br />
organized as folder, where the pycache infos will save<br />
like: \hooks\hook-streamlit.py<br />

```
from PyInstaller.utils.hooks import copy_metadata
datas = []
datas += copy_metadata('streamlit')
datas += copy_metadata('streamlit_plotly_events')
datas += copy_metadata('pyopenms')  
```

## compile the app 
Now, ready for compilation
```
pyinstaller --onefile --additional-hooks-dir ./hooks run_app.py --clean

#--onefile create join binary file ??
#will create run_app.spec file
#--clean delete cache and removed temporary files before building
#--additional-hooks-dir path to search for hook 
```

## stream config
To access  streamlit config create file in root <br />
(or just can be in output folder)<br />
.streamlit\config.toml<br />

```
# content of .streamlit\config.toml
[global]
developmentMode = false

[server]
port = 8502
``` 

## copy necessary files to output folder
copy .streamlit folder into dist (output) folder<br />
copy app.py (main streamlit files) into dist (output) folder<br />

## add datas in run_app.spec (.spec file)
Add DATAS to the new hook we created<br />
```
datas=[
        ("myenv/Lib/site-packages/altair/vegalite/v4/schema/vega-lite-schema.json","./altair/vegalite/v4/schema/"),
        ("myenv/Lib/site-packages/streamlit/static", "./streamlit/static"),
        ("myenv/Lib/site-packages/streamlit/runtime", "./streamlit/runtime"),
        ("myenv/Lib/site-packages/streamlit_plotly_events", "./streamlit_plotly_events/"),
        ("myenv/Lib/site-packages/pyopenms", "./pyopenms/"),
    ]
```    
## run final step to make executable
All the modifications in datas should be loaded with <br />
```
pyinstaller run_app.spec --clean
```

*if problem with altair <br />
use this version pip install altair==4.0.1 , and again compile
