import keras


def pre_dl_models():
    """
    This script downloads the pre-trained models stored in keras.
    """
    keras.applications.xception.Xception(include_top=True, weights='imagenet', input_tensor=None,
                                         input_shape=None, pooling=None, classes=1000)

    # keras.applications.vgg16.VGG16(include_top=True, weights='imagenet', input_tensor=None,
    #                                input_shape=None, pooling=None, classes=1000)

    # keras.applications.vgg19.VGG19(include_top=True, weights='imagenet', input_tensor=None,
    #                                input_shape=None, pooling=None, classes=1000)

    # keras.applications.resnet50.ResNet50(include_top=True, weights='imagenet', input_tensor=None,
    #                                      input_shape=None, pooling=None, classes=1000)

    # keras.applications.inception_v3.InceptionV3(include_top=True, weights='imagenet', input_tensor=None,
    #                                             input_shape=None, pooling=None, classes=1000)


if __name__ == "__main__":
    pre_dl_models()
