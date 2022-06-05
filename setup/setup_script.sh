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
sudo sed -i "s@{photos_cleanup_dir_file}@$cleanup_cron_dir@" /var/spool/cron/crontabs/cctv_crontab
sudo sed -i "s@{project_root}@$PWD@g" /etc/supervisor/conf.d/cctv.conf

sudo supervisorctl restart all
