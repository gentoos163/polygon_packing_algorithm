# С&P problem, nesting, dxf, gcode

## 1. Алгоритм для решения задачи упаковки полигонов в рабочей области 
![packing2](https://user-images.githubusercontent.com/45397736/214505413-c7065105-1907-4d02-9b4d-da061f60474a.png)

## 2. Преобразование координат в набор инструкций языка *gcode*
![gcode2](https://user-images.githubusercontent.com/45397736/214505419-2f6ddbdd-5021-41c8-9fd5-9b735dbeb6b1.png)

### *Дополнительная информация*
1. Оригинальный [репозиторий](https://github.com/liangxuCHEN/no_fit_polygon) с алгоритмом
2. Переписан и проверен на Python 3.10.4 
3. Работает с файлами формата *dxf* (с объектами LINE и SPLINE(с интерполяцией)). Примеры файлов находятся в [input_data](input_data)
4. Основной файл  **[test_nfp.py](test_nfp.py)**
5. Настройка алгоритма через **[settings.py](settings.py)**


