from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0026_item_branch_printtype_model_alter_item_is_sleeve_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_code',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

