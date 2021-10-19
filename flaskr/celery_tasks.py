def tasks_return(celery):
    @celery.task()
    def add_num(a, b):
        return a + b

    @celery.task()
    def send_mail():
        pass