gunicorn --bind 127.0.0.1:5000 bot:app --log-level debug --access-logfile my.log --daemon
