from django.db import models

class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=5)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=1)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.precinct_number}"


import csv
from django.db import IntegrityError

def load_data(file_path):
    from .models import Voter
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'] or None,
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=row['Date of Birth'],
                    date_of_registration=row['Date of Registration'],
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'].strip().upper() == 'TRUE',
                    v21town=row['v21town'].strip().upper() == 'TRUE',
                    v21primary=row['v21primary'].strip().upper() == 'TRUE',
                    v22general=row['v22general'].strip().upper() == 'TRUE',
                    v23town=row['v23town'].strip().upper() == 'TRUE',
                    voter_score=int(row['voter_score']),
                )
            except IntegrityError:
                print(f"Failed to insert row for {row['Voter ID Number']}")
            except ValueError as e:
                print(f"ValueError: {e} for row {row['Voter ID Number']}")
