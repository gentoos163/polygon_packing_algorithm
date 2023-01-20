# -*- coding: utf-8 -*-
from nesting import get_polygons_nested_gcode
import time


if __name__ == '__main__':
    start = time.time()
    dxf_project_files = [
        'art1045_1_LApa.dxf',
        'art1045_1_LApa.dxf',
        'art1045_1_LApa.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf',
        'art1045_3_L.dxf'
        # 'E5.dxf',
        # 'T9.dxf'
    ]

    get_polygons_nested_gcode(dxf_project_files)

    end = time.time()

    print('Running time: %s Seconds' % (end - start))
    print('Running time: %s Minuts' % ((end - start) / 60))

