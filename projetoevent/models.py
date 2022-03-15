from django.db import models


class Event(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    code = models.IntegerField()
    rfid = models.IntegerField()
    status = models.IntegerField()
    user_id = models.IntegerField()
    type = models.IntegerField()
    gate = models.IntegerField()
    sector = models.IntegerField()
    block = models.CharField(max_length=100)
    row = models.CharField(max_length=100)
    seat = models.IntegerField()
    extra = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
