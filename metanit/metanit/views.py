from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.shortcuts import render

def build_detail_view(request, build_id):
    return render(request, 'metanit/build_detail.html', {'build_id': build_id})

class BuildListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        budget = request.GET.get('budget')
        purpose = request.GET.get('purpose')
        priority = request.GET.get('priority')

        print('purpose:', purpose)
        print('priority:', priority)

        # Валидация входных данных
        if not budget or not purpose or not priority:
            return Response({'error': 'Все параметры обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        PURPOSE_MODEL_MAP = {
            'gaming': GamingPc,
            'office': OfficePc,
            'home': MultimediaPc,
            'workstation': Workstation,
        }

        model = PURPOSE_MODEL_MAP.get(purpose.lower())
        if not model:
            return Response({'error': 'Некорректное значение purpose'}, status=400)

        data = model.objects.all()

        PRIORITY_FIELD_MAP = {
            'balanced': 'balanced_coefficient',
            'cpu': 'cpu_priority_coefficient',
            'gpu': 'gpu_priority_coefficient',
            'storage': 'ram_memory_priority_coefficient',
        }

        priority_field = PRIORITY_FIELD_MAP.get(priority.lower())
        if not priority_field:
            return Response({'error': 'Некорректное значение priority'}, status=400)

        total = model.objects.aggregate(sum=Sum(priority_field))['sum'] or 0
        print(f'Сумма по полю {priority_field} для {purpose}:', total)

        # budget и total должны быть числами
        part_budget = (float(budget)*1.3) / float(total) if total else 0
        print(f'Часть бюджета на 1 коэффициент: {part_budget}')

        # Получаем бюджет для каждого компонента из таблицы БД
        component_budgets = []
        for obj in data:
            coef = float(getattr(obj, priority_field, 0) or 0)
            component_budget = float(part_budget) * coef
            print(f'Компонент: {str(obj)}, бюджет: {component_budget}')
            component_budgets.append({
                'id': obj.pk,
                'name': str(obj),
                'coefficient': coef,
                'component_budget': component_budget,
            })

        import itertools

        category_ids = [
            (1, "Процессоры"),
            (2, "Видеокарты"),
            (3, "Материнские платы"),
            (4, "Оперативная память"),
            (5, "Накопители SSD"),
            # (6, "Жесткие диски"),  # Исключено
            (7, "Блоки питания"),
            (8, "Корпуса"),
            (9, "Системы охлаждения"),
        ]
#бюджет для каждой категории компонентов
        components_by_category = []
        for cat_id, cat_name in category_ids:
            info = next((c for c in component_budgets if c['id'] == cat_id), None)
            if not info:
                return Response([], status=status.HTTP_200_OK)
            comps = list(Component.objects.filter(category_id=cat_id, price__lte=info['component_budget']))
            if not comps:
                return Response([], status=status.HTTP_200_OK)
            components_by_category.append(comps)
#с этого момента начинается создание сборок
        import itertools

        builds = []
        cpu_list = components_by_category[0]
        gpu_list = components_by_category[1]
        motherboard_list = components_by_category[2]
        ram_list = components_by_category[3]  # RAM
        ssd_list = components_by_category[4]  # SSD
        other_components = components_by_category[5:]  # PSU, Case, etc.

        idx = 1
        for cpu in cpu_list:
            cpu_obj = CPU.objects.filter(component_id=cpu.id).first()
            if not cpu_obj:
                continue
            cpu_socket = cpu_obj.socket

            compatible_motherboards = [mb for mb in motherboard_list
                                       if
                                       Motherboard.objects.filter(component_id=mb.id, cpu_socket=cpu_socket).exists()]

            for gpu in gpu_list:
                for mb in compatible_motherboards:
                    mb_obj = Motherboard.objects.filter(component_id=mb.id).first()
                    if not mb_obj:
                        continue
                    ram_type = mb_obj.ram_type
                    ram_slots = mb_obj.ram_slots
                    sata_slots = mb_obj.sata_slots
                    m_2_slots = mb_obj.m_2_slots

                    # RAM
                    compatible_rams = [ram for ram in ram_list
                                       if RAM.objects.filter(component_id=ram.id, memory_type=ram_type).exists()]
                    ram_budget = next((b['component_budget'] for b in component_budgets if b['id'] == 4), None)
                    if not compatible_rams or not ram_budget:
                        continue

                    ram_combinations = []
                    for n in range(1, ram_slots + 1):
                        for comb in itertools.combinations_with_replacement(compatible_rams, n):
                            total_ram_price = sum(r.price for r in comb)
                            if total_ram_price <= ram_budget:
                                ram_combinations.append(list(comb))
                    if not ram_combinations:
                        continue

                    # SSD
                    compatible_sata_ssds = [ssd for ssd in ssd_list
                                            if SSD.objects.filter(component_id=ssd.id, ssd_type='SATA').exists()]
                    compatible_m2_ssds = [ssd for ssd in ssd_list
                                          if SSD.objects.filter(component_id=ssd.id, ssd_type='M.2').exists()]
                    ssd_budget = next((b['component_budget'] for b in component_budgets if b['id'] == 5), None)
                    if not ssd_budget:
                        continue

                    ssd_combinations = []
                    for n_sata in range(0, sata_slots + 1):
                        for sata_comb in itertools.combinations_with_replacement(compatible_sata_ssds, n_sata):
                            for n_m2 in range(0, m_2_slots + 1):
                                for m2_comb in itertools.combinations_with_replacement(compatible_m2_ssds, n_m2):
                                    ssd_comb = list(sata_comb) + list(m2_comb)
                                    if not ssd_comb:
                                        continue
                                    total_ssd_price = sum(s.price for s in ssd_comb)
                                    if total_ssd_price <= ssd_budget:
                                        ssd_combinations.append(ssd_comb)
                    if not ssd_combinations:
                        continue

                    for ram_comb in ram_combinations:
                        for ssd_comb in ssd_combinations:
                            for other_comb in itertools.product(*other_components):
                                combination = [cpu, gpu, mb] + list(ram_comb) + list(ssd_comb) + list(other_comb)
                                categories = (
                                        [category_ids[0], category_ids[1], category_ids[2]] +
                                        [category_ids[3]] * len(ram_comb) +
                                        [category_ids[4]] * len(ssd_comb) +
                                        category_ids[5:5 + len(other_components)]
                                )
                                total_price = sum(comp.price for comp in combination)
                                builds.append({
                                    'id': idx,
                                    'name': f'Сборка #{idx}',
                                    'totalPrice': total_price,
                                    'components': [
                                        {'name': str(comp), 'price': comp.price, 'category': cat_name,
                                         'country_of_origin': comp.country_of_origin}
                                        for comp, (_, cat_name) in zip(combination, categories)
                                    ]
                                })
                                idx += 1
                                if idx > 20:
                                    break
                            if idx > 20:
                                break
                        if idx > 20:
                            break
                    if idx > 20:
                        break
                if idx > 20:
                    break
            if idx > 20:
                break
#закомментила создание сборок, здесь просто генератор(без учета совместимости)
        '''builds = []
        for idx, combination in enumerate(itertools.islice(itertools.product(*components_by_category), 20), 1):
            total_price = sum(comp.price for comp in combination)

            builds.append({
                'id': idx,
                'name': f'Сборка #{idx}',
                'totalPrice': total_price,
                'components': [
                    {'name': str(comp), 'price': comp.price, 'category': cat_name, 'country_of_origin': comp.country_of_origin}
                    for comp, (_, cat_name) in zip(combination, category_ids)

                ]
            })
            print(f'Сборка #{idx} , {total_price}')

        print(f'Сборки: {builds}')'''
        print(f'Сборки: {components_by_category}')

        return Response(builds, status=status.HTTP_200_OK)


class ComponentCategoryViewSet(viewsets.ModelViewSet):
    queryset = ComponentCategory.objects.all()
    serializer_class = ComponentCategorySerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = ComponentCategoryBulkSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = ManufacturerBulkSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class ManufacturerBulkViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerBulkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class RAMViewSet(viewsets.ModelViewSet):
    queryset = RAM.objects.all()
    serializer_class = RAMSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class MotherboardViewSet(viewsets.ModelViewSet):
    queryset = Motherboard.objects.all()
    serializer_class = MotherboardSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class SSDViewSet(viewsets.ModelViewSet):
    queryset = SSD.objects.all()
    serializer_class = SSDSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class HDDViewSet(viewsets.ModelViewSet):
    queryset = HDD.objects.all()
    serializer_class = HDDSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class PSUViewSet(viewsets.ModelViewSet):
    queryset = PSU.objects.all()
    serializer_class = PSUSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component
            instance.delete()
            component.delete()

class IncompatibleComponentsViewSet(viewsets.ModelViewSet):
    queryset = IncompatibleComponents.objects.all()
    serializer_class = IncompatibleComponentsSerializer

class PCCaseViewSet(viewsets.ModelViewSet):
    queryset = PCCase.objects.all()
    serializer_class = PCCaseSerializer