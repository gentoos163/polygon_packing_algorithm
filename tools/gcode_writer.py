from decimal import Decimal, ROUND_FLOOR


def coordinates_to_gcode(coordinates: list) -> str:
    if not len(coordinates):
        return ''

    gcode = '''G90G17G21
    M06 T3
    S1
    G00 Z10.000 F15000'''.replace('    ', '')

    coordinates_length = len(coordinates)
    fisrt = True
    for i in range(coordinates_length):
        shape = coordinates[i]
        skip = 0
        if fisrt:
            skip = 2
            fisrt = False
            gcode = add_offset_points(gcode, pos1=shape[0], pos2=shape[1])
        shape_length = len(shape)
        fisrt_point = None
        for j in range(shape_length):
            if j == 0:
                fisrt_point = shape[j]
            if skip > 0:
                skip -= 1
                continue
            point = shape[j]
            if j < shape_length - 1:
                gcode = add_intermediate_point(gcode, x=point[0], y=point[1])
            elif j == shape_length - 1 and i < coordinates_length - 1:
                gcode = add_intermediate_point(gcode, x=point[0], y=point[1])
                gcode = add_intermediate_point(gcode, x=fisrt_point[0], y=fisrt_point[1])
                gcode = add_lifting_point(gcode, x=fisrt_point[0], y=fisrt_point[1])
                gcode = add_offset_points(gcode, pos1=coordinates[i + 1][0], pos2=coordinates[i + 1][1])
                skip = 2
            else:
                gcode = add_intermediate_point(gcode, x=point[0], y=point[1])
                gcode = add_intermediate_point(gcode, x=fisrt_point[0], y=fisrt_point[1])
                gcode = add_last_point(gcode, x=fisrt_point[0], y=fisrt_point[1])

    gcode += '\nM30'

    return gcode


def add_intermediate_point(gcode: str, x: float, y: float):
    gcode += f'\nG01 X{round_coordinate(x)} Y{round_coordinate(y)} Z-11.000'
    return gcode


def add_lifting_point(gcode: str, x: float, y: float):
    gcode += f'\nG00 X{round_coordinate(x)} Y{round_coordinate(y)} Z10.000 F15000 '
    return gcode


def add_offset_points(gcode: str, pos1: tuple, pos2: tuple):
    pos1_x = round_coordinate(pos1[0])
    pos1_y = round_coordinate(pos1[1])
    pos2_x = round_coordinate(pos2[0])
    pos2_y = round_coordinate(pos2[1])
    gcode += f'''
    G00 X{pos1_x} Y{pos1_y} Z10.000
    G00 X{pos1_x} Y{pos1_y} Z3.000
    G01 X{pos1_x} Y{pos1_y} Z-11.000 F3000
    G01 X{pos2_x} Y{pos2_y} Z-11.000 F12000'''.replace('    ', '')
    return gcode


def add_last_point(gcode: str, x: float, y: float):
    gcode += f'\nG00 X{round_coordinate(x)} Y{round_coordinate(y)} Z10.000 F15000'
    return gcode


def round_coordinate(i) -> float:
    number = Decimal(i)
    return number.quantize(Decimal("1.000"), ROUND_FLOOR)



