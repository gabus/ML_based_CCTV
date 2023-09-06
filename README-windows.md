## How to make it work: Windows
https://www.python.org/downloads/release/python-3810/
```windows (2022.04.14: tflite-runtime has compiled version only for python 3.8 on windows)
py -3.8 -m venv venv
.\venv\scripts\activate
pip install pipenv
pipenv install
```

## Project setup
Variables that need to be set: FROM_EMAIL TO_EMAIL FROM_EMAIL_PASSWORD PHOTOS_STORAGE_LOCATION. Everything else can be default
```bash
cp .env.example .env
```

### To run scripts manually instead of supervisor use
```commandline
pi src/TFLite_detection_webcam.py --modeldir=coco-model --resolution=1600x1200 --framerate=30
```

## Troubleshooting

```commandline
On windows '.\venv\scripts\activate' throws UnauthorizedAccess
Run PowerShell in Admin mode:
Set-ExecutionPolicy RemoteSigned
or
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
