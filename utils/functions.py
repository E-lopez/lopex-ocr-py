from models.defaults.defaults_dict import document_defaults
#(x0, top, width, heigth)

presets = {
   'left': {
      'x0': 40.68, 
      'width': 269.45, 
      'height': 11.39,
   },
}


def calculate_coords(values, key):
  match key:
    case 'informacion_general':
      x0 = values[0]
      top = values[1]
      x1 = x0 + values[2]
      bottom = top + values[3]
      return (x0, top, x1, bottom)
    case _:
      x0, width, height = presets['left'].values()
      top = float(values)
      x1 = x0 + width
      bottom = top + height
      return (x0, top, x1, bottom)
      
      
     
def get_default(document, index, version):
    try:
      default = document_defaults[document][version][index]
      return default
    except KeyError:
      return 'n/a'