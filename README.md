### What's this?
Neural network based object recognition CCTV which sends email once person is detected

Thanks to 
* https://github.com/HackerShackOfficial/Smart-Security-Camera
* https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi

## How to make it work on unix machines
```commandline
python3 -m venv venv
source venv/bin/activate
pip install pipenv
pipenv install
```

## Project setup
Variables that need to be set: FROM_EMAIL TO_EMAIL FROM_EMAIL_PASSWORD PHOTOS_STORAGE_LOCATION. Everything else can be default
```bash
cp .env.example .env
```

### Run script locally
```commandline
python3 src/TFLite_detection_webcam.py --modeldir=coco-model --resolution=1600x1200 --framerate=30
```

## Troubleshooting

### Download photos from camera
```bash
scp -r pi@192.168.1.175:/home/pi/tflite/photos .
```

### Commands to check storage usage
```commandline
du -hs .
du -h .
df -h .
df -h
```

### Commands to debug supervisor
```commandline
sudo supervisorctl status
sudo supervisorctl restart all
tail -fn 100 /var/log/motioneye-cctv.log
```

## How it works
1. Every 1s the latest frame is requested from video_stream
2. Frame is analyzed via ML 
3. If human detected, for the next 5 seconds continue to request frames from video_stream and store them locally (without analyzing via ML)
4. After 5 seconds ask for new latest frame and analyze again
5. If no human detected, send email and return to 1, otherwise continue from step 3

+ gathers as many frames as camera capable to produce + writing locally
+ low cpu hit
- can't show on frame where object was detected
