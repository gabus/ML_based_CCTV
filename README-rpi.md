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

## Troubleshooting

read comments at src/video_stream.py:14
```commandline
cv2.error: OpenCV(4.5.5) /tmp/pip-wheel-efxaz4j7/opencv-python_bedc0fac27944da0921e079da44d32bf/opencv/modules/imgproc/src/color.cpp:182: error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'
```

```text
pipenv is piece of shit. If you're getting any problems installing dependencies, just install them globally using pip
```