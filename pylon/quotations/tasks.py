from config import celery_app

from celery import Celery, shared_task
from celery.schedules import crontab

from pylon.users.models import User

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("AUAUA")
    # x = User.objects.first()
    sender.add_periodic_task(4.0, test.s("lol"), expires=2)
    # sender.add_periodic_task(3, test.s("ASD"), expires=3)
    # sender.add_periodic_task(3, test.s(x.email), expires=3)

# @celery_app.on_after_configure.connect
# def setup_periodic_tasks2(sender, **kwargs):
#     sender.add_periodic_task(3, test.s("xxx"), expires=3)

# @celery_app.task()
# def test(arg):
#     print(arg)

@shared_task
def test(arg):
    x = User.objects.first()
    print("noice", arg, x.email)