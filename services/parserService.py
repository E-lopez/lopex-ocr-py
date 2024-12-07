from io import StringIO
import io
from typing import Iterable, Any

import PyPDF2
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextContainer, LTTextLine, LTTextBox
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_document_service(file):
  if allowed_file(file.filename):
    pdf_reader = PyPDF2.PdfReader(file)
    test = ''

    for page_num in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[page_num]
      test += page.extract_text()

    return test
  
  
def parse_with_miner(file):
  # output = StringIO()
  # manager = PDFResourceManager()
  # converter = TextConverter(manager, output, laparams=LAParams())
  # interpreter = PDFPageInterpreter(manager, converter)

  output_string = StringIO()

  parser = PDFParser(file)
  doc = PDFDocument(parser)

  rsrcmgr = PDFResourceManager()
  device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
  # device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
  interpreter = PDFPageInterpreter(rsrcmgr, device)


  for page in PDFPage.create_pages(doc):
      interpreter.process_page(page)

  return output_string.getvalue()

  #     layout = device.get_result()
  #     for lobj in layout:
  #       if isinstance(lobj, LTTextBox):
  #         x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
  #         print('At %r is text: %s' % ((x, y), text))
  # return output_string.getvalue()

  # for page_layout in extract_pages(f):
  #   for element in page_layout:
  #       if isinstance(element, LTTextLine):
  #           output.write(element.get_text())
  
  # return output.getvalue()

  # fields = resolve1(doc.catalog['AcroForm'])['Fields']
  # test = ''
  # for i in fields:
  #   field = resolve1(i)
  #   name, value = field.get('T'), field.get('V')
  #   test += '{0}: {1}'.format(name, value)
  # return test


def show_ltitem_hierarchy(o, depth=0):  
    """Show location and text of LTItem and all its descendants"""
    if depth == 0:
        print('element                        x1  y1  x2  y2   text')
        print('------------------------------ --- --- --- ---- -----')

    print(
        f'{get_indented_name(o, depth):<30.30s} '
        f'{get_optional_bbox(o)} '
        f'{get_optional_text(o)}'
    )

    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, depth=depth + 1)


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of LTItem"""
    return '  ' * depth + o.__class__.__name__


def get_optional_bbox(o: Any) -> str:
    """Bounding box of LTItem if available, otherwise empty string"""
    if hasattr(o, 'bbox'):
        return ''.join(f'{i:<4.0f}' for i in o.bbox)
    return ''


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}