import lief

# Загружаем EXE файл
binary = lief.parse(r"C:\Program Files\DAEMON Tools Ultra\Extractor.exe")


# Проверяем наличие защитных механизмов
def check_security(binary):
    if binary.has_segment(".text"):
        print("Segment .text found, checking for executable code...")
    else:
        print("No executable code segment found.")
    
    # Проверка наличия ASLR (Address Space Layout Randomization)
    if binary.has_dynamic_entry(lief.ELF.DYNAMIC_TAGS.PIE):
        print("Position Independent Executable (PIE) detected.")
    else:
        print("No PIE detected.")
        
    # Проверка на наличие переполнения буфера
    # (например, поиск функции strcpy, которая может вызвать переполнение буфера)
    for function in binary.functions:
        if "strcpy" in function.name:
            print(f"Warning: Potential buffer overflow in function: {function.name}")
            
check_security(binary)
