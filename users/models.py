from django.db import models
from django.contrib.auth.models import User



class Employee(models.Model):
    
    dasic_user_data = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey("Department", on_delete=models.DO_NOTHING)
    posithion = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    salary = models.PositiveIntegerField(default = 0)


    def __str__(self):
        """Unicode representation of MODELNAME."""
        return self.dasic_user_data.username


class Department(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
















