using System;
using System.Net.Http;
using System.Text.RegularExpressions;

namespace TranslatorLib
{
    public class Translator
    {
        private static readonly HttpClient client = new HttpClient();

        // Функция для перевода текста
        public static string Translate(string text, string targetLanguage)
        {
            try
            {
                // URL для Google Translate
                string url = $"https://translate.google.com/m?hl={targetLanguage}&sl=auto&q={Uri.EscapeDataString(text)}";

                // Отправляем GET-запрос
                HttpResponseMessage response = client.GetAsync(url).Result;
                response.EnsureSuccessStatusCode();

                string responseBody = response.Content.ReadAsStringAsync().Result;

                // Используем регулярное выражение для извлечения переведенного текста
                var match = Regex.Match(responseBody, "<div class=\"result-container\">(.*?)</div>", RegexOptions.Singleline);

                // Проверка на случай, если перевод не найден
                if (match.Success)
                {
                    return match.Groups[1].Value.Trim();
                }
                else
                {
                    return "Перевод не найден.";
                }
            }
            catch (Exception ex)
            {
                return $"Ошибка: {ex.Message}";
            }
        }

#if DEBUG
        // Точка входа для тестирования (только в режиме DEBUG)
        public static void Main(string[] args)
        {
            Console.WriteLine("Введите текст для перевода:");
            string textToTranslate = Console.ReadLine();

            Console.WriteLine("Введите тег языка (например, 'en' для английского):");
            string targetLanguage = Console.ReadLine();

            string translatedText = Translate(textToTranslate, targetLanguage);
            Console.WriteLine($"Перевод: {translatedText}");
        }
#endif
    }
}