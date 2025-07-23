import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.fetchings import *

clone_datas()
get_operator()
get_theme()
