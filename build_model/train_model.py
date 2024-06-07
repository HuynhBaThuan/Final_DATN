# train_model.py
from model import build_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir = 'data/train'
test_dir = "data/test_new"

input_size = (48, 48, 1)
classes = 7

model = build_model(input_size, classes)

train_datagen = ImageDataGenerator(rescale=1./255,
                                   zoom_range=0.3,
                                   horizontal_flip=True,
                                   rotation_range=10,
                                   width_shift_range= 0.1,
                                   height_shift_range= 0.1,
                                   shear_range= 0.2 )

training_set = train_datagen.flow_from_directory(train_dir,
                                                batch_size=64,
                                                target_size=(48,48),
                                                shuffle=True,
                                                color_mode='grayscale',
                                                class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)
test_set = test_datagen.flow_from_directory(test_dir,
                                                batch_size=64,
                                                target_size=(48,48),
                                                shuffle=True,
                                                color_mode='grayscale',
                                                class_mode='categorical')

hist = model.fit(x=training_set,
                 validation_data=test_set,
                 epochs=150)

model.save('trained_model.h5')
