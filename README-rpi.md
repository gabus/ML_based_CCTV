## How to make it work: Linux (raspberry pi)

### Build python dependencies
```commandline
python3 -m venv venv
source venv/bin/activate
pip install pipenv
pipenv install
```

### Enable camera in rpi settings
```commandline
sudo raspi-config
sudo reboot now
```

### Execute setup script
```commandline
sh ./setup/setup_script.sh
```

### update .env credentials file