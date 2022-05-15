from decouple import config

FROM_EMAIL = config('FROM_EMAIL', cast=str)
FROM_EMAIL_PASSWORD = config('FROM_EMAIL_PASSWORD', cast=str)
TO_EMAIL = config('TO_EMAIL', cast=str)

STORAGE_RETENTION_DAYS = config('STORAGE_RETENTION_DAYS', cast=int)

CONTINUOUS_RECORDING_TIMER = config('CONTINUOUS_RECORDING_TIMER', cast=int)

PERSON_SCORE_THRESHOLD = config('PERSON_SCORE_THRESHOLD', cast=float)

IDLE_LOOP_SLEEP = config('IDLE_LOOP_SLEEP', cast=float)

CAMERA_RESET_TIMER = config('CAMERA_RESET_TIMER', cast=float)

PERSON_DETECTION_COOLDOWN_TIME = config('PERSON_DETECTION_COOLDOWN_TIME', cast=float)

CONTINUOUS_RECORDING_LOOP_SLEEP = config('CONTINUOUS_RECORDING_LOOP_SLEEP', cast=float)

PHOTOS_STORAGE_LOCATION = config('PHOTOS_STORAGE_LOCATION', cast=str)
