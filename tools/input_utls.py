# coding=utf8
import dxfgrabber
from settings import COUNTOUR_SCALING


def find_shape_from_dxf(file_name):
    """
    读取DXF文档，从LINE里面找出多边形
    :param file_name: 文档路径
    :return:
    """
    dxf = dxfgrabber.readfile(file_name)
    all_shapes = list()
    new_polygon = dict()
    for e in dxf.entities:
        if e.dxftype == 'LINE':
            # print (e.start, e.end)
            # Находим замкнутые полигоны
            # Линии рисуются не по порядку
            end_key = '{}x{}'.format(e.end[0], e.end[1])
            start_key = '{}x{}'.format(e.start[0], e.start[1])
            if end_key in new_polygon:
                # Найти замкнутый многоугольник
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
                if points[-1][0] == e.start[0] and points[-1][1] == e.start[1]:
                    new_polygon[key].append([e.end[0], e.end[1]])
                    has_find = True
                    break
                if points[-1][0] == e.end[0] and points[-1][1] == e.end[1]:
                    new_polygon[key].append([e.start[0], e.start[1]])
                    has_find = True
                    break

            if not has_find:
                new_polygon['{}x{}'.format(
                    e.start[0], e.start[1])] = [[e.start[0], e.start[1]], [e.end[0], e.end[1]]]
        elif e.dxftype == 'SPLINE':
            # pom+
            spline_polygon = []
            for x, y, _ in e.control_points: ######## ПРОВЕРИТЬ КОЛИЧЕСТВО ТОЧЕК
                spline_polygon.append([x*COUNTOUR_SCALING, y*COUNTOUR_SCALING])    
            all_shapes.append(spline_polygon)
            # pom-

    return all_shapes


def input_polygon(dxf_file):
    """
    :param dxf_file: 文件地址
    :param is_class: 返回Polygon 类，或者通用的 list
    :return:
    """
    # 从dxf文件中提取数据
    datas = find_shape_from_dxf(dxf_file)
    shapes = list()

    for i in range(0, len(datas)):
        shapes.append(datas[i])

    print(shapes)
    return shapes


if __name__ == '__main__':
    s = find_shape_from_dxf('/input_data/T9.dxf')
    print(s)
    print(len(s))
