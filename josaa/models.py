from django.db import models

class AcademicProgram(models.Model):
    ID = models.IntegerField(primary_key=True)
    Institute = models.CharField(max_length=100)
    AcademicProgramName = models.CharField(max_length=200)
    Quota = models.CharField(max_length=50)
    SeatType = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50, blank=True, null=True)
    OpeningRank = models.FloatField(blank=True, null=True)
    ClosingRank = models.FloatField(blank=True, null=True)
    Year = models.IntegerField()
    Round = models.IntegerField()

    def __str__(self):
        return self.AcademicProgramName