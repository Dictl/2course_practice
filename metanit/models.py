# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Component(models.Model):
    category = models.ForeignKey('Componentcategory', models.DO_NOTHING)
    manufacturer = models.ForeignKey('Manufacturer', models.DO_NOTHING)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    warranty_months = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'component'


class Componentcategory(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'componentcategory'


class Cpu(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    cores = models.IntegerField()
    threads = models.IntegerField()
    clock_speed = models.DecimalField(max_digits=5, decimal_places=2)
    socket = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cpu'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Gpu(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    vram = models.IntegerField()
    memory_type = models.CharField(max_length=20)
    power_consumption = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gpu'


class Hdd(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    capacity = models.IntegerField()
    form_factor = models.CharField(max_length=20)
    rotation_speed = models.IntegerField()
    interface = models.CharField(max_length=10)
    speed = models.IntegerField()
    cache_size = models.IntegerField()
    durability = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'hdd'


class Incompatiblecomponents(models.Model):
    first_component = models.ForeignKey(Component, models.DO_NOTHING, db_column='first_component')
    second_component = models.ForeignKey(Component, models.DO_NOTHING, db_column='second_component', related_name='incompatiblecomponents_second_component_set')

    class Meta:
        managed = False
        db_table = 'incompatiblecomponents'


class Manufacturer(models.Model):
    name = models.CharField(unique=True, max_length=100)
    website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manufacturer'


class Motherboard(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    cpu_socket = models.CharField(max_length=20)
    chipset = models.CharField(max_length=20)
    ram_socket = models.CharField(max_length=20)
    expansion_slots = models.CharField(max_length=50)
    interface = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'motherboard'


class Psu(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    psu_power = models.IntegerField()
    certification = models.CharField(max_length=10)
    modularity = models.BooleanField(blank=True, null=True)
    protection = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'psu'


class Ram(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    capacity = models.IntegerField()
    speed = models.IntegerField()
    latency = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ram'


class Ssd(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    capacity = models.IntegerField()
    ssd_type = models.CharField(max_length=20)
    form_factor = models.CharField(max_length=10)
    speed = models.IntegerField()
    tbw = models.IntegerField()
    controller = models.CharField(max_length=20)
    memory = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ssd'
