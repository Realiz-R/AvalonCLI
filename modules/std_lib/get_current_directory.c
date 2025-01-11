#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char* get_current_directory() {
    // Выделяем начальный буфер
    size_t size = 1024; // Начальный размер буфера
    char* buffer = malloc(size);
    if (buffer == NULL) {
        perror("Ошибка выделения памяти");
        return NULL; // Возвращаем NULL в случае ошибки выделения памяти
    }

    // Получаем текущую директорию
    char* result = getcwd(buffer, size);
    while (result == NULL) {
        // Если буфер недостаточен, увеличиваем его размер
        size *= 2; // Увеличиваем размер буфера
        char* new_buffer = realloc(buffer, size);
        if (new_buffer == NULL) {
            perror("Ошибка перераспределения памяти");
            free(buffer);
            return NULL; // Возвращаем NULL в случае ошибки
        }
        buffer = new_buffer;
        result = getcwd(buffer, size); // Пытаемся снова получить текущую директорию
    }

    return buffer; // Возвращаем указатель на динамически выделенный буфер
}

// Пример использования функции
int main() {
    char* current_dir = get_current_directory();
    if (current_dir) {
        printf("Текущая директория: %s\n", current_dir);
        free(current_dir); // Освобождаем выделенную память после использования
    } else {
        printf("Не удалось получить текущую директорию.\n");
    }
    return 0;
}


