import keras
import numpy as np
import tensorflow as tf
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
from diana_exceptions import ModelCannotBeFoundException


class NN:
    def __init__(self, model_name):
        self.graph = None
        self.model = self.get_model(model_name=model_name)
        self.target_size = {"xception": (299, 299),
                            "inceptionv3": (299, 299),
                            "vgg16": (224, 224),
                            "resnet50": (224, 224),
                            "vgg19": (224, 224)}

    def get_model(self, model_name):
        model_name = model_name.lower()
        self.model_name = model_name

        if model_name == "xception":
            model = keras.applications.xception.Xception(include_top=True, weights='imagenet', input_tensor=None,
                                                         input_shape=None, pooling=None, classes=1000)

        elif model_name == "vgg16":
            model = keras.applications.vgg16.VGG16(include_top=True, weights='imagenet', input_tensor=None,
                                                   input_shape=None, pooling=None, classes=1000)

        elif model_name == "vgg19":
            model = keras.applications.vgg19.VGG19(include_top=True, weights='imagenet', input_tensor=None,
                                                   input_shape=None, pooling=None, classes=1000)

        elif model_name == "resnet50":
            model = keras.applications.resnet50.ResNet50(include_top=True, weights='imagenet', input_tensor=None,
                                                         input_shape=None, pooling=None, classes=1000)

        elif model_name == "inceptionv3":
            keras.applications.inception_v3.InceptionV3(include_top=True, weights='imagenet', input_tensor=None,
                                                        input_shape=None, pooling=None, classes=1000)
        else:
            raise ModelCannotBeFoundException("Model does not exist. Given : {}.".format(model_name))

        self.graph = tf.get_default_graph()

        return model

    def preprocess_input(self, x):
        x /= 255.
        x -= 0.5
        x *= 2.
        return x

    def predict(self, img_path):

        img = image.load_img(img_path,
                             target_size=self.target_size[self.model_name])
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = self.preprocess_input(x)
        # print('Input image shape:', x.shape)

        with self.graph.as_default():
            preds = self.model.predict(x)
            # print(np.argmax(preds))
            # print('Predicted:', decode_predictions(preds, 1))

        #  [[('n03291819', 'envelope', 0.0462779)]]
        triple = decode_predictions(preds, 1)[0][0]
        return {"label": triple[1],
                "prob": triple[2]}
