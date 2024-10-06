import keras
from keras import ops
from keras import layers
import numpy as np

class BinaryTransformClassifier:
    def __init__(self, input_shape):
        input_layer = keras.layers.Input(input_shape)

        conv1 = keras.layers.Conv2D(filters=64, kernel_size=3, padding="same")(input_layer)
        conv1 = keras.layers.BatchNormalization()(conv1)
        conv1 = keras.layers.ReLU()(conv1)

        conv2 = keras.layers.Conv2D(filters=64, kernel_size=3, padding="same")(conv1)
        conv2 = keras.layers.BatchNormalization()(conv2)
        conv2 = keras.layers.ReLU()(conv2)

        conv3 = keras.layers.Conv2D(filters=64, kernel_size=3, padding="same")(conv2)
        conv3 = keras.layers.BatchNormalization()(conv3)
        conv3 = keras.layers.ReLU()(conv3)
        
        gap = keras.layers.GlobalAveragePooling2D()(conv3)

        output_layer = keras.layers.Dense(2, activation="softmax")(gap)

        self.model = keras.models.Model(inputs=input_layer, outputs=output_layer)

    def train(self, epochs, x_train, y_train, batch_size=32,):
        idx = np.random.permutation(len(x_train))
        x_train = x_train[idx]
        y_train = y_train[idx]

        callbacks = [
            keras.callbacks.ModelCheckpoint(
                "binaryclass_lunar.keras", save_best_only=True, monitor="val_loss"
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=20, min_lr=0.0001
            ),
            keras.callbacks.EarlyStopping(monitor="val_loss", patience=50, verbose=1),
        ]

        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["sparse_categorical_accuracy"],
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
