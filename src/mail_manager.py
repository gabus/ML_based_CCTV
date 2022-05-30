import os
import math
import smtplib
from enum import Enum
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from settings import FROM_EMAIL, FROM_EMAIL_PASSWORD, TO_EMAIL, EMAIL_ATTACHMENT_SIZE_LIMIT, EMAIL_SUBJECT


class AttachmentsSelectAlgorithm(Enum):
    all = 0
    first_to_limit = 1
    every_second_to_limit = 2
    even_spread_to_limit = 3


class Mailer:

    def __init__(self):
        pass

    def send_email(self, attachments: list, attachments_select_algorithm: AttachmentsSelectAlgorithm):
        logger.info("Sending email")

        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = EMAIL_SUBJECT
        msg_root['From'] = FROM_EMAIL
        msg_root['To'] = TO_EMAIL
        msg_root.preamble = 'Raspberry pi security camera update'

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)
        msg_alternative.attach(MIMEText('Smart security cam found object'))

        if attachments_select_algorithm == AttachmentsSelectAlgorithm.first_to_limit:
            attachments = self.__first_to_limit(attachments)
        elif attachments_select_algorithm == AttachmentsSelectAlgorithm.every_second_to_limit:
            attachments = self.__every_second_to_limit(attachments)
        elif attachments_select_algorithm == AttachmentsSelectAlgorithm.even_spread_to_limit:
            attachments = self.__even_spread_to_limit(attachments)

        for frame_name in attachments:
            image_content = open(frame_name, 'rb').read()
            msg_image = MIMEImage(image_content)
            msg_image.add_header('Content-ID', '<image1>')
            msg_image.add_header('Content-Disposition', 'attachment', filename=frame_name)
            msg_root.attach(msg_image)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, msg_root.as_string())
        smtp.quit()

    @staticmethod
    def __first_to_limit(attachments: list) -> list:
        """
        |||----------
        """
        return attachments

    @staticmethod
    def __every_second_to_limit(attachments: list) -> list:
        """
        |-|-|---------
        """
        return attachments

    @staticmethod
    def __even_spread_to_limit(attachments: list) -> list:
        """
        |---|---|-
        |-----|-----|-

        files count = 16
        files size = 1,164.492mb
        1.6 / 16 = 0.1mb approximate one file size
        25MB is limit
        how many files i'll be able to send? 0.3 / 0.1 = 3 floor 3
        i've got 16 files, which 3 to send?
        index 16 / 3 = 5.3333

        counter = 0
        floor(counter) = 0
        0 + 5.333 = 5.3333
        round(counter) = 5
        5 + 5.3333 = 10.3333
        round(counter) = 10
        10 + 5.3333 = 15.3333
        floor(counter) = 15
        """

        total_size = 0
        files_to_send = []
        attachment_size_limit = EMAIL_ATTACHMENT_SIZE_LIMIT * 1024 * 1024

        for attachment in attachments:
            fs = os.path.getsize(attachment)
            total_size = total_size + fs

        if total_size < attachment_size_limit:
            logger.info("All attachment files takes {}MB which is less space than {}MB. Sending all"
                        .format(round(total_size / 1024 / 1024, 2), attachment_size_limit / 1024 / 1024))
            return attachments  # all files takes less than the limit. Send all

        approximate_one_file_size = total_size / len(attachments)
        approximate_files_to_send = math.floor(attachment_size_limit / approximate_one_file_size)

        if approximate_files_to_send == 0:
            logger.warning("Attachment is too big. Can't send anything")
            return []  # files are too big

        approximate_index = len(attachments) / approximate_files_to_send
        index = 0

        logger.info({
            "all attachments": len(attachments),
            "how many file will be sent": approximate_files_to_send,
            "approximate_index": approximate_index,
            "total files size (mb)": round(total_size / 1024 / 1024, 2),
            "mailer attachments limit (mb)": round(attachment_size_limit / 1024 / 1024, 2)
        })

        for i in range(int(approximate_files_to_send)):
            # logger.debug("which photo is selected index: {}".format(index))
            fts = attachments[index]
            files_to_send.append(fts)
            index = index + int(round(approximate_index, 0))

        return files_to_send
