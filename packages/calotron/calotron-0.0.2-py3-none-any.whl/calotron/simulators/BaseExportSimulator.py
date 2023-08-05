import tensorflow as tf
from calotron.simulators import BaseSimulator


class BaseExportSimulator(tf.Module):
  def __init__(self, simulator):
    super().__init__()
    if not isinstance(simulator, BaseSimulator):
      raise TypeError("transformer should be a calotron's BaseSimulator simulator")
    self._simulator = simulator

  @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.float32)])
  def __call__(self, source, max_length):
    result = self._simulator(source, max_length)
    return result

  @property
  def simulator(self) -> BaseSimulator:
    return self._simulator
