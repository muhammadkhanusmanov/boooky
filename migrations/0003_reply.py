# Generated by Django 4.2.6 on 2023-10-18 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_api', '0002_alter_ebook_book_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('ruxsat', models.CharField(choices=[('Ruxsat', True), ('Mumkinmas', False)], default='Mumkinmas', max_length=10)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='main_api.message')),
            ],
        ),
    ]
