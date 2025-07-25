import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

from src.db.context_loader import context_loader
from src.db.insert_results import insert_results
from src.models.result import DocumentClassification, ExpedienteModel, DocumentoModel


class TestDB(unittest.TestCase):

    @patch('src.db.context_loader.get_db_connection')
    def test_context_loader(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock the data returned by the database
        data = {
            'documento_nombre': ['doc1', 'doc1', 'doc2'],
            'documento_descripcion': ['desc1', 'desc1', 'desc2'],
            'campo_nombre': ['campo1', 'campo2', 'campo3'],
            'campo_tipo': ['tipo1', 'tipo2', 'tipo3'],
            'requerido': [True, False, True]
        }
        df = pd.DataFrame(data)
        with patch('pandas.read_sql', return_value=df):
            result = context_loader()

        # Assert that the result is correct
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'doc1')
        self.assertEqual(result[1]['name'], 'doc2')
        self.assertIn('desc1', result[0]['description'])
        self.assertIn('campo1', result[0]['description'])
        self.assertIn('campo2', result[0]['description'])
        self.assertIn('desc2', result[1]['description'])
        self.assertIn('campo3', result[1]['description'])

    @patch('src.db.insert_results.get_db_connection')
    @patch('src.db.insert_results.get_or_create_tipo_expediente')
    @patch('src.db.insert_results.get_or_create_expediente')
    @patch('src.db.insert_results.get_tipo_documento_id')
    @patch('src.db.insert_results.insert_documento')
    @patch('src.db.insert_results.insert_campos_extraidos')
    def test_insert_results(self, mock_insert_campos_extraidos, mock_insert_documento, mock_get_tipo_documento_id, mock_get_or_create_expediente, mock_get_or_create_tipo_expediente, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock the return values of the helper functions
        mock_get_or_create_tipo_expediente.return_value = 1
        mock_get_or_create_expediente.return_value = 1
        mock_get_tipo_documento_id.return_value = 1
        mock_insert_documento.return_value = 1

        # Create a DocumentClassification instance
        resultado = DocumentClassification(
            expediente=ExpedienteModel(id=1, tipo_expediente='test'),
            documento=DocumentoModel(tipo_documento='test', nombre_archivo='test.txt'),
            campos_extraidos=[],
            confianza_total=0.9,
            razon='test'
        )

        # Call the function
        result = insert_results(resultado)

        # Assert that the result is correct
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['expediente_id'], 1)
        self.assertEqual(result['documento_id'], 1)


if __name__ == '__main__':
    unittest.main()
