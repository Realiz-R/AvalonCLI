#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>  // Для работы с errno

// Смена директории
int change_directory(const char* path) {
    if (path == NULL) {
        fprintf(stderr, "Ошибка: путь не может быть NULL.\n");
        return -1;  // Возвращаем ошибку
    }

    // Пытаемся сменить директорию
    if (chdir(path) == -1) {
        // Если произошла ошибка, выводим сообщение
        fprintf(stderr, "Ошибка при смене директории на '%s': %s\n", path, strerror(errno));
        return -1;  // Возвращаем ошибку
    }

    return 0;  // Успех
}