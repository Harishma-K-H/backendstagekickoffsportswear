import pandas as pd
from django.core.management.base import BaseCommand
from user_auth.models import Item, Model_data, Material, PrintType, Branch
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class Command(BaseCommand):
    help = 'Import items from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the items CSV file')

    def handle(self, *args, **kwargs):
        path = kwargs['csv_path']
        self.stdout.write(f"📂 Importing items from: {path}")

        df = pd.read_csv(path)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        inserted = 0
        skipped = 0

        for index, row in df.iterrows():
            if pd.isna(row['item_code']):
                self.stderr.write(f"⚠️ Row {index} skipped: Missing item_code")
                skipped += 1
                continue

            try:
                model_id = int(row['model_id']) if pd.notna(row['model_id']) else None
                material_id = int(row['material_id']) if pd.notna(row['material_id']) else None
                print_type_id = int(row['print_type_id']) if pd.notna(row['print_type_id']) else None
                branch_id = int(row['branch']) if pd.notna(row['branch']) else None

                # Check for required fields only (material_id is optional)
                missing_fields = []
                if not model_id:
                    missing_fields.append('model_id')
                if not print_type_id:
                    missing_fields.append('print_type_id')
                if not branch_id:
                    missing_fields.append('branch')

                if missing_fields:
                    self.stderr.write(f"⚠️ Row {index} skipped: Missing fields: {', '.join(missing_fields)}.")
                    skipped += 1
                    continue

                model = Model_data.objects.get(id=model_id)
                print_type = PrintType.objects.get(id=print_type_id)
                branch = Branch.objects.get(id=branch_id)
                material = Material.objects.get(id=material_id) if material_id else None

                item = Item.objects.create(
                    name=row['name'],
                    item_code=row['item_code'],
                    item_cost=row['item_cost'] if pd.notna(row['item_cost']) else 0,
                    item_alert=row['item_alert'] if pd.notna(row['item_alert']) else None,
                    model=model,
                    material=material,
                    print_type=print_type,
                    size=row['size'] if pd.notna(row['size']) else '',
                    branch=branch,
                    is_sleeve=row['is_sleeve'] if pd.notna(row['is_sleeve']) else '',
                    item_description=row['item_description'] if pd.notna(row['item_description']) else '',
                    created_at=datetime.strptime(row['created_at'], "%d-%m-%Y %H:%M") if pd.notna(row['created_at']) else None,
                    is_active=True
                )
                self.stdout.write(f"✅ Row {index}: '{item.item_code}' inserted.")
                inserted += 1

            except ObjectDoesNotExist as e:
                self.stderr.write(f"⚠️ Row {index} skipped: {e}")
                skipped += 1
                continue
            except ValueError as e:
                self.stderr.write(f"⚠️ Row {index} skipped: Invalid value - {e}")
                skipped += 1
                continue

        self.stdout.write(f"🎉 Import completed: {inserted} inserted, {skipped} skipped.")

