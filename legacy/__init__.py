from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

import legacy.display_main
import legacy.display_church
import legacy.display_settings
