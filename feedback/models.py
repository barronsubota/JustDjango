# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Feedback(models.Model):
    """
    Модель відгуків користувачів для продуктів або загальна.
    Розміщується у окремому Django-приложенні "feedback".
    """
    STATUS_CHOICES = [
        ('new', _('Новий')),
        ('in_progress', _('В обробці')),
        ('resolved', _('Вирішено')),
        ('closed', _('Закрито')),
    ]

    CATEGORY_CHOICES = [
        ('general', _('Загальний')),
        ('product', _('Продукт')),
        ('service', _('Сервіс')),
        ('other', _('Інше')),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID відгуку')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='feedbacks',
        verbose_name=_('Користувач'),
        null=True,
        blank=True,
        help_text=_('Авторизований користувач, що залишив відгук')
    )
    product = models.ForeignKey(
        'fabric.Product',
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name=_('Продукт'),
        null=True,
        blank=True,
        help_text=_('Прив’язати відгук до конкретного продукту')
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general',
        verbose_name=_('Категорія відгуку')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=_('Статус обробки')
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Оцінка'),
        help_text=_('Оцінка від 1 до 5')
    )
    comment = models.TextField(
        verbose_name=_('Коментар'),
        help_text=_('Текст відгуку')
    )
    language = models.CharField(
        max_length=10,
        default='uk',
        verbose_name=_('Мова відгуку'),
        help_text=_('Код мови тексту відгуку')
    )
    manager_response = models.TextField(
        blank=True,
        verbose_name=_('Відповідь менеджера'),
        help_text=_('Текст відповіді менеджера на відгук')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата створення')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата оновлення')
    )

    class Meta:
        verbose_name = _('Відгук')
        verbose_name_plural = _('Відгуки')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        user_display = self.user.username if self.user else _('Анонім')
        return f"[{self.get_status_display()}] {user_display} - {self.rating}/5"
