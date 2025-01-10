import java.util.Scanner;

public class SimpleCalculator {
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Добро пожаловать в Realiz калькулятор!");
        System.out.println("Введите первое число: ");
        double num1 = scanner.nextDouble();

        System.out.println("Введите второе число: ");
        double num2 = scanner.nextDouble();

        System.out.println("Выбирите операцию: ");
        System.out.println("1. Сложение (+)");
        System.out.println("2. Вычитание (-)");
        System.out.println("3. Умножение (*)");
        System.out.println("4. Деление (/)");

        int choice = scanner.nextInt();
        double result;

        switch (choice) {
            case 1:
                result = num1 + num2;
                System.out.println("Результат: " + num1 + " + " + num2 + " = " +
result);                
                break; 
            case 2:
                result = num1 - num2;
                System.out.println("Результат: " + num1 + " - " + num2 + " = " +
result);
                break;   
            case 3:
                result = num1 * num2;
                System.out.println("Результат: " + num1 + " * " + num2 + " = " + 
result);
                break;
            case 4:
                if (num2 != 0) {
                    result = num1 / num2;
                    System.out.println("Результат: " + num1 + " / " + num2 + " = " + 
result);
                } else {
                    System.out.println("Ошибка: Деление на ноль невозможно.");
                }
                break;
            default:
                System.out.println("Неверный выбор операции.");
                break;
        

        }
    }
}
