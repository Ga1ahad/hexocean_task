import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


def add_sizes(apps, schema_editor):
    ThumbnailSize = apps.get_model('thumbnail', 'ThumbnailSize')
    ThumbnailSize.objects.create(thumbnail_size=200)
    ThumbnailSize.objects.create(thumbnail_size=400)


def add_tiers(apps, schema_editor):
    AccountTier = apps.get_model('thumbnail', 'AccountTier')
    ThumbnailSize = apps.get_model('thumbnail', 'ThumbnailSize')
    thumbnail_200 = ThumbnailSize.objects.get(thumbnail_size=200)
    thumbnail_400 = ThumbnailSize.objects.get(thumbnail_size=400)
    basic = AccountTier.objects.create(name='Basic')
    basic.thumbnail_size.add(thumbnail_200)
    premium = AccountTier.objects.create(name='Premium', original_img=True)
    premium.thumbnail_size.add(thumbnail_200, thumbnail_400)
    enterprise = AccountTier.objects.create(name='Enterprise', original_img=True, fetch_expired=True)
    enterprise.thumbnail_size.add(thumbnail_200, thumbnail_400)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThumbnailSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail_size', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('fetch_expired', models.BooleanField(default=False)),
                ('original_img', models.BooleanField(default=False)),
                ('thumbnail_size', models.ManyToManyField(blank=True, related_name='thumbnail_sizes',
                                                          to='thumbnail.thumbnailsize')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all'
                                                                              ' permissions without explicitly'
                                                                              ' assigning them.',
                                                     verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                              help_text='Required. 150 characters or fewer.'
                                                        ' Letters, digits and @/./+/-/_ only.', max_length=150,
                                              unique=True,
                                              validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                              verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. '
                                                            'Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. '
                                                                        'A user will get all permissions granted '
                                                                        'to each of their groups.',
                                                  related_name='user_set', related_query_name='user',
                                                  to='auth.group', verbose_name='groups')),
                ('tier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to='thumbnail.accounttier')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RunPython(add_sizes),
        migrations.RunPython(add_tiers)
    ]
