from decouple import config

FROM_EMAIL = config('FROM_EMAIL', default='', cast=str)
FROM_EMAIL_PASSWORD = config('FROM_EMAIL_PASSWORD', default='', cast=str)
TO_EMAIL = config('TO_EMAIL', default='', cast=str)

STORAGE_RETENTION_DAYS = config('STORAGE_RETENTION_DAYS', default=1, cast=int)

CONTINUOUS_RECORDING_TIMER = config('CONTINUOUS_RECORDING_TIMER', default=3, cast=int)

PERSON_SCORE_THRESHOLD = config('PERSON_SCORE_THRESHOLD', default=0.6, cast=float)
