version = [
1, 2, 3, 4,
5, 6, 7, 8,
9, 10, 11, 12,
13, 14, 15, 16,
17, 18, 19, 20,
21, 22, 23, 24,
25, 26, 27, 28,
29, 30, 31, 32,
33, 34, 35, 36,
37, 38, 39, 40
]

tam_fragmento = [
5, 9, 15, 23,
31, 40, 46, 57,
69, 81, 96, 110,
127, 137, 156, 176,
193, 215, 237, 257,
279, 301, 327, 351,
382, 410, 439, 458,
488, 519, 552, 585,
620, 656, 691, 729,
769, 809, 842, 886
]

box_size = [
15, 15, 14, 14,
13, 13, 12, 12,
11, 11, 10, 10,
9, 9, 8, 8,
8, 8, 7, 7,
6, 6, 5, 5,
5, 5, 5, 5,
5, 5, 5, 5,
4, 4, 4, 4,
4, 4, 4, 4
]

byte_size = [
17, 32, 53, 78,
106, 134, 154, 192,
230, 271, 321, 367,
425, 458, 520, 586,
644, 718, 792, 858,
929, 1003, 1091, 1171,
1273, 1367, 1465, 1528,
1628, 1732, 1840, 1952,
2068, 2188, 2303, 2431,
2563, 2699, 2809, 2953
]

diccionario_fragmentos = dict(zip(version, tam_fragmento))
diccionario_box_size = dict(zip(version, box_size))
diccionario_byte_size = dict(zip(version, byte_size))