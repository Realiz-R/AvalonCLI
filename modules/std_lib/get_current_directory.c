#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h> // Для Windows
#else
#include <unistd.h>  // Для Unix-систем (Linux, macOS)
#endif

// Функция для получения текущей директории
void get_current_directory(char* buffer, size_t size) {
    if (buffer == NULL || size == 0) {
        fprintf(stderr, "Ошибка: неверные параметры буфера.\n");
        buffer[0] = '\0'; // Возвращаем пустую строку
        return;
    }

#ifdef _WIN32
    // Для Windows
    DWORD result = GetCurrentDirectory(size, buffer);
    if (result == 0) {
        fprintf(stderr, "Ошибка получения текущей директории: %lu\n", GetLastError());
        buffer[0] = '\0'; // Возвращаем пустую строку
    } else if (result > size) {
        fprintf(stderr, "Ошибка: буфер слишком мал для текущей директории.\n");
        buffer[0] = '\0'; // Возвращаем пустую строку
    }
#else
    // Для Unix-систем
    if (getcwd(buffer, size) == NULL) {
        fprintf(stderr, "Ошибка получения текущей директории: %s\n", strerror(errno));
        buffer[0] = '\0'; // Возвращаем пустую строку
    }
#endif
}