# Generated by Django 2.0.1 on 2018-02-09 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testerka', '0002_auto_20180208_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='testsText',
            field=models.TextField(blank=True, default='', verbose_name='Testy'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='testquestion',
            order_with_respect_to=None,
        ),
    ]
