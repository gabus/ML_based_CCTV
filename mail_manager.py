import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from settings import FROM_EMAIL, FROM_EMAIL_PASSWORD, TO_EMAIL


def sendEmail(frame_names):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Security Update'
    msgRoot['From'] = FROM_EMAIL
    msgRoot['To'] = TO_EMAIL
    msgRoot.preamble = 'Raspberry pi security camera update'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('Smart security cam found object')
    msgAlternative.attach(msgText)

    msgText = MIMEText('<img src="cid:image1">', 'html')
    msgAlternative.attach(msgText)

    for frame_name in frame_names:
        image_content = open(frame_name, 'rb').read()
        msgImage = MIMEImage(image_content)
        msgImage.add_header('Content-ID', '<image1>')
        msgImage.add_header('Content-Disposition', 'attachment', filename=frame_name)
        msgRoot.attach(msgImage)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
    smtp.sendmail(FROM_EMAIL, TO_EMAIL, msgRoot.as_string())
    smtp.quit()
