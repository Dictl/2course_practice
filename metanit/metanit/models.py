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

class ComponentCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'componentcategory'
        app_label = 'metanit'
        managed = False

class FormFactor(models.Model):
    ff = models.CharField(unique=True, max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'formfactor'
        app_label = 'metanit'
        managed = False

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'manufacturer'
        app_label = 'metanit'
        managed = False

class Component(models.Model):
    category = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, db_column='category_id')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, db_column='manufacturer_id')
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    warranty_months = models.IntegerField(blank=True, null=True)
    country_of_origin = models.CharField(max_length=100, blank=True, null=True)
    link_to_store = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.model

    class Meta:
        db_table = 'component'
        app_label = 'metanit'
        managed = False


class CPU(models.Model):
    component = models.OneToOneField('Component', on_delete=models.CASCADE, primary_key=True, db_column='component_id')
    cores = models.IntegerField()
    threads = models.IntegerField()
    base_clock_speed = models.FloatField()
    socket = models.CharField(max_length=20)
    max_clock_speed = models.FloatField()
    core_name = models.CharField(max_length=50)
    ram_type = models.CharField(max_length=20)
    max_ram_vol = models.IntegerField()
    tdp = models.IntegerField()
    max_temperature = models.IntegerField()
    integrated_pci_e_controller = models.CharField(max_length=20)
    pci_e_lanes_amount = models.IntegerField()
    integrated_graphics = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'cpu'
        app_label = 'metanit'
        managed = False


class GPU(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True, db_column='component_id')
    vram = models.IntegerField()
    memory_type = models.CharField(max_length=20)
    power_consumption = models.IntegerField(blank=True, null=True)
    max_monitors = models.IntegerField()
    hdmi_ver = models.CharField(max_length=10)
    max_res = models.CharField(max_length=30)
    pci_e_lines_amount = models.IntegerField()
    amount_of_exp_slots = models.IntegerField()
    dimensions = models.CharField(max_length=30)
    interface = models.CharField(max_length=20)
    interface_form_factor = models.CharField(max_length=20)

    class Meta:
        db_table = 'gpu'
        app_label = 'metanit'
        managed = False

class HDD(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True)
    capacity = models.IntegerField()
    form_factor = models.CharField(max_length=20)
    rotation_speed = models.IntegerField()
    interface = models.CharField(max_length=10)
    speed = models.IntegerField()
    cache_size = models.IntegerField()
    durability = models.CharField(max_length=20)

    class Meta:
        db_table = 'hdd'
        app_label = 'metanit'
        managed = False


class SSD(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True)
    capacity = models.IntegerField()
    ssd_type = models.CharField(max_length=20)
    form_factor = models.CharField(max_length=20)
    tbw = models.IntegerField()
    memory = models.CharField(max_length=20)
    max_seq_read_speed = models.IntegerField(blank=True, null=True)
    max_seq_write_speed = models.IntegerField(blank=True, null=True)
    controller = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'ssd'
        app_label = 'metanit'
        managed = False

class RAM(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True)
    latency = models.IntegerField()
    amount_of_plates = models.IntegerField()
    volume_of_each = models.IntegerField()
    memory_type = models.CharField(max_length=20)
    cl = models.IntegerField()
    trp = models.IntegerField()
    trcd = models.IntegerField(blank=True, null=True)
    tras = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ram'
        app_label = 'metanit'
        managed = False



class Motherboard(models.Model):
    component = models.OneToOneField('Component', on_delete=models.CASCADE, primary_key=True, db_column='component_id')
    cpu_socket = models.CharField(max_length=20)
    chipset = models.CharField(max_length=30)
    ram_slots = models.IntegerField()
    ram_type = models.CharField(max_length=10)
    pci_e_ver_exp = models.CharField(max_length=10, blank=True, null=True)
    nvme_support = models.BooleanField()
    m_2_slots = models.IntegerField()
    sata_slots = models.IntegerField()
    dimensions = models.CharField(max_length=20)
    m_2_pci_e_cpu_line = models.CharField(max_length=100)
    m_2_pci_e_chipset_line = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=20)
    supported_cores = models.CharField(max_length=100)

    class Meta:
        db_table = 'motherboard'
        app_label = 'metanit'
        managed = False


