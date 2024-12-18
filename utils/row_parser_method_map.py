def get_row_parser_method_name(key):
  match key:
    case 'informacion_general':
      return None
    case _:
      return 'table_row'