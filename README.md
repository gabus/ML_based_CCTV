### What's this?
Neural network based object recognition CCTV which sends email once there's a person.

Thanks to 
* https://github.com/HackerShackOfficial/Smart-Security-Camera
* https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi

## How to make it work? 

```commandline
sudo apt-get update
```

```commandline
sudo apt-get install supervisor
```

```commandline
sudo apt-get install python3-pip
```

### enable camera in settings
```commandline
sudo raspi-config
sudo reboot now
```

### install all other crap
```commandline
sh ./get_pi_requirements.sh
```

### modify credentials in mail_manager.py
```python
fromEmail = 'your_mama@gmail.com'
fromEmailPassword = 'your_momma_is_so_ugly_she_made_One_Direction_go_another_direction'
toEmail = '50_cent@gmail.com'
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