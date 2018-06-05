from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Create your models here.
class Owner(User):
    phone_tel = models.CharField(max_length=24, blank=True, null=True)
    SlackCon = models.CharField(max_length=24, blank=True, null=True)
    FBCon = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']


class Car(models.Model):
    owner = models.ManyToManyField(Owner)
    manufacturer = models.CharField(max_length=24, )
    pic = models.CharField(max_length=24, ) #picture name (full name from pictures directory)
    reg_no = models.CharField(max_length=24, )
    model = models.CharField(max_length=24, )
    prod_year = models.DecimalField(decimal_places=0, max_digits=4,  null=True) #XXXX
    engine_model = models.CharField(max_length=24, blank=True, null=True)
    VIN = models.CharField(max_length=30, blank=True, null=True)
    fuel_choices = (
        ("gasoline", "gasoline"),
        ("diesel", "diesel"),
        ("electricity", "electricity"),
        ("hybrid", "hybrid")
    )
    fuel = models.CharField(choices=fuel_choices, max_length=24)
    power = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)     # unit: Horse Power (KM)
    torque = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)     # unit: Nm
    engine_capacity = models.DecimalField(decimal_places=0, max_digits=9)   #unit: ccm

    def __str__(self):
        return "{} {} {}".format(self.manufacturer, self.model, round(self.engine_capacity/1000, 1))

    def getName(self):
        return "{} {} {}".format(self.manufacturer, self.model, round(self.engine_capacity / 1000, 1))

    class Meta:
        ordering = ['manufacturer', 'model', 'engine_capacity']


class Milage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    milage = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)  # unit: km
    date = models.DateTimeField()

    def __str__(self):
        return str("{} : {}".format(self.milage, self.car.getName()))


class ActionPopular(models.Model):
    title = models.CharField(max_length=224)
    desc = models.CharField(max_length=224)

    def __str__(self):
        return self.title


class ActionTemplate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    action_popular = models.ForeignKey(ActionPopular, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=224, blank=True, null=True)     #if action is not very popular add title here
    desc = models.CharField(max_length=224, blank=True, null=True)      #if action is not very popular add desc here
    action_milage_period = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)
    action_days_period = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)
    action_end_date = models.DateTimeField(blank=True, null=True)  # end date if date is strict
    product = models.CharField(max_length=224, blank=True, null=True)
    product_quantity = models.CharField(max_length=224, blank=True, null=True)

    def __str__(self):
        if self.action_popular:
            return "{} {}".format(self.car, self.action_popular.title)
        else:
            return "{} {}".format(self.car, self.title)


class Action(models.Model):
    ActionTemplate = models.ForeignKey(ActionTemplate, on_delete=models.CASCADE)
    milage = models.ForeignKey(Milage, on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.CharField(max_length=224)
    cost = models.DecimalField(decimal_places=2, max_digits=9, blank=True, null=True)# cost in PLN
    product = models.CharField(max_length=224, blank=True, null=True)

    def __str__(self):
        if self.ActionTemplate.action_popular:
            return "{} {}".format(self.ActionTemplate.car, self.ActionTemplate.action_popular.title)
        else:
            return "{} {}".format(self.ActionTemplate.car, self.ActionTemplate.title)
