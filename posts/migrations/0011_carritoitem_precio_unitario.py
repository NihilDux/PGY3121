# Generated by Django 4.2.2 on 2023-07-06 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_id_categoria_alter_post_precio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carritoitem',
            name='precio_unitario',
            field=models.PositiveIntegerField(default=0),
        ),
    ]