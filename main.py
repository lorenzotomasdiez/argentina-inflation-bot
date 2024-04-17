import time
from backup import backup_prices
from scrapping import scrapping
from telegram import send_task_finished
from config import test_config


test_config()

time.sleep(10)

backup_prices()
scrapping()
send_task_finished()
#twittear
