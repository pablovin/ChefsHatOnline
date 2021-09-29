from keras.models import load_model
import keras
import tensorflow as tf
import tensorflow_addons as tfa
from django.conf import settings

class SupervisedContrastiveLoss(keras.losses.Loss):
    CLASSIFIERTYPE = {'categorical': 'categorical',
                      'mse': 'mse',
                      "BinaryCrossEntropy": "BinaryCrossEntropy"}

    def __init__(self, temperature=1, name=None):
        super(SupervisedContrastiveLoss, self).__init__(name=name)
        self.temperature = temperature

    def __call__(self, labels, feature_vectors, sample_weight=None):
        # print("Shape labels:" + str(labels.shape))
        # print("Shape feature_vectors:" + str(feature_vectors.shape))

        # Normalize feature vectors
        feature_vectors_normalized = tf.math.l2_normalize(feature_vectors, axis=1)
        # print("Shape feature_vectors normalized:" + str(feature_vectors_normalized.shape))
        # print("Shape transpose  normalized:" + str(tf.transpose(feature_vectors_normalized).shape))
        # Compute logits
        logits = tf.divide(
            tf.matmul(
                feature_vectors_normalized, tf.transpose(feature_vectors_normalized)
            ),
            self.temperature,
        )

        labels = tf.math.argmax(labels, 1)

        return tfa.losses.npairs_loss(tf.squeeze(labels), logits)


class SimialrityNetwork():

    def __init__(self):
        self.model = keras.models.load_model(settings.BASE_DIR + settings.STATIC_URL+"/trainedModels/similarityNetwork/", custom_objects={'SupervisedContrastiveLoss': SupervisedContrastiveLoss}, compile=False)

    def predict(self, stateAndActions):
        return self.model.predict(stateAndActions)