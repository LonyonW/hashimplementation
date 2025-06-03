Requisitos

Python 3.x
Módulos: time, os, hashlib (incluidos en la biblioteca estándar de Python)


Uso


Asegúrate de tener un archivo de prueba (por ejemplo, large_test_file.txt) en el directorio del proyecto. O usar un archivo existente mayor a 1 MB.

Modifica la variable file_path en la función main() si deseas usar otro archivo.

Ejecuta el script:

python implemented_hash.py




El programa mostrará:

Tamaño del archivo.
Chaining value inicial en formato hexadecimal.
Hash final (256 bits).
Tiempo de ejecución.




Estructura del Código


pad_block: Aplica padding a los bloques para alcanzar 512 bits, inspirado en H1padding.py.

custom_hash_function: Implementa una función de hash propia con rotaciones, XOR, y transformaciones no lineales.

hash_file_by_blocks: Procesa el archivo en bloques y calcula el hash final.

generate_mathematical_chaining_value: Genera un chaining value inicial usando los primeros 50 dígitos de π, e, y φ con SHA-256.

generate_chaining_value_with_seed: Genera un chaining
