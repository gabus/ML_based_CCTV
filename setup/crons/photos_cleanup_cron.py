import os
import datetime
import shutil
from loguru import logger
from src.settings import STORAGE_RETENTION_DAYS, PHOTOS_STORAGE_LOCATION


now = datetime.datetime.now()
retention_days = datetime.timedelta(days=STORAGE_RETENTION_DAYS)

logger.info({
    "today": now,
    "retention_days": retention_days
})

# Little cheat. Delete week's data before retention day. In case camera was offline for more than a day
for i in range(7):
    ii = datetime.timedelta(days=i)
    day_to_delete = (now - retention_days - ii).strftime("%Y-%m-%d")
    folder_to_delete = os.path.join(PHOTOS_STORAGE_LOCATION, day_to_delete)

    logger.info("Folder to delete: {}".format(folder_to_delete))

    if os.path.isdir(folder_to_delete):
        shutil.rmtree(folder_to_delete)
        continue

logger.success("Folders have been deleted")
