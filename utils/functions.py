from models.defaults.defaults_dict import document_defaults
#(x0, top, width, heigth)

presets = {
   'left': {
      'x0': 40.68, 
      'width': 269.45, 
      'height': 11.39,
   },
   'right': {
      'x0': 324.48, 
      'width': 269.57, 
      'height': 11.39,
   }
}


def calculate_coords(values, key):
  right_column = ['Renta2', 'Ganancias_ocasionales', 'Impuestos_renta_liquida', 'Liquidacion_privada', 'Retenciones']
  right_offset = ['Impuestos_renta_liquida', 'Retenciones']
  match key:
    case 'informacion_general' | 'pago_total' | 'pie_de_pagina' | 'obras_por_impuestos':
      x0 = values[0]
      top = values[1]
      x1 = x0 + values[2]
      bottom = top + values[3]
      return (x0, top, x1, bottom)
    case _:
      selected_preset = 'right' if key in right_column else 'left'
      x_offset = 15.09 if key in right_offset else 0

      x0, width, height = presets[selected_preset].values()
      x0 += x_offset
      width -= x_offset
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