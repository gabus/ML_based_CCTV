echo '================ installing requirements ================'
sh get_pi_requirements.sh

echo '================ copying env file ================'
cp .env.example .env

echo '================ copying supervisor conf to /etc/supervisor/conf.d/cctv.conf ================'
sudo cp setup/supervisor_motion_eye.conf /etc/supervisor/conf.d/cctv.conf

echo '================ copying crontab to /var/spool/cron/crontabs/cctv_crontab ================'
sudo cp setup/crontab /var/spool/cron/crontabs/cctv_crontab

echo '================ injecting paths into supervisor and cron configs ================'
cleanup_cron_dir=$PWD"/photos_cleanup_cron.py"
sed -i "s/{photos_cleanup_dir_file}/$cleanup_cron_dir/" /var/spool/cron/crontabs/cctv_crontab
sed -i "s/{project_root}/$PWD/" /etc/supervisor/conf.d/cctv.conf


#  original cron
#   */30 * * * * python3 /home/pi/tflite/crons/photos_cleanup_cron.py >> /var/log/motioneye-cctv-cron.log 2>&1


#[program:motioneye-cctv]
#command=venv/bin/python src/TFLite_detection_webcam.py --modeldir=coco-model --resolution=1600x1200 --framerate=30
#user=pi
#autostart=true
#autorestart=true
#directory=/home/pi/tflite
#stdout_logfile=/var/log/motioneye-cctv.log
#redirect_stderr=true
#environment=PYTHONPATH=/home/pi/.local/lib/python3.7/site-packages
