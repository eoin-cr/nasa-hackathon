import keras
from keras import ops
from keras import layers
import numpy as np

class BinaryTransformClassifier:
    def __init__(self, input_shape):
        input_layer = keras.layers.Input(input_shape)

        conv1 = keras.layers.Conv2D(filters=1024, kernel_size=3, padding="same")(input_layer)
        batched1 = keras.layers.BatchNormalization()(conv1)
        relued1 = keras.layers.ReLU()(batched1)

        conv2 = keras.layers.Conv2D(filters=512, kernel_size=3, padding="same")(relued1)
        batched2 = keras.layers.BatchNormalization()(conv2)
        relued2 = keras.layers.ReLU()(batched2)

        conv3 = keras.layers.Conv2D(filters=64, kernel_size=3, padding="same")(relued2)
        batched3 = keras.layers.BatchNormalization()(conv3)
        relued3 = keras.layers.ReLU()(batched3)
        
        gap = keras.layers.GlobalAveragePooling2D()(relued3)

        output_layer = keras.layers.Dense(1, activation="sigmoid")(gap)

        self.model = keras.models.Model(inputs=input_layer, outputs=output_layer)

    def train(self, epochs, x_train, y_train, batch_size=32,):
        idx = np.random.permutation(len(x_train))
        x_train = x_train[idx]
        y_train = y_train[idx]

        callbacks = [
            keras.callbacks.ModelCheckpoint(
                "binaryclass_lunar.keras", save_best_only=True, monitor="val_loss"
            ),
        ]

        self.model.compile(
         loss=keras.losses.BinaryCrossentropy(),
    metrics=[
        keras.metrics.BinaryAccuracy(),
        keras.metrics.FalseNegatives(),
    ],   optimizer=keras.optimizers.Adam(learning_rate=0.01),
        )

        return self.model.fit(
            x_train,
            y_train,
            batch_size=batch_size,
            epochs=epochs,
            callbacks=callbacks,
            validation_split=0.2,
            verbose=1,
        )

    def evaluate(self, x_test, y_test):
        model = keras.saving.load_model("binaryclass_lunar.keras")
        return model.evaluate(x_test, y_test)

    def generate(self, x):
        model = keras.saving.load_model("binaryclass_lunar.keras")
        return model.predict(x)
