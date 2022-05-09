## How to make it work: Linux (raspberry pi)
```commandline
python3 -m venv venv
source venv/bin/activate
pip install pipenv
pipenv install
```


### install all other crap
```commandline
sh ./get_pi_requirements.sh
```


### enable camera in settings
```commandline
sudo raspi-config
sudo reboot now
```



### execute setup script
```commandline
sh ./setup/setup_script.sh
```

### update .env credentials file