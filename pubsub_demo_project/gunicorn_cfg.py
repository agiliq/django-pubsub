import os, getpass

curr_dir = os.path.dirname(os.path.abspath(__file__))
bind = "127.0.0.1:8000"
workers = 2
max_requests = 200
debug = True
daemon = True
pidfile = os.path.join(curr_dir, "pid/gunicorn.pid")
user = getpass.getuser()
group = user
logfile = os.path.join(curr_dir, "logs/chat.log")
