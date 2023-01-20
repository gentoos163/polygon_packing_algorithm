# coding=utf8
from settings import COUNTOUR_SCALING, SIMPLIFYING_POLYGONS
import ezdxf as ez


def find_shape_from_dxf(file_name):
    """
    Чтение документа DXF и получение координатов объектов LINE и SPLINE
    :param file_name: 文档路径
    :return:
    """
    dxf = ez.readfile(file_name)
    all_shapes = list()
    new_polygon = dict()
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
                    points[0] = points[0] * COUNTOUR_SCALING
                    points[1] = points[1] * COUNTOUR_SCALING
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
            spline_polygon = []
            if SIMPLIFYING_POLYGONS:
                for x, y, _ in e.control_points:
                    spline_polygon.append([x * COUNTOUR_SCALING, y * COUNTOUR_SCALING])
            else:
                bspline = e.construction_tool()
                xy_pts = [p.xy for p in bspline.flattening(distance=1, segments=20)]
                for x, y, _ in xy_pts:
                    spline_polygon.append([x * COUNTOUR_SCALING, y * COUNTOUR_SCALING])

            all_shapes.append(spline_polygon)
    return all_shapes


def input_polygon(dxf_file):
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
