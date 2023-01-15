# -*- coding: utf-8 -*-
from nfp_function import Nester, content_loop_rate, set_target_loop, get_polygon_coordinates, get_result_npf
from tools import input_utls
from settings import BIN_WIDTH, BIN_NORMAL, BIN_CUT_BIG
import turtle as t
from gcode_writer import coordinates_to_gcode, save_to_txt


def visualize_shape_points(dxfProjectFilesData: list):
    window = t.Screen()
    window.setup(600, 1000)

    for odbData in dxfProjectFilesData:
        _x, _y = odbData[0]
        t.up()
        t.goto(x=_x, y=_y)
        t.down()
        for x, y in odbData:
            t.goto(x=x, y=y)
    
    t.exitonclick()


if __name__ == '__main__':
    n = Nester()
    dxfProjectFiles = [
        'art1045_1_LApa.dxf',
        'art1045_3_L.dxf',
        'art1045_1_LApa.dxf',
        'art1045_1_LApa.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf',
        #'E5.dxf',
        #'T9.dxf'
    ]
    for file in dxfProjectFiles:
        s = input_utls.input_polygon(f'input_data/{file}')
        n.add_objects(s)

    if n.shapes_max_length > BIN_WIDTH:
        BIN_NORMAL[2][0] = n.shapes_max_length
        BIN_NORMAL[3][0] = n.shapes_max_length

    # выброть область
    n.add_container(BIN_NORMAL)
    # выполнить расчет
    n.run()
    n.show_result()

    # расчетное выходное условие
    res_list = list()
    best = n.best

    polygons = get_result_npf(best['placements'], n.shapes)
    # получаем коондинаты из результата работы алгоритма
    shape_coordinates = get_polygon_coordinates(polygons)
    print('\n')
    print(shape_coordinates)

    # vizualizeShapePoinst(shape_coordinates)
    # конвертируем координаты в формат gcode
    txt = coordinates_to_gcode(shape_coordinates)
    print(txt)
    save_to_txt(txt)
    
    # помещается в контейнер
    #set_target_loop(best, n)    # T6

    # Вывод результата в графическом окне
    # Цикл определенное количество раз
    # content_loop_rate(best, n, loop_time=1)   # T7 , T4



