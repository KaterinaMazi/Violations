from django.db import models
from datetime import datetime


class Violation(models.Model):
    code = models.CharField(max_length=10, unique=True)
    legal_basis = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    driver_fine = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    owner_fine = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    eu_code = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.legal_basis} - {self.eu_code}"


class Violator(models.Model):
    circulation_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    violations = models.ManyToManyField(
        Violation,
        through='ViolationRecord',
        related_name='violators'
    )

    def __str__(self):
        return f"{self.circulation_number} - {self.name}"


class ViolationRecord(models.Model):
    DRIVER = 'Οδηγός'
    OWNER = 'Ιδιοκτήτης'

    VIOLATOR_CHOICES = [
        (DRIVER, 'Οδηγός'),
        (OWNER, 'Ιδιοκτήτης'),
    ]

    violator = models.ForeignKey(Violator, on_delete=models.CASCADE)
    violation = models.ForeignKey(Violation, on_delete=models.PROTECT)
    datetime_inspection = models.DateTimeField(default=datetime.now)
    previous_inspection = models.DateTimeField(null=True, blank=True)
    kind_violator = models.CharField(
        max_length=10,
        choices=VIOLATOR_CHOICES,
        default=OWNER
    )


    @property
    def fine_amount(self):
        if self.kind_violator == self.DRIVER:
            return self.violation.driver_fine
        else:
            return self.violation.owner_fine

    def days_difference(self):
        if self.previous_inspection:
            return (self.datetime_inspection - self.previous_inspection).days

