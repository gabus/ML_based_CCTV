### What's this?
Neural network based object recognition CCTV which sends email once there's a person.

Thanks to 
* https://github.com/HackerShackOfficial/Smart-Security-Camera
* https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi

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


## How to make it work: Windows
https://www.python.org/downloads/release/python-3810/
```windows (2022.04.14: tflite-runtime has compiled version only for python 3.8 on windows)
py -3.8 -m venv venv
.\venv\scripts\activate
pip install pipenv
pipenv install
```

## Project setup: all platforms
```commandline
cp .env.example .env
```


### supervisor config /etc/supervisor/conf.d/cctv.conf
```/etc/supervisor/conf.d/cctv.conf
[program:motioneye-cctv]
command=python3 -u TFLite_detection_webcam.py --modeldir=coco-model --resolution=1600x1200 --framerate=30
user=pi
directory=/home/pi/tflite
stdout_logfile=/var/log/motioneye-cctv.log
redirect_stderr=true
environment=PYTHONPATH=/home/pi/.local/lib/python3.7/site-packages
```

### add cron to crontab -e
```commandline
*/30 * * * * python3 /home/pi/tflite/crons/photos_cleanup_cron.py >> /var/log/motioneye-cctv-cron.log 2>&1
*/31 * * * * sh /home/pi/tflite/crons/restart_app.sh >> /var/log/motioneye-cctv-cron.log 2>&1
```

### to run scripts manually instead of supervisor use
```commandline
python3 TFLite_detection_webcam.py --modeldir=coco-model --resolution=1600x1200 --framerate=30
```

### Debugging
```commandline
sudo supervisorctl status
sudo supervisorctl restart all
tail -fn 100 /var/log/motioneye-cctv.log
```

## What's missing?
* downscale emailing photos - currently it's ~3MB (1600x1200 px)
* there's rare random issue when image quality becomes really poor. Requires power disconnection
* could be faster

### Troubleshooting
```commandline
On windows '.\venv\scripts\activate' throws UnauthorizedAccess
Run PowerShell in Admin mode:
Set-ExecutionPolicy RemoteSigned
```


### todo 
* move all file in src
* throttle down if no human detected
* fetch camera from only when requested from main thread
* optimize mail manager (reduce file size without reducing quality? is there a better way to display images in gmail?)
* some files use camel-case variable naming. Change to match snake-style
* write setup.sh script which make raspberry py ready to go (venv, pip install, apt-get requirements, set .env)
* fix any problems in "Code -> Inspect Code"

[] which file to send via email? even though camera might continue recording 5s after last human detection, should it be sent to gmail?
[] 

