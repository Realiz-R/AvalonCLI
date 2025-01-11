import okhttp3.*;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Scanner;

public class SimpleTranslator {

    private static final String API_URL = "https://libretranslate.com/translate";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введите текст для перевода:");
        String textToTranslate = scanner.nextLine();

        System.out.println("Введите язык, на который хотите перевести (например, 'es' для испанского):");
        String targetLanguage = scanner.nextLine();

        try {
            String translatedText = translate(textToTranslate, targetLanguage);
            System.out.println("Переведенный текст: " + translatedText);
        } catch (IOException e) {
            System.out.println("Ошибка при переводе: " + e.getMessage());
        }

        scanner.close();
    }

    private static String translate(String text, String targetLang) throws IOException {
        OkHttpClient client = new OkHttpClient();

        JSONObject json = new JSONObject();
        json.put("q", text);
        json.put("target", targetLang);
        json.put("source", "auto"); // Автоматическое определение языка

        RequestBody body = RequestBody.create(json.toString(), MediaType.parse("application/json"));
        Request request = new Request.Builder()
                .url(API_URL)
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected code " + response);
            }

            JSONObject responseJson = new JSONObject(response.body().string());
            return responseJson.getString("translatedText");
        }
    }
}
