import unittest
from datetime import datetime

from xlsx_to_dict import xlsx_to_dict


class TestXlsxToDict(unittest.TestCase):
    def test_xlsx_to_dict(self):
        expected = [
            {"nome": "Fulano",
             "idade": 42, "patrimonio": 42,
             "data_nascimento": datetime.strptime("01/01/01", "%d/%m/%y")},
            {"nome": "Ciclano",
             "idade": 84, "patrimonio": 84,
             "data_nascimento": datetime.strptime("12/12/12", "%d/%m/%y")},
        ]
        self.assertEqual(expected, xlsx_to_dict('tests/test.xlsx'))

    def test_get_first_row(self):
        expected = [
            {"nome": "Fulano",
             "idade": 42, "patrimonio": 42,
             "data_nascimento": datetime.strptime("01/01/01", "%d/%m/%y")},
            {"nome": "Ciclano",
             "idade": 84, "patrimonio": 84,
             "data_nascimento": datetime.strptime("12/12/12", "%d/%m/%y")},
        ]
        self.assertEqual(expected, xlsx_to_dict('tests/test.xlsx', sheetname='Planilha2'))

    def test_get_first_col(self):
        expected = [
            {"nome": "Fulano",
             "idade": 42, "patrimonio": 42,
             "data_nascimento": datetime.strptime("01/01/01", "%d/%m/%y")},
            {"nome": "Ciclano",
             "idade": 84, "patrimonio": 84,
             "data_nascimento": datetime.strptime("12/12/12", "%d/%m/%y")},
        ]
        self.assertEqual(expected, xlsx_to_dict('tests/test.xlsx', sheetname='Planilha3'))
