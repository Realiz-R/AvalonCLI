#include <stdio.h>
#include <unistd.h>
#include <string.h>

// Смена директории
int change_directory(const char* path) {
    return chdir(path); // Возвращает 0 в случае успеха, -1 в случае ошибки
}
