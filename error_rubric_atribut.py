from django.db import models
from django.contrib.auth.models import User

#Валидаторы
from django.core import validators
from django.core.exceptions import ValidationError
# Create your models here.


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар', help_text='<br>Введите название товара',
                             validators=[validators.MinLengthValidator(limit_value=3,
                                                                       message='Названиедолжносодержать более 3х символов')]
)
    content = models.TextField(null=True, blank=True, verbose_name='Описание',
                               help_text='<br>Опишите подробно что вы продаете',
                               validators=[validators.MinLengthValidator(limit_value=100,
                                                                        message='Описание должно содержать не менее 100 символов')])
    price = models.FloatField(null=True, blank=True, verbose_name='Цена',
                              help_text='<br>Цена пишиться без пробелов пример 5000')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        verbose_name_plural = 'Объявления'#множественное число
        verbose_name = 'Объявление'#единственное число
        get_latest_by = ['-published']#Последовательность полей по которым будет выполняться сортировка
        #order_with_respect_to = 'rubric'
        """
    def clean(self):
        #Еще один вариант валидатора, более удобный я указал в моделе
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продоваемого товара')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите не отрицательное значение цены')

        if errors:
            raise ValidationError(errors)
        """
    def title_and_price(self):
        """функцианально поле возвращает название и цену """
        if self.price:
            return '%s (%.2f  ₽)' % (self.title, self.price)

        else:
            return self.title

    title_and_price.short_description = 'Название и цена'

    def __str__(self):
        return self.title

class Rubric(models.Model):
    """Создание рубрики одна со многими"""
    name = models.CharField(max_length=30, db_index=True, verbose_name='Название')

    def __str__(self):# Имя в админке при сохранении
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

class AdvUser(models.Model):
    is_activvated = models.BooleanField(default=True, verbose_name='Активирован')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'пользователя'

    def __str__(self):
        name = 'Список пользователей'
        return name


class Spare(models.Model):
    """Хранит детали авто"""
    name = models.CharField(max_length=30, verbose_name='Детали')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Детали'
        verbose_name = 'Деталь'

class Machine(models.Model):
    """Хранит готовые авто"""
    name = models.CharField(max_length=30, verbose_name='Машину')
    spares = models.ManyToManyField(Spare)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Машины'
        verbose_name = 'Машину'
