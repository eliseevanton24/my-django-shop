import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# Создаём экземпляр приложения Celery
app = Celery('myshop')

# Загружаем конфигурацию из Django settings, с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в файлах tasks.py всех приложений проекта
app.autodiscover_tasks()

# (Необязательно) Можно добавить функцию отладки
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')