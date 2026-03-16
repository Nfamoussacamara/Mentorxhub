# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='banners/'),
        ),
    ]

