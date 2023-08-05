def checkType(object, classinfo):
  if not isinstance(object, classinfo):
    raise TypeError(f"{object.__name__} should be {classinfo}, instead {object} passed")
