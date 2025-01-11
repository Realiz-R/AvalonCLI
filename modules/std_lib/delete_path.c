#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <errno.h>

// Функция для удаления файла
void delete_file(const char *filepath) {
    if (unlink(filepath) == -1) {
        perror("Ошибка при удалении файла");
    } else {
        printf("Файл '%s' успешно удалён.\n", filepath);
    }
}

// Функция для удаления директории и её содержимого
void delete_directory(const char *dirpath) {
    struct dirent *entry;
    DIR *dp = opendir(dirpath);
    
    // Проверка, удалось ли открыть директорию
    if (dp == NULL) {
        perror("Ошибка при открытии директории");
        return;
    }

    // Проходим по всем элементам в директории
    while ((entry = readdir(dp)) != NULL) {
        // Игнорируем текущую и родительскую директории
        if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
            char fullpath[1024];
            snprintf(fullpath, sizeof(fullpath), "%s/%s", dirpath, entry->d_name);

            // Пытаемся получить информацию о файле или директории
            struct stat entry_stat;
            if (stat(fullpath, &entry_stat) == -1) {
                perror("Ошибка при получении информации о файле");
                continue;
            }

            // Проверяем тип файла
            if (S_ISDIR(entry_stat.st_mode)) {
                // Если это директория, удаляем её рекурсивно
                delete_directory(fullpath);
            } else if (S_ISREG(entry_stat.st_mode)) {
                // Если это файл, удаляем файл
                delete_file(fullpath);
            } else {
                fprintf(stderr, "Неизвестный тип: '%s'\n", fullpath);
            }
        }
    }

    closedir(dp);

    // Удаляем саму директорию
    if (rmdir(dirpath) == -1) {
        perror("Ошибка при удалении директории");
    } else {
        printf("Директория '%s' успешно удалена.\n", dirpath);
    }
}

// Функция для определения типа пути и его удаления
void delete_path(const char *path) {
    struct stat path_stat;
    if (stat(path, &path_stat) == -1) {
        perror("Ошибка при получении информации о пути");
        return;
    }
    
    if (S_ISDIR(path_stat.st_mode)) {
        delete_directory(path);
    } else if (S_ISREG(path_stat.st_mode)) {
        delete_file(path);
    } else {
        fprintf(stderr, "Неизвестный тип: '%s'\n", path);
    }
}

// Основная функция, которая будет вызываться из Python
void delete_from_python(const char *path) {
    delete_path(path);
}
