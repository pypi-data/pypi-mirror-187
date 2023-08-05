import tensorflow as tf
from tensorflow.keras.optimizers.schedules import LearningRateSchedule


class AttentionSchedule(LearningRateSchedule):
  def __init__(self, d_model, warmup_steps=4000):
    super().__init__()
    self._d_model = tf.cast(d_model, tf.float32)
    self._warmup_steps = warmup_steps

  def __call__(self, step):
    step = tf.cast(step, dtype=tf.float32)
    arg1 = tf.math.rsqrt(step)
    arg2 = step * (self._warmup_steps ** -1.5)
    return tf.math.rsqrt(self._d_model) * tf.math.minimum(arg1, arg2)