class PSU(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True)
    psu_power = models.IntegerField()
    certification = models.CharField(max_length=20)
    modularity = models.BooleanField(blank=True, null=True)
    protection = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=20)

    class Meta:
        db_table = 'psu'
        app_label = 'metanit'
        managed = False

class IncompatibleComponents(models.Model):
    first_component = models.ForeignKey(Component, on_delete=models.CASCADE, db_column='first_component', related_name='incompatible_first')
    second_component = models.ForeignKey(Component, on_delete=models.CASCADE, db_column='second_component', related_name='incompatible_second')

    class Meta:
        db_table = 'incompatiblecomponents'
        app_label = 'metanit'
        managed = False

class Workstation(models.Model):
    category_id = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, db_column='category_id')
    component_name = models.CharField(max_length=50)
    balanced_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    cpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    gpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    ram_memory_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        db_table = 'workstation'
        app_label = 'metanit'
        managed = False

class OfficePc(models.Model):
    category_id = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, db_column='category_id')
    component_name = models.CharField(max_length=50)
    balanced_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    cpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    gpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    ram_memory_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        db_table = 'office_pc'
        app_label = 'metanit'
        managed = False

class MultimediaPc(models.Model):
    category_id = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, db_column='category_id')
    component_name = models.CharField(max_length=50)
    balanced_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    cpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    gpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    ram_memory_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        db_table = 'multimedia_pc'
        app_label = 'metanit'
        managed = False

class GamingPc(models.Model):
    category_id = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, db_column='category_id')
    component_name = models.CharField(max_length=50)
    balanced_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    cpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    gpu_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    ram_memory_priority_coefficient = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        db_table = 'gaming_pc'
        app_label = 'metanit'
        managed = False


class PCCase(models.Model):
    component = models.OneToOneField('Component', on_delete=models.CASCADE, primary_key=True)
    dimensions = models.CharField(max_length=50)
    weight = models.FloatField()
    color = models.CharField(max_length=20)
    psu_form_factor = models.CharField(max_length=20)
    max_gpu_length = models.IntegerField()
    max_cpu_cooler_height = models.IntegerField()
    horizontal_expansion_slots_amount = models.IntegerField()
    two_p_five_drives_amount = models.IntegerField()
    three_p_five_drives_amount = models.IntegerField()
    fans_included = models.CharField(max_length=50)
    frontal_fan_support = models.CharField(max_length=50)
    rear_fan_support = models.CharField(max_length=50)
    upper_fan_support = models.CharField(max_length=50)
    bottom_fan_support = models.CharField(max_length=50)
    side_fan_support = models.CharField(max_length=50)
    io_panel_loc = models.CharField(max_length=20)
    connectors = models.CharField(max_length=255)
    max_form_factor = models.CharField(max_length=20)

    class Meta:
        db_table = 'pc_case'
        app_label = 'metanit'
        managed = False


class CoolingSystem(models.Model):
    component = models.OneToOneField('Component', on_delete=models.CASCADE, primary_key=True)
    tdp = models.IntegerField()
    fan_amount = models.IntegerField()
    fan_size = models.IntegerField()
    rpm_min = models.IntegerField()
    heat_pipes_amount = models.IntegerField()
    radiator_material = models.CharField(max_length=100)
    sockets = models.CharField(max_length=255)
    rpm_max = models.IntegerField()
    dimensions = models.CharField(max_length=50)
    max_noise = models.FloatField()
    base_material = models.CharField(max_length=100)
    rated_current = models.FloatField()
    rated_voltage = models.FloatField()

    class Meta:
        managed = False
        db_table = 'coolingsystem'
        app_label = 'metanit'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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