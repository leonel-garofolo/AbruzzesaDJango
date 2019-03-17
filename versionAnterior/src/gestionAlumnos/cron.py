from django_cron import cronScheduler, Job
import kronos

@kronos.register('0 * * * *')
def task():#inicializo las tareas registradas en el sistema
    print("ejecuto task")
    pass