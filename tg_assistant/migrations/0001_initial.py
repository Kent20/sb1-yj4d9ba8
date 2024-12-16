"""Initial migration for tg_assistant app"""
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TelegramConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(max_length=255, verbose_name='API ID')),
                ('api_hash', models.CharField(max_length=255, verbose_name='API Hash')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('session_name', models.CharField(max_length=255, verbose_name='Имя сессии')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активно')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Настройки Telegram',
                'verbose_name_plural': 'Настройки Telegram',
            },
        ),
        migrations.CreateModel(
            name='CapturedChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=255, unique=True, verbose_name='ID чата')),
                ('chat_title', models.CharField(max_length=255, verbose_name='Название чата')),
                ('chat_type', models.CharField(
                    choices=[
                        ('user', 'Личный чат'),
                        ('group', 'Группа'),
                        ('channel', 'Канал'),
                        ('unknown', 'Неизвестно')
                    ],
                    default='unknown',
                    max_length=20,
                    verbose_name='Тип чата'
                )),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('auto_reply', models.BooleanField(default=True, verbose_name='Автоответ')),
                ('unread_count', models.IntegerField(default=0, verbose_name='Непрочитанные')),
                ('last_message_text', models.TextField(blank=True, null=True, verbose_name='Последнее сообщение')),
                ('last_message_time', models.DateTimeField(null=True, blank=True, verbose_name='Время последнего сообщения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Захваченный чат',
                'verbose_name_plural': 'Захваченные чаты',
                'ordering': ['-last_message_time', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('sender', models.CharField(max_length=255, verbose_name='Отправитель')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время')),
                ('is_outgoing', models.BooleanField(default=False, verbose_name='Исходящее')),
                ('context', models.TextField(blank=True, verbose_name='Контекст')),
                ('chat', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='dialogues',
                    to='tg_assistant.capturedchat',
                    verbose_name='Чат'
                )),
            ],
            options={
                'verbose_name': 'Диалог',
                'verbose_name_plural': 'Диалоги',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='SuggestedResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField(verbose_name='Текст ответа')),
                ('confidence_score', models.FloatField(default=0.0, verbose_name='Уверенность')),
                ('is_used', models.BooleanField(default=False, verbose_name='Использован')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('dialogue', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='suggested_responses',
                    to='tg_assistant.dialogue',
                    verbose_name='Диалог'
                )),
            ],
            options={
                'verbose_name': 'Предложенный ответ',
                'verbose_name_plural': 'Предложенные ответы',
                'ordering': ['-confidence_score'],
            },
        ),
    ]