import tensorflow as tf


class LatentMapLayer(tf.keras.layers.Layer):
  def __init__(self, latent_dim, num_layers, hidden_units=128):
    super().__init__()
    self._latent_dim = int(latent_dim)
    self._num_layers = int(num_layers)
    self._hidden_units = int(hidden_units)

    self._latent_layers = [
        tf.keras.layers.Dense(self._hidden_units, activation="relu")
        for _ in range(self._num_layers - 1)]
    self._latent_layers += [
        tf.keras.layers.Dense(self._latent_dim, activation="relu")]
  
  def call(self, x):
    outputs = list()
    for i in range(x.shape[1]):
      latent_tensor = x[:, i:i+1, :]
      print(i, latent_tensor.shape)
      for layer in self._latent_layers:
        latent_tensor = layer(latent_tensor)
      outputs.append(latent_tensor)

    concat = tf.keras.layers.Concatenate(axis=1)(outputs)
    print(concat.shape)
    output = tf.reduce_sum(concat, axis=1)
    return output

  @property
  def latent_dim(self) -> int:
    return self._latent_dim

  @property
  def num_layers(self) -> int:
    return self._latent_dim

  @property
  def hidden_units(self) -> int:
    return self._hidden_units
  
