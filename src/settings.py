from decouple import config

FROM_EMAIL = config('FROM_EMAIL', default='', cast=str)
FROM_EMAIL_PASSWORD = config('FROM_EMAIL_PASSWORD', default='', cast=str)
TO_EMAIL = config('TO_EMAIL', default='', cast=str)
PHOTOS_LOCATION = config('PHOTOS_LOCATION', default='', cast=str)
