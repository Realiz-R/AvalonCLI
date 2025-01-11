#include <stdio.h>
#include <sys/stat.h>
#include <errno.h>

void create_directory(const char *dirpath) {
    // Проверяем, существует ли директория
    struct stat st = {0};

    if (stat(dirpath, &st) == -1) {
        // Директории нет, пробуем создать
        if (mkdir(dirpath) == -1) {  // Не указываем режим, чтобы избежать проблем на Windows
            perror("Ошибка при создании директории");
        } else {
            printf("Директория '%s' успешно создана.\n", dirpath);
        }
    } else {
        printf("Директория '%s' уже существует.\n", dirpath);
    }
}

// Основная функция, которая будет вызываться из Python
void create_from_python(const char *dirpath) {
    create_directory(dirpath);
}
