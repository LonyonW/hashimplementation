import time
import os
import hashlib

def pad_block(block, block_size=512):
    """
    Aplica padding a un bloque para que tenga exactamente 512 bits. (Inspirado en el ejmplo de la clase H1padding.py)
    """
    block_bits = ''.join(f'{byte:08b}' for byte in block)  # Convertir bytes a bits
    original_length = len(block_bits)

    # Añadir bit '1'
    block_bits += '1'

    # Añadir ceros hasta que la longitud sea congruente a (block_size - 64)
    while (len(block_bits) + 64) % block_size != 0:
        block_bits += '0'

    # Añadir la longitud original en 64 bits
    block_bits += f'{original_length:064b}'

    # Convertir de vuelta a bytes (512 bits = 64 bytes)
    padded_block = bytearray()
    for i in range(0, len(block_bits), 8):
        byte = int(block_bits[i:i+8], 2)
        padded_block.append(byte)
    
    return bytes(padded_block)

def custom_hash_function(block, chaining_value):
    """
    Función de hash propia que procesa un bloque de 512 bits y un chaining value de 256 bits.
    Devuelve un nuevo chaining value de 256 bits.
    
    Diseño:
    - Nueva division de bloque en 4 partes de 128 bits.
    - Aplica rotaciones, XOR, y sumas módulo 2^64 a cada parte.
    - Combina con el chaining value (256 bits) dividido en 4 partes de 64 bits.
    - Usa una transformación no lineal para mezclar los resultados.
    """
    # División del bloque
    # Dividir el bloque en 4 partes de 128 bits o 16 bytes
    part_size = 16  
    parts = [int.from_bytes(block[i:i+part_size], byteorder='big') for i in range(0, 64, part_size)]

    # División del chaining value
    # Dividir el chaining value (256 bits) en 4 partes de 64 bits
    cv_parts = [
        (chaining_value >> 192) & 0xFFFFFFFFFFFFFFFF,
        (chaining_value >> 128) & 0xFFFFFFFFFFFFFFFF,
        (chaining_value >> 64) & 0xFFFFFFFFFFFFFFFF,
        chaining_value & 0xFFFFFFFFFFFFFFFF
    ]

    # Transformaciones
    # Procesar cada parte con rotaciones y operaciones bit a bit
    new_cv_parts = []
    for i in range(4):
        # Rotaciones (rotar a la izquierda)
        rotated = ((parts[i] << 3) | (parts[i] >> (128 - 3))) & ((1 << 128) - 1)
        
        # Combinar con el chaining value usando XOR y suma módulo 2^64
        part_lower = rotated & 0xFFFFFFFFFFFFFFFF  # Lower 64 bits
        part_upper = (rotated >> 64) & 0xFFFFFFFFFFFFFFFF  # Upper 64 bits
        
        # Mezclar con el chaining value
        mixed_lower = (part_lower ^ cv_parts[i]) & 0xFFFFFFFFFFFFFFFF
        mixed_upper = (part_upper + cv_parts[(i+1) % 4]) & 0xFFFFFFFFFFFFFFFF
        
        # Transformación no lineal: usar una operación cuadrática simple
        mixed = ((mixed_lower * mixed_lower) ^ mixed_upper) & 0xFFFFFFFFFFFFFFFF
        new_cv_parts.append(mixed)

    # Combinar las partes en un nuevo chaining value de 256 bits
    new_chaining_value = (
        (new_cv_parts[0] << 192) |
        (new_cv_parts[1] << 128) |
        (new_cv_parts[2] << 64) |
        new_cv_parts[3]
    ) & ((1 << 256) - 1)

    return new_chaining_value

def hash_file_by_blocks(file_path):
    """
    Calcula el hash de un archivo procesándolo en bloques de 512 bits usando una función hash propia.
    """
    block_size_bits = 512
    block_size_bytes = block_size_bits // 8  # 64 bytes

    # generar chaining value inicial de 256 bits
    # chaining_value = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
    chaining_value = generate_mathematical_chaining_value()
    # chaining_value = generate_chaining_value_with_seed(verbose=True)
    print(f"chaining_value   = 0x{chaining_value:064x}") # mostrar en hexadecimal

    # para medir tiempo
    start_time = time.time()

    # Abrir el archivo y procesar en bloques
    with open(file_path, 'rb') as file:
        while True:
            block = file.read(block_size_bytes)  # Lee bloques de 64 bytes o 512 bits
            if not block:  # Fin del archivo
                break

            # Si el bloque es menor a 512 bits, usar función para aplicar padding
            if len(block) < block_size_bytes:
                block = pad_block(block, block_size=block_size_bits)
            
            # Comprimir el bloque con el chaining value usando la función hash propia
            chaining_value = custom_hash_function(block, chaining_value)

    # Convertir el chaining value final a hexadecimal (256 bits = 64 caracteres hex)
    final_hash = f'{chaining_value:064x}'

    # Calcular tiempo
    elapsed_time = time.time() - start_time

    return final_hash, elapsed_time

# generar un valor de chaining_value usando constantes matematicas
def generate_mathematical_chaining_value():
    """Genera chaining_value usando constantes matemáticas"""
    # primeros 50 dígitos de π, e, φ
    pi_digits = "31415926535897932384626433832795028841971693993751"
    e_digits = "27182818284590452353602874713526624977572470936999"
    phi_digits = "16180339887498948482045868343656381177203091798057"
    
    combined = pi_digits + e_digits + phi_digits
    hash_result = hashlib.sha256(combined.encode()).hexdigest() # uso de hashlib
    
    return int(hash_result, 16)

def generate_chaining_value_with_seed(verbose=True):
    # Generar hash de la semilla
    seed="euler_constant_gamma_plus_golden_ratio_phi"
    hash_result = hashlib.sha256(seed.encode()).hexdigest()
    chaining_value = int(hash_result, 16)
    
    if verbose:
        # Verificar letras presentes
        letters_present = [c for c in hash_result if c in 'abcdef']
        
        print(f"Semilla utilizada: {seed}")
        print(f"Hash: {hash_result}")
        print(f"chaining_value = 0x{chaining_value:064x}")
        print(f"Letras presentes: {letters_present}")
        print(f"Cantidad de letras: {len(letters_present)}")
    
    return chaining_value

def main():
    # Ruta del archivo a procesar
    file_path = "large_test_file.txt"
    # file_path = "largest_file.mov"
    # file_path = "ubuntu-24.04.2-desktop-amd64.iso"

    # Verificar tamaño del archivo
    file_size = os.path.getsize(file_path)
    print(f"Tamaño del archivo: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")

    if file_size < 1024 * 1024:  # 1 MB
        print("Advertencia: El archivo es menor a 1 MB. El algoritmo está diseñado para archivos más grandes.")
    
    # Calcular hash
    final_hash, elapsed_time = hash_file_by_blocks(file_path)

    # Mostrar resultados
    print("\nResultados:")
    print(f"Hash final (256 bits): {final_hash}")
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")

if __name__ == "__main__":
    main()