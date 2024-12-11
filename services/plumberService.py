import io
import pdfplumber
import pandas as pd
from pdfplumber.utils import extract_text, get_bbox_overlap, obj_to_bbox
import tabulate
from models.coords.coords_dict import document_coords
from models.defaults.defaults_dict import document_defaults

def parse_with_plumber(file):
  f = io.BytesIO(file.getvalue())
  
  with pdfplumber.open(f, laparams = { "line_overlap": 0.7 }) as pdf:
    first_page = pdf.pages[0]
    im = first_page.to_image(resolution=320)
    im.reset().draw_rects(first_page.chars)
    im.show()


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


def get_version(s):
  if (len(s) == 1): return
  temp = s[-1].strip()
  return temp > 2018


def generate_row(file_name, key, s, document, version):
  if (len(s) > 1):
    temp = s[0].split('.', 1)
    index = temp[0]
    field = temp[1].strip()
    pre_value = ''.join(s[-1].split())
    value = pre_value if pre_value.isnumeric() else s[-1].strip()
    return [file_name, index, key, field, value]

  temp = s[0].split()
  index = temp[0].strip('.')
  if(temp[-1].isnumeric()):
    field = get_default(document, index, version)
    return [file_name, index, key, field, temp[-1]]
  else:
    return [file_name, index, key, temp[-1], '']
  

def get_boxes(file):
  f = io.BytesIO(file.getvalue())
  file_name = file.filename
  partial = pd.DataFrame({
    'filename': [],
    'index':[], 
    'section': [], 
    'field': [], 
    'value': [],
  })
  with pdfplumber.open(f, laparams = { "line_overlap": 0.7, "all_texts": True }) as pdf:
    for page in pdf.pages:
      initial = page.crop((50.71, 59.91, 100.71, 70.0), relative=True)
      version = ''.join(initial.extract_text(keep_blank_chars=False, layout=True).split()).strip()
      for key, value in document_coords['renta'][version].items():
        for coords in value:
          crop_coords = calculate_coords(coords)
          t = page.crop(crop_coords, relative=True)
          s = t.extract_text(keep_blank_chars=False, layout=True).splitlines()
          partial.loc[len(partial)] = generate_row(file_name, key, s, 'renta', version)
  return partial
        

def handle_multiple(files):
  df = pd.DataFrame()
  for file in files:
    partial = get_boxes(file)
    df = pd.concat([df, partial])
  print(df)
  return 'done'
   
   
def crop_doc(file):
  f = io.BytesIO(file.getvalue())

  text = ''
  pages = []

  with pdfplumber.open(f, laparams = { "line_overlap": 0.7 }) as pdf:
    for i, page in enumerate(pdf.pages):
        print(page.height, page.width, 0.2 * float(page.height), 0.5 * page.width, page.height)
        im = page.to_image(resolution=150)
        t = page.crop((43.89, 154.56, 166.87, 179.33))
        im.draw_rects(t.extract_words())
        im.show()
        #   page_crop = page.crop(bbox=my_bbox)
        text = text+str(t.extract_text()).lower()

  return text
   