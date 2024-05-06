## create windows executable of streamlit app with embeddable python

### Download suitable python Embeddable Version e-g 3.11.9

```
wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip

# Unzip the folder
unzip python-3.11.9-embed-amd64.zip
```

### Download get-pip.py and install pip
```
wget https://bootstrap.pypa.io/get-pip.py

# Install pip
./python-3.11.9-embed-amd64/python <path_to_get-pip.py> --no-warn-script-location
```

### Uncomment 'import site' in the python-3.11.9-embed-amd64/python311._pth
```
# Uncomment to run site.main() automatically
# Remove hash
import site 
# Or use command
sed -i 's/^# import site/import site/' python-3.11.9-embed-amd64/python311._pth
```

### Install all packages from requirements.txt
```
./python-3.11.9-embed-amd64/python -m pip install -r requirements.txt --no-warn-script-location
```

### Run streamlit app
```
./python-3.11.9-embed-amd64/python -m streamlit run app.py
```

### Wrap a command in .bat file to achieve clickable event
```
# create run_app.bat file

@echo off
.\python-3.11.9-embed-amd64\python -m streamlit run app.py local
```

#### <code> After successfully completing all these steps, the streamlit app will be available by running run_app.bat file.</code>

> [!NOTE]
you can still change the configuration of streamlit app with .streamlit/config.toml file e-g provide different port, change upload size etc

