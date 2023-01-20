# С&P problem, nesting, dxf, gcode

## 1. Алгоритм для решения задачи упаковки полигонов в рабочей области 
![Packing.png](screenshots%2FPacking.png)

## 2. Преобразование координат в набор инструкций языка *gcode*
![gcode.png](screenshots%2Fgcode.png)

### *Дополнительная информация*
1. Оригинальный [репозиторий](https://github.com/liangxuCHEN/no_fit_polygon) с алгоритмом
2. Переписан и проверен на Python 3.10.4 
3. Работает с файлами формата *dxf* (с объектами LINE и SPLINE(с интерполяцией)). Примеры файлов находятся в [input_data](input_data)
4. Основной файл  **[test_nfp.py](test_nfp.py)**
5. Настройка алгоритма через **[settings.py](settings.py)**


