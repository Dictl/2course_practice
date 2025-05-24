from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        UserPreferences.objects.create(user=instance)
class UserPreferences(models.Model):
    PURPOSE_CHOICES = [
        ('gaming', 'Игровой'),
        ('office', 'Офисный'),
        ('workstation', 'Рабочая станция'),
        ('home', 'Домашний мультимедиа'),
    ]
    
    PRIORITY_CHOICES = [
        ('balanced', 'Балансированная сборка'),
        ('cpu', 'Процессор'),
        ('gpu', 'Видеокарта'),
        ('storage', 'Память и накопители'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='hello_preferences',  # Уникальное имя для этого приложения
        related_query_name='hello_preference'
    )

    class Meta:
        db_table = 'hello_userpreferences'

    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='gaming')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='balanced')
    
    def __str__(self):
        return f"Preferences for {self.user.username}"