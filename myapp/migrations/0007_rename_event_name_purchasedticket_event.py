# Generated by Django 3.2.6 on 2023-11-14 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20231114_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchasedticket',
            old_name='event_name',
            new_name='event',
        ),
    ]
