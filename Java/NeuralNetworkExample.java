import org.deeplearning4j.nn.conf.Configuration;
import org.deeplearning4j.nn.conf.MultiLayerConfiguration;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.optim.api.OptimizationAlgorithm;
import org.nd4j.linalg.activations.Activations;
import org.nd4j.linalg.learning.config.Adam;
import org.nd4j.linalg.dataset.api.iterator.DataSetIterator;
import org.nd4j.linalg.factory.Nd4j;

public class NeuralNetworkExample {

    public static void main(String[] args) {
        // Конфигурация нейронной сети
        int inputSize = 784;  // Например, размер изображения 28x28
        int outputSize = 10;  // Для цифр 0-9 в MNIST

        MultiLayerConfiguration configuration = new NeuralNetConfiguration.Builder()
                .seed(123) // Для воспроизводимости
                .updater(new Adam(0.001))
                .list()
                .layer(0, new DenseLayer.Builder()
                        .nIn(inputSize)
                        .nOut(128)
                        .activation(Activations.RELU)
                        .build())
                .layer(1, new OutputLayer.Builder()
                        .nIn(128)
                        .nOut(outputSize)
                        .activation(Activations.SOFTMAX)
                        .build())
                .build();

        // Создание модели
        MultiLayerNetwork model = new MultiLayerNetwork(configuration);
        model.init();

        // Здесь можно добавить код для тренировки модели на данных
        // Например, с использованием DataSetIterator
    }
}
