from time import sleep

from loguru import logger

from celery import shared_task


@shared_task
def send_sms_msg(phone, msg):
    """
    使用celery发送短信

    模拟接口调用

    :param phone:
    :param msg:
    :return:
    """
    sleep(1)
    logger.info(f"send sms to {phone} with msg {msg}")  # 模拟发送短信

    return True
