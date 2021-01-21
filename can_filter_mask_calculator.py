# Script para cálculo do filter e mask da CAN dado um vetor de IDs que devem passar
import operator
from functools import reduce


def can_bus_filter_mask(can_bus_ids, quiet=True):
    print('[{}]'.format(', '.join([hex(x).upper() for x in can_bus_ids])))

    # Calculo do FILTER e da MASK
    can_bus_filter = reduce(operator.and_, can_bus_ids)
    can_bus_mask = operator.xor(reduce(operator.or_, can_bus_ids), can_bus_filter)

    if reduce(operator.or_, can_bus_ids) > 0x7FF:  # Verifica se utiliza extended ID
        can_bus_mask ^= 0x1FFFFFFF  # 29 bits
    else:
        can_bus_mask ^= 0x7FF  # 11 bits

    # Verifica se todos os ids de interesse passam pela mask e filter projetados
    for can_bus_id in can_bus_ids:
        assert can_bus_id & can_bus_mask == can_bus_filter, 'Error: 0x{:03X}'.format(can_bus_id)

    print('Filter: 0x{:03X}'.format(can_bus_filter))
    print('Mask: 0x{:03X}'.format(can_bus_mask))

    if can_bus_filter <= 0x7FF:
        can_bus_received_id_count = 0
        for can_bus_id in range(0, 0x7FF + 1):
            if can_bus_id & can_bus_mask == can_bus_filter:
                can_bus_received_id_count += 1
                print('ID: 0x{:03X} will be received'.format(can_bus_id))
        print('{} ID\'s will be received\n'.format(can_bus_received_id_count))
    else:  # Extendido fica muito longo, então printa os que não irão passar
        for can_bus_id in can_bus_ids:
            if can_bus_id & can_bus_mask != can_bus_filter:
                print('ID: 0x{:03X} will NOT be received'.format(can_bus_id))

    return can_bus_filter, can_bus_mask


# Vetor com os IDs que devem passar pelo filtro
used_ids = [[0x11] + [0x55] + [0x15]]

for ids in used_ids:
    can_bus_filter_mask(ids, False)

