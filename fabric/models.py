#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
import uuid


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Назва категорії',
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name='URL-ярлик',
        help_text='Автоматично генерується з назви категорії'
    )

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категорія'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Назва продукту'
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name='URL-ярлик'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Опис'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Ціна'
    )
    currency = models.CharField(
        max_length=3,
        choices=[
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('UAH', 'Ukrainian Hryvnia'),
        ],
        default='UAH',
        verbose_name='Валюта'
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Артикул (SKU)'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Наявність на складі'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активний'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата останнього оновлення'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class ProductImage(models.Model):
    """
    Зображення для продукту: підтримує декілька зображень на продукт.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        verbose_name='Зображення'
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Альтернативний текст'
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Порядок'
    )

    class Meta:
        verbose_name = 'Зображення продукту'
        verbose_name_plural = 'Зображення продуктів'
        ordering = ['order']

    def __str__(self):
        return f"Image {self.id} for {self.product.name}"
