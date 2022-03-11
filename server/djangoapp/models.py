from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=256)
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    model_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(null=False, max_length=30)
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    MODEL_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV,"SUV"),
        (WAGON, "Wagon")
    ]
    model_type = models.CharField(null=False, max_length=30, choices=MODEL_CHOICES, default=SEDAN)
    year = models.DateField(null=True, )
    def __str__(self):
        return "Make: " + str(self.model_make) + "," + \
                "Dealer ID: " + str(self.dealer_id) + "," + \
                "Model Name: " + self.name + "," + \
                "Model Type: " + str(self.model_type)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
