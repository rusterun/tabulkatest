from django.db import models


class Bookings(models.Model):
    id = models.IntegerField('id',primary_key=True)
    arrival = models.DateField('Заезд')
    departure = models.DateField('Выезд')
    first_name = models.CharField('Имя', default="", max_length=60)
    last_name = models.CharField('Фамилия', default="", max_length=60)
    property = models.ForeignKey('Properties', on_delete=models.PROTECT)
    adults = models.IntegerField('Кол-во взрослых')
    children = models.IntegerField('Кол-во детей')
    infants = models.IntegerField('Кол-во младенцев')
    pets = models.IntegerField('Кол-во питомцев')
    comment = models.TextField('Комментарий к бронированию', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.arrival} - {self.departure} ({self.property})'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class Comments(models.Model):
    date = models.DateField('Дата')
    comment = models.TextField('Комментарий')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Properties(models.Model):
    property = models.CharField('Апартамент', max_length=30)

    def __str__(self):
        return self.property

    class Meta:
        verbose_name = 'Апартамент'
        verbose_name_plural = 'Апартаменты'

class Configs(models.Model):
    config_name = models.CharField('Конфигурация', max_length=60, primary_key=True)
    config_value = models.IntegerField('Значение')

    def __str__(self):
        return str(self.config_name) + " = " + str(self.config_value)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

class Blocks(models.Model):
    arrival = models.DateField('Заезд')
    departure = models.DateField('Выезд')
    property = models.ForeignKey('Properties', on_delete=models.PROTECT)
    def __str__(self):
        return f'BLOCK: {self.property} {self.arrival} - {self.departure}'

    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'