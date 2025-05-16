from django.db import models

class ComponentCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'componentcategory'
        app_label = 'metanit'

class Formfactor(models.Model):
    id = models.IntegerField(primary_key=True)
    ff = models.CharField(unique=True, max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'formfactor'
        app_label = 'metanit'

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'manufacturer'
        app_label = 'metanit'

class Component(models.Model):
    category = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, db_column='category_id')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, db_column='manufacturer_id')
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    warranty_months = models.IntegerField(blank=True, null=True)
    country_of_origin = models.CharField(max_length=30, blank=True, null=True)
    link_to_store = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'component'
        app_label = 'metanit'

class CPU(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    cores = models.IntegerField()
    threads = models.IntegerField()
    base_clock_speed = models.DecimalField(max_digits=5, decimal_places=2)
    socket = models.CharField(max_length=20)
    max_clock_speed = models.DecimalField(max_digits=5, decimal_places=2)
    core_name = models.CharField(max_length=20, blank=True, null=True)
    ram_type = models.CharField(max_length=20)
    max_ram_vol = models.IntegerField()
    tdp = models.IntegerField()
    max_temperature = models.IntegerField()
    integrated_pci_e_controller = models.CharField(max_length=20)
    pci_e_lanes_amount = models.IntegerField(null=True)
    integrated_graphics = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'cpu'
        app_label = 'metanit'

class GPU(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    vram = models.IntegerField()
    memory_type = models.CharField(max_length=20)
    power_consumption = models.IntegerField(null=True)
    max_monitors = models.IntegerField()
    hdmi_ver = models.CharField(max_length=4)
    max_res = models.CharField(max_length=50)
    pci_e_lines_amount = models.IntegerField()
    amount_of_exp_slots = models.IntegerField()
    dimensions = models.CharField(max_length=20)
    interface = models.CharField(max_length=20, blank=True, null=True)
    interface_form_factor = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'gpu'
        app_label = 'metanit'

class RAM(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True, db_column='component_id')
    capacity = models.IntegerField()
    speed = models.IntegerField()
    latency = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ram'
        app_label = 'metanit'

class Motherboard(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    cpu_socket = models.CharField(max_length=20)
    chipset = models.CharField(max_length=20)
    ram_slots = models.IntegerField(blank=True, null=True)
    ram_type = models.CharField(max_length=20, blank=True, null=True)
    pci_e_ver_exp = models.CharField(max_length=5, blank=True, null=True)
    nvme_support = models.BooleanField(blank=True, null=True)
    m_2_slots = models.IntegerField(blank=True, null=True)
    sata_slots = models.IntegerField(blank=True, null=True)
    dimensions = models.CharField(max_length=20, blank=True, null=True)
    m_2_pci_e_cpu_line = models.CharField(max_length=70, blank=True, null=True)
    m_2_pci_e_chipset_line = models.CharField(max_length=50, blank=True, null=True)
    form_factor = models.CharField(max_length=10, blank=True, null=True)
    supported_cores = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'motherboard'
        app_label = 'metanit'

class SSD(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    capacity = models.IntegerField()
    ssd_type = models.CharField(max_length=20)
    form_factor = models.CharField(max_length=10)
    tbw = models.IntegerField()
    memory = models.CharField(max_length=20)
    max_seq_read_speed = models.IntegerField(blank=True, null=True)
    max_seq_write_speed = models.IntegerField(blank=True, null=True)
    controller = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'ssd'
        app_label = 'metanit'

class HDD(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, primary_key=True, db_column='component_id')
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

class PSU(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    psu_power = models.IntegerField()
    certification = models.CharField(max_length=10)
    modularity = models.BooleanField(blank=True, null=True)
    protection = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'psu'
        app_label = 'metanit'


class IncompatibleComponents(models.Model):
    first_component = models.ForeignKey(Component, models.DO_NOTHING, db_column='first_component')
    second_component = models.ForeignKey(Component, models.DO_NOTHING, db_column='second_component', related_name='incompatiblecomponents_second_component_set')

    class Meta:
        managed = False
        db_table = 'incompatiblecomponents'
        app_label = 'metanit'

class PCCase(models.Model):
    component = models.OneToOneField(Component, models.DO_NOTHING, primary_key=True)
    dimensions = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=2, decimal_places=1)
    color = models.CharField(max_length=20, blank=True, null=True)
    psu_form_factor = models.CharField(max_length=20)
    max_gpu_length = models.IntegerField()
    max_cpu_cooler_height = models.IntegerField()
    horizontal_expansion_slots_amount = models.IntegerField()
    two_p_five_drives_amount = models.IntegerField()
    three_p_five_drives_amount = models.IntegerField()
    fans_included = models.CharField(max_length=20, blank=True, null=True)
    frontal_fan_support = models.CharField(max_length=50, blank=True, null=True)
    rear_fan_support = models.CharField(max_length=20, blank=True, null=True)
    upper_fan_support = models.CharField(max_length=50, blank=True, null=True)
    bottom_fan_support = models.CharField(max_length=50, blank=True, null=True)
    side_fan_support = models.CharField(max_length=50, blank=True, null=True)
    io_panel_loc = models.CharField(max_length=10)
    connectors = models.CharField(max_length=100)
    max_form_factor = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'pc_case'
        app_label = 'metanit'
