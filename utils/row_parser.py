from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from models.defaults.defaults_dict import document_defaults
from utils.functions import get_default


class RowParser():
  def __init__(self, strategy: Strategy = None) -> None:
    if strategy is not None:
        self._strategy = strategy
    else:
        self._strategy = DefaultParser()

  def set_parser(self, strategy: Strategy):
    self._strategy = strategy

  def use_parser(self, *args):
    self._strategy.parse_row(*args)


class Strategy(ABC):
  @abstractmethod
  def parse_row(self, data: List):
    pass


class DefaultParser(Strategy):
  def parse_row(self, *args) -> List:
    s, key, document, version, file_name = args

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


class TableRowsParser(Strategy):
  def parse_row(self, *args) -> List:
    s, key, document, version, file_name = args

    print("STRATEGY B")

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
       