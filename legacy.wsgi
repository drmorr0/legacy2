import sys
sys.path.insert(0, '/var/www/legacy2/')

activate_this = '/var/www/legacy2/venv/bin/activate_this.py'
with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))

from legacy import app as application
