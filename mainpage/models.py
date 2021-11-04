from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Subdivision(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class DetailOfUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField()
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.surname} {self.patronymic} - {self.position}'

    def get_duration(self):
        timedelta = date.today() - self.start_date

        years = int(timedelta.days // 365.25)

        # Форматиорвание текста под года
        if years < 1:
            return 'Менее одного года'
        elif years > 10 and years%10 < 21:
            return f'{years} лет'
        elif years%10 == 1:
            return f'{years} год'
        elif years%10 >1 and years%10<5:
            return f'{years} года'
        elif (years%10 > 4 and years < 10) or years%10 == 0:
            return f'{years} лет'
        else:
            return 'Error'