import unittest
import json
from unittest.mock import patch, MagicMock
from src.models.result import DocumentClassification, ExpedienteModel, DocumentoModel
from index import lambda_handler


class TestIndex(unittest.TestCase):

    @patch('index.context_loader')
    @patch('index.create_multi_prompt_chain')
    @patch('index.insert_results')
    @patch('index.init_model')
    def test_lambda_handler_success(self, mock_init_model, mock_insert_results, mock_create_multi_prompt_chain, mock_context_loader):
        # Mock the context loader
        mock_context_loader.return_value = [{'name': 'doc1', 'description': 'desc1'}]

        # Mock the classification result
        mock_chain = MagicMock()
        mock_chain.run.return_value = DocumentClassification(
            expediente=ExpedienteModel(id=1, tipo_expediente='test'),
            documento=DocumentoModel(tipo_documento='test', nombre_archivo='test.txt'),
            campos_extraidos=[],
            confianza_total=0.9,
            razon='test'
        )
        mock_create_multi_prompt_chain.return_value = mock_chain

        # Mock the insert_results function
        mock_insert_results.return_value = {'status': 'success'}

        # Create a sample event
        event = {'contenido': 'test content', 'nombre': 'test.txt'}

        # Call the lambda handler
        result = lambda_handler(event, None)

        # Assert that the result is correct
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['nombre'], 'test.txt')
        self.assertEqual(body['tipo_documento'], 'test')
        self.assertEqual(body['confianza'], 0.9)
        self.assertEqual(body['razon'], 'test')

    def test_lambda_handler_no_content(self):
        # Create a sample event with no content
        event = {'nombre': 'test.txt'}

        # Call the lambda handler
        result = lambda_handler(event, None)

        # Assert that the result is correct
        self.assertEqual(result['statusCode'], 400)
        body = json.loads(result['body'])
        self.assertEqual(body['tipo_documento'], 'Error')
        self.assertEqual(body['razon'], 'Sin contenido de documento')

    @patch('index.context_loader')
    def test_lambda_handler_exception(self, mock_context_loader):
        # Mock the context loader to raise an exception
        mock_context_loader.side_effect = Exception('test exception')

        # Create a sample event
        event = {'contenido': 'test content', 'nombre': 'test.txt'}

        # Call the lambda handler
        result = lambda_handler(event, None)

        # Assert that the result is correct
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        self.assertEqual(body['tipo_documento'], 'Error')
        self.assertEqual(body['razon'], 'Error en clasificación: test exception')


if __name__ == '__main__':
    unittest.main()
