import tensorflow as tf
from tensorflow.keras.optimizers import Optimizer, SGD, RMSprop, Adam


OPT_SHORTCUTS = ["sgd", "rmsprop", "adam"]
TF_OPTIMIZERS = [SGD(), RMSprop(), Adam()]


def selectOptimizer(optimizer) -> Optimizer:
  if isinstance(optimizer, str):
    if optimizer in OPT_SHORTCUTS:
      for opt, tf_opt in zip(OPT_SHORTCUTS, TF_OPTIMIZERS):
        if optimizer == opt:
          return tf_opt
    else:
      raise ValueError(f"`optimizer` should be selected in {OPT_SHORTCUTS}, "
                       f"instead '{optimizer}' passed")
  elif isinstance(optimizer, Optimizer):
    return optimizer
  else:
    raise TypeError(f"`optimizer` should be a TensorFlow `Optimizer`, "
                    f"instead {type(optimizer)} passed")
