# build_model.py
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Dense, BatchNormalization, Activation, Dropout, MaxPooling2D, Flatten, DepthwiseConv2D, GlobalAveragePooling2D
from keras import regularizers

def build_model(input_size, classes=7):
    model = tf.keras.models.Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), input_shape=input_size))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(64, kernel_size=(3, 3)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(DepthwiseConv2D(kernel_size=(3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, kernel_size=(1, 1)))
    model.add(Activation('relu'))

    model.add(Conv2D(256, kernel_size=(3, 3)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(512, kernel_size=(3, 3)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(7, kernel_size=(1, 1)))
    model.add(GlobalAveragePooling2D())
    model.add(Activation('softmax'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model
