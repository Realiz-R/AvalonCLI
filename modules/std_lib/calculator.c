#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

// Определяем M_PI и M_E, если они не определены
#ifndef M_PI
#define M_PI 3.14159265358979323846  // Значение π
#endif

#ifndef M_E
#define M_E 2.71828182845904523536   // Значение e
#endif

// Максимальная длина имени функции или константы
#define MAX_FUNC_NAME_LEN 32

// Функция для вычисления факториала (оптимизированная)
double factorial(double n) {
    if (n < 0 || n != (int)n) return NAN;  // Факториал определён только для целых неотрицательных чисел
    double result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
        if (isinf(result)) return INFINITY;  // Проверка на переполнение
    }
    return result;
}

// Функция для получения констант (с кэшированием)
double get_constant(const char* name) {
    static const struct {
        const char* name;
        double value;
    } constants[] = {
        {"pi", M_PI},
        {"π", M_PI},
        {"пи", M_PI},
        {"e", M_E},
        {NULL, NAN}
    };

    for (int i = 0; constants[i].name; i++) {
        if (strcmp(name, constants[i].name) == 0) {
            return constants[i].value;
        }
    }
    return NAN;  // Неизвестная константа
}

// Парсер выражений
double parse_expression(const char** expr);

// Парсер чисел и констант
double parse_number(const char** expr) {
    double result = 0;
    while (isdigit(**expr)) {
        result = result * 10 + (**expr - '0');
        (*expr)++;
    }
    if (**expr == '.') {
        (*expr)++;
        double fraction = 0.1;
        while (isdigit(**expr)) {
            result += (**expr - '0') * fraction;
            fraction *= 0.1;
            (*expr)++;
        }
    }
    return result;
}

// Парсер функций и констант
double parse_function(const char** expr) {
    char func_name[MAX_FUNC_NAME_LEN] = {0};
    int i = 0;
    while (isalpha(**expr) || (**expr & 0x80)) {  // Поддержка UTF-8 символов (например, "пи")
        if (i >= MAX_FUNC_NAME_LEN - 1) return NAN;  // Защита от переполнения буфера
        func_name[i++] = **expr;
        (*expr)++;
    }
    func_name[i] = '\0';

    // Пропускаем пробелы после имени функции
    while (**expr == ' ') (*expr)++;

    // Обработка функций с аргументами
    if (**expr == '(') {
        (*expr)++;  // Пропускаем '('
        double arg = parse_expression(expr);
        if (**expr != ')') return NAN;  // Ошибка: отсутствует закрывающая скобка
        (*expr)++;  // Пропускаем ')'

        if (strcmp(func_name, "sin") == 0) return sin(arg);
        else if (strcmp(func_name, "cos") == 0) return cos(arg);
        else if (strcmp(func_name, "tan") == 0) return tan(arg);
        else if (strcmp(func_name, "log") == 0) return (arg > 0) ? log10(arg) : NAN;
        else if (strcmp(func_name, "ln") == 0) return (arg > 0) ? log(arg) : NAN;
        else if (strcmp(func_name, "arctan") == 0) return atan(arg);
        else if (strcmp(func_name, "factorial") == 0) return factorial(arg);
        else if (strcmp(func_name, "abs") == 0) return fabs(arg);
        else if (strcmp(func_name, "round") == 0) return round(arg);
    }

    // Обработка констант
    return get_constant(func_name);
}

// Парсер выражений
double parse_expression(const char** expr) {
    double result = 0;
    while (**expr == ' ') (*expr)++;  // Пропускаем пробелы

    if (**expr == '(') {
        (*expr)++;
        result = parse_expression(expr);
        if (**expr != ')') return NAN;  // Ошибка: отсутствует закрывающая скобка
        (*expr)++;
    } else if (isdigit(**expr) || **expr == '.') {
        result = parse_number(expr);
    } else if (isalpha(**expr) || (**expr & 0x80)) {  // Поддержка UTF-8 символов
        result = parse_function(expr);
    }

    while (**expr == ' ') (*expr)++;  // Пропускаем пробелы

    if (**expr == '+' || **expr == '-' || **expr == '*' || **expr == '/' || **expr == '^' || **expr == '%') {
        char op = **expr;
        (*expr)++;
        double next = parse_expression(expr);
        if (op == '+') result += next;
        else if (op == '-') result -= next;
        else if (op == '*') result *= next;
        else if (op == '/') result = (next != 0) ? result / next : NAN;  // Проверка деления на ноль
        else if (op == '^') result = pow(result, next);
        else if (op == '%') result = fmod(result, next);
    } else if (**expr == '/' && *(*expr + 1) == '/') {  // Целочисленное деление
        (*expr) += 2;
        double next = parse_expression(expr);
        result = (next != 0) ? floor(result / next) : NAN;  // Проверка деления на ноль
    }

    return result;
}

// Основная функция калькулятора
double calc(const char* expression) {
    return parse_expression(&expression);
}