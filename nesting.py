from tools.nfp_function import Nester
from tools import input_utls
from settings import BIN_WIDTH, BIN_NORMAL, SPLIT_SPLINES
from tools.gcode_writer import coordinates_to_gcode


def get_polygons_nested_gcode(dxf_project_files):
    gcode = ''
    shapes = []
    for file in dxf_project_files:
        ss = input_utls.input_polygon(f'input_data/{file}')
        for shape in ss:
            shapes.append(shape)
    if not len(shapes):
        return None

    n = Nester()
    n.add_objects(shapes)

    # if n.shapes_max_length > BIN_WIDTH:
    #     BIN_NORMAL[2][0] = n.shapes_max_length
    #     BIN_NORMAL[3][0] = n.shapes_max_length

    # выбрать область
    n.add_container(BIN_NORMAL)
    # выполнить расчет
    n.run()
    # показать результат нестинга
    n.show_result()

    # получаем коондинаты из результата работы алгоритма
    shape_coordinates = n.get_polygon_coordinates()

    if not SPLIT_SPLINES:
        shape_coordinates = input_utls.find_flags_and_break_shapes(shape_coordinates)

    # конвертируем координаты в формат gcode
    gcode = coordinates_to_gcode(shape_coordinates)
    save_to_txt(gcode)

    return gcode


def save_to_txt(text: str) -> str:
    with open("output_data/res.txt", "w") as file:
        file.write(text)
