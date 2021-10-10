from celery import shared_task


@shared_task
def divide(x, y):
    # to perform rdb task debugging
    #from celery.contrib import rdb
    #rdb.set_trace()

    import time
    time.sleep(5)
    return x / y 
