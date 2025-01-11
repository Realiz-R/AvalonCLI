#include <stdio.h>
#include <stdlib.h>
#include <utime.h>
#include <sys/stat.h>
#include <locale.h>
#include <windows.h>

void set_utf8_codepage() {
    // Устанавливаем кодовую страницу UTF-8 для консоли
    SetConsoleOutputCP(CP_UTF8);
}

void touch_file(const char *filepath) {
    struct stat buffer;

    // Проверяем существование файла
    if (stat(filepath, &buffer) == 0) {
        // Файл существует, обновляем время доступа
        if (utime(filepath, NULL) == -1) {
            perror("Ошибка при обновлении времени доступа");
        } else {
            printf("Время доступа для файла '%s' обновлено.\n", filepath);
        }
    } else {
        // Файл не существует, создаем его
        FILE *file = fopen(filepath, "w, ccs=UTF-8"); // Открываем файл для записи
        if (file) {
            fclose(file);
            printf("Файл '%s' успешно создан.\n", filepath);
        } else {
            perror("Ошибка при создании файла");
        }
    }
}

// Основная функция для вызова из Python
void touch_from_python(const char *filepath) {
    touch_file(filepath);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Использование: %s <имя_файла>\n", argv[0]);
        return 1;
    }

    // Установка кодовой страницы и локали
    set_utf8_codepage();
    setlocale(LC_ALL, "en_US.UTF-8");  // Устанавливаем локаль для поддержки UTF-8

    touch_from_python(argv[1]);
    return 0;
}