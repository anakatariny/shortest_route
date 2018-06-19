# Generated by Django 2.0.6 on 2018-06-18 23:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shortest_route_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('file', models.FileField(upload_to='')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='map',
            name='name',
        ),
        migrations.RemoveField(
            model_name='map',
            name='path',
        ),
        migrations.RemoveField(
            model_name='route',
            name='map_id',
        ),
        migrations.AddField(
            model_name='map',
            name='first_edge',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='second_edge',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='value',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='file_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shortest_route_app.FileMap'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='file_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shortest_route_app.FileMap'),
            preserve_default=False,
        ),
    ]