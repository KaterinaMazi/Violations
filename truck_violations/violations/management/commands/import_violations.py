import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from violations.models import Violation


class Command(BaseCommand):
    help = "Import violations data from an Excel file"

    def handle(self, *args, **options):
        excel_file = "data/violations.xlsx"

        Violation.objects.all().delete()

        df = pd.read_excel(excel_file)

        df = df.replace({np.nan: None})

        total_imported = 0
        for index, row in df.iterrows():
            Violation.objects.create(
                code=row['Α/Α'],
                legal_basis=row['Νομική Βάση'],
                eu_code=row.get('EU Code', row.get('eu_code', None)),
                owner_fine=row.get('Πρόστιμο Ιδιοκτήτη', row.get('Owner Fine', None)),
                driver_fine=row.get('Πρόστιμο Οδηγού', row.get('Driver Fine', None))
            )
            total_imported += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Επιτυχής εισαγωγή {total_imported} δεδομένων!"))