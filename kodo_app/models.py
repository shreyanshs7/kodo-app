from django.db import models

# Create your models here.
class MockData(models.Model):
    class Meta:
        db_table = 'mock_datas'

    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    description = models.TextField()
    date_last_edited = models.DateTimeField()

    def __str__(self) -> str:
        return '<{}>'.format(self.name)
