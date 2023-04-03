# -*- coding: utf-8 -*-
from nesting import get_polygons_nested_gcode
from time import perf_counter


def check_time(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        func(*args, **kwargs)
        print(f'time: {(perf_counter() - start):.02f}')
    return wrapper


@check_time
def main():
    dxf_project_files = [
        # '50x30.dxf',
        # 'art1045_1_LApa.dxf',
        # 'art1045_1_LApa.dxf',
        # 'art1045_1_LApa.dxf',
        # 'art1045_3_L.dxf',
        # 'art1045_3_L.dxf',
        # 'art1045_3_L.dxf',
        # 'art1045_3_L.dxf',
        # 'art1045_3_L.dxf',
        # 'test/66_50x30.dxf',
        'test/1_art-3876_1_lapa.dxf',
        'test/1_art-3876_2.dxf',
        'test/2_art-3876_5.dxf',
        'test/1_art-3876_5.dxf',
        #
        'test/1_art-3876_1_lapa.dxf',
        'test/1_art-3876_2.dxf',
        'test/2_art-3876_5.dxf',
        'test/1_art-3876_5.dxf',


        # 'test/2_art-3876_1_lapa.dxf',
        # 'test/2_art-3876_2.dxf',
        # 'test/2_art-3876_5.dxf',
        # 'test/2_art-3876_5.dxf',
        # 'E5.dxf',
        # 'T9.dxf'
    ]

    get_polygons_nested_gcode(dxf_project_files)


if __name__ == '__main__':
    main()


