#include <stdio.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>

// Функция для создания директории
void create_directory(const char *dirpath) {
    // Проверяем, существует ли директория
    struct stat st = {0};

    if (stat(dirpath, &st) == -1) {
        // Директории нет, пробуем создать
#ifdef _WIN32
        // На Windows используем mkdir без параметра mode
        if (mkdir(dirpath) == -1) {
#else
        // На Unix-системах используем mkdir с параметром mode (например, 0755)
        if (mkdir(dirpath, 0755) == -1) {
#endif
            // Если произошла ошибка, выводим сообщение
            fprintf(stderr, "Ошибка при создании директории '%s': %s\n", dirpath, strerror(errno));
        } else {
            printf("Директория '%s' успешно создана.\n", dirpath);
        }
    } else if (S_ISDIR(st.st_mode)) {
        // Директория уже существует
        printf("Директория '%s' уже существует.\n", dirpath);
    } else {
        // По указанному пути существует файл, но это не директория
        fprintf(stderr, "Ошибка: '%s' существует, но это не директория.\n", dirpath);
    }
}

// Основная функция, которая будет вызываться из Python
void create_from_python(const char *dirpath) {
    create_directory(dirpath);
}