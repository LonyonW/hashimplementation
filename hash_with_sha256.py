import hashlib
import time
import os

def calculate_sha256_hash(file_path):
    """
    Calcula el hash SHA-256 de un archivo procesándolo en bloques.
    
    Parámetros:
    - file_path (str): Ruta del archivo a hashear
    
    Retorna:
    - hash_result (str): Hash SHA-256 en formato hexadecimal
    - elapsed_time (float): Tiempo de ejecución en segundos
    """
    # Tamaño del bloque para leer el archivo (ajustable, 64 KB es eficiente)
    block_size = 64 * 1024  # 64 KB
    
    # Crear un objeto hash SHA-256
    hasher = hashlib.sha256()
    
    # Medir tiempo
    start_time = time.time()
    
    # Abrir el archivo en modo binario y procesar en bloques
    with open(file_path, 'rb') as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            hasher.update(block)  # Actualizar el hash con el bloque
    
    # Calcular el hash final y el tiempo
    hash_result = hasher.hexdigest()
    elapsed_time = time.time() - start_time
    
    return hash_result, elapsed_time

def main():
    # Ruta del archivo a procesar
    file_path = "large_test_file.txt"  
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe.")
        return
    
    # Verificar tamaño del archivo
    file_size = os.path.getsize(file_path)
    print(f"Tamaño del archivo: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")
    
    # Calcular el hash
    hash_result, elapsed_time = calculate_sha256_hash(file_path)
    
    # Mostrar resultados
    print("\nResultados:")
    print(f"Hash SHA-256: {hash_result}")
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")

if __name__ == "__main__":
    main()