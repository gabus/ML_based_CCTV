echo 'copying env file'
cp ../.env.example ../.env

echo 'copying supervisor conf to /etc/supervisor/conf.d/cctv.conf'
sudo cp supervosor_motion_eye.conf /etc/supervisor/conf.d/cctv.conf

echo 'copying crontab to /var/spool/cron/crontabs/cctv.conf'
sudo cp crontab /var/spool/cron/crontabs/cctv.conf
