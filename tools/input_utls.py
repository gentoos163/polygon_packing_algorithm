# coding=utf8
from settings import CONTOUR_SCALING, SIMPLIFYING_POLYGONS, SPLIT_SPLINES
import ezdxf as ez
import numpy as np

def find_shape_from_dxf(file_name):
    """
    Чтение документа DXF и получение координатов объектов LINE и SPLINE
    :param file_name: 文档路径
    :return:
    """
    dxf = ez.readfile(file_name)
    all_shapes = list()
    new_polygon = dict()
    spline_polygon = []
    first_spline = True
    """
    В моей задаче в файлах могут быть совмещенные контуры, т.е. автомобильные 
    коврики и в них отверстия под люверсы.
    Поэтому было решено разделить коврики на отдельные файлы. Но осталась проблема с люверсами.
    Для ее решения я точки координат коврика и люверсов представляю одним контуром,
    но в начало люверсов помещаю задваивание начальной позиции, чтобы после размещения найти их
    и разделить на отдельные контуры.
    """
    for e in dxf.entities:
        if e.dxftype() == 'LINE':
            # print (e.start, e.end)
            # Находим замкнутые полигоны
            # Линии рисуются не по порядку
            end_key = '{}x{}'.format(e.dxf.end[0], e.dxf.end[1])
            start_key = '{}x{}'.format(e.dxf.start[0], e.dxf.start[1])
            if end_key in new_polygon:
                # Найти замкнутый многоугольник
                for points in new_polygon[end_key]:
                    points[0], points[1] = scaling_coordinates(x=points[0], y=points[1])
                all_shapes.append(new_polygon[end_key])
                new_polygon.pop(end_key)
                continue

            # Преобразование начальной и конечной точки
            if start_key in new_polygon:
                # Найти замкнутый многоугольник
                all_shapes.append(new_polygon[start_key])
                new_polygon.pop(start_key)
                continue

            # Найти точки соединения
            has_find = False
            for key, points in new_polygon.items():
                if points[-1][0] == e.dxf.start[0] and points[-1][1] == e.dxf.start[1]:
                    new_polygon[key].append([e.dxf.end[0], e.dxf.end[1]])
                    has_find = True
                    break
                if points[-1][0] == e.dxf.end[0] and points[-1][1] == e.dxf.end[1]:
                    new_polygon[key].append([e.dxf.start[0], e.dxf.start[1]])
                    has_find = True
                    break

            if not has_find:
                new_polygon['{}x{}'.format(
                    e.dxf.start[0], e.dxf.start[1])] = [[e.dxf.start[0], e.dxf.start[1]], [e.dxf.end[0], e.dxf.end[1]]]

        elif e.dxftype() == 'SPLINE':
            if SPLIT_SPLINES:
                spline_polygon = []
            first_spline_points = True
            # if SIMPLIFYING_POLYGONS:
            #     for x, y, _ in e.control_points:
            #         if not SPLIT_SPLINES:
            #             add_spline_dots_flag(first_spline, first_spline_points, [x, y], spline_polygon)
            #         first_spline_points = False
            #         spline_polygon.append(scaling_coordinates(x=x, y=y))
            # else:
            bspline = e.construction_tool()
            xy_pts = [p.xy for p in bspline.flattening(distance=1, segments=30)]  # 1 - 20
            for x, y, _ in xy_pts:
                if not SPLIT_SPLINES:
                    add_spline_dots_flag(first_spline, first_spline_points, [x, y], spline_polygon)
                first_spline_points = False
                spline_polygon.append(scaling_coordinates(x=x, y=y))
            first_spline = False
            if SPLIT_SPLINES:
                all_shapes.append(spline_polygon)
        elif e.dxftype() == 'LWPOLYLINE':
            if SPLIT_SPLINES:
                spline_polygon = []
            first_spline_points = True
            xy_pts = e.get_points(format='xy')
            for x, y in xy_pts:
                if not SPLIT_SPLINES:
                    add_spline_dots_flag(first_spline, first_spline_points, [x, y], spline_polygon)
                first_spline_points = False
                spline_polygon.append(scaling_coordinates(x=x, y=y))
            first_spline = False
            if SPLIT_SPLINES:
                all_shapes.append(spline_polygon)

        elif e.dxftype() == 'POLYLINE':
            if SPLIT_SPLINES:
                spline_polygon = []
            first_spline_points = True
            for x, y, _ in e.points():
                if not SPLIT_SPLINES:
                    add_spline_dots_flag(first_spline, first_spline_points, [x, y], spline_polygon)
                first_spline_points = False
                spline_polygon.append(scaling_coordinates(x=x, y=y))
            first_spline = False
            if SPLIT_SPLINES:
                all_shapes.append(spline_polygon)
    if not SPLIT_SPLINES and len(spline_polygon):
        all_shapes.append(spline_polygon)
    return all_shapes


def scaling_coordinates(x, y) -> list:
    return [x * CONTOUR_SCALING, y * CONTOUR_SCALING]


def add_spline_dots_flag(first_spline: bool, first_spline_points: bool, points: list, spline_polygon: list):
    if first_spline or not first_spline_points:
        return
    x = points[0]
    y = points[1]
    spline_polygon.append(scaling_coordinates(x=x, y=y))
    spline_polygon.append(scaling_coordinates(x=x, y=y))
    spline_polygon.append(scaling_coordinates(x=x, y=y))


def find_flags_and_break_shapes(shapes: list) -> list:
    new_shapes = []
    for i, shape_points in enumerate(shapes):
        shape_points_length = len(shape_points)
        new_shape_points = []
        skip = 0
        for j, shape_point in enumerate(shape_points):
            if skip > 0:
                skip -= 1
                continue
            x, y = shape_point
            if j < shape_points_length-5 and \
                    shape_points[j+1][0] == x and \
                    shape_points[j+1][1] == y and \
                    shape_points[j+2][0] == x and \
                    shape_points[j+2][1] == y and \
                    shape_points[j+3][0] == x and \
                    shape_points[j+3][1] == y:
                new_shapes.append(new_shape_points)
                new_shape_points = []
                skip = 3
                continue
            new_shape_points.append((x, y))
        new_shapes.append(new_shape_points)

    return new_shapes


def input_polygon(dxf_file) -> list:
    """
    :param dxf_file: путь к файлу
    :return:
    """
    # извлечь данные из файла dxf
    datas = find_shape_from_dxf(dxf_file)

    shapes = list()

    for i in range(0, len(datas)):
        shapes.append(datas[i])

    # print(shapes)
    return shapes


if __name__ == '__main__':
    s = find_shape_from_dxf('/input_data/T9.dxf')
    print(s)
    print(len(s))
