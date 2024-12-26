from __future__ import annotations
from abc import ABC, abstractmethod
import locale
from typing import List
from models.defaults.defaults_dict import document_defaults
from utils.functions import get_default
import re

loc = locale.getlocale()
locale.setlocale(locale.LC_MONETARY, loc)

class RowParser():
  def __init__(self, strategy = None) -> None:
    self._strategy = self.select_parser(strategy)

  def select_parser(self, strategy):
    match strategy:
      case 'table_row':
        return TableRowsParser()
      case _:
        return DefaultParser()

  def set_parser(self, strategy: Strategy):
    self._strategy = strategy

  def use_parser(self, *args):
    return self._strategy.parse_row(*args)


class Strategy(ABC):
  @abstractmethod
  def parse_row(self, *args: List):
    pass


class DefaultParser(Strategy):
  def parse_row(self, *args):
    file_name, key, page, crop_coords, document, version = args
    t = page.crop(crop_coords, relative=True)
    s = t.extract_text(keep_blank_chars=False, layout=False, x_tolerance=7)
    is_char_index_list = [7,8,9,10,11]

    label_holder = ''.join(filter(lambda x: x.isalpha() or x.isspace(), re.findall(r'\D', s))).strip()
    numeric = re.findall(r'\d+', s)
    index = numeric[0]
    is_char = int(index) in is_char_index_list
    char_label = '' if label_holder.split('\n')[-1] == label_holder else label_holder.split('\n')[-1]
    value = char_label if is_char else ''.join(numeric[1:])
    label = label_holder if label_holder else get_default(document, index, version)

    return [file_name, index, key, label, value]


class TableRowsParser(Strategy):
  def parse_row(self, *args) -> List:
    file_name, key, page, crop_coords, document, version = args
    t = page.crop(crop_coords, relative=True)
    s = t.extract_text(keep_blank_chars=False, layout=False, x_tolerance=7)
    parsed_key = re.sub(r'\d+', '', key)
    label_holder = ''.join(filter(lambda x: x.isalpha() or x.isspace(), re.findall(r'\D', s))).strip()
    numeric = re.findall(r'\d+', s.replace(',', ''))

    if(len(numeric) > 1):
      value = locale.currency(int(numeric[1]))
      index = numeric[0]
    else:
      test = int(numeric[0]) == 0 or len(numeric[0]) > 2
      value = locale.currency(int(numeric[0])) if test else 'n/a'
      index = '00' if test else numeric[0]
    
    label = label_holder if label_holder else get_default(document, index, version)

    return [file_name, index, parsed_key, label, value]
       