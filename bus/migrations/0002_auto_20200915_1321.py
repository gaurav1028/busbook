# Generated by Django 3.1 on 2020-09-15 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_plate', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination', to='bus.busstop')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source', to='bus.busstop')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField()),
                ('bus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bus.bus')),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bus.route'),
        ),
    ]