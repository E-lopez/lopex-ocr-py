from models.defaults.defaults_dict import document_defaults


def calculate_coords(values):
  x0 = values[0]
  top = values[1]
  x1 = x0 + values[2]
  bottom = top + values[3]
  return (x0, top, x1, bottom)


def get_default(document, index, version):
    try:
      default = document_defaults[document][version][index]
      return default
    except KeyError:
      return 'n/a'