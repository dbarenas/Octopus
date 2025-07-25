import unittest
from pydantic import ValidationError
from src.models.result import ExpedienteModel, DocumentoModel, CampoExtraidoModel, DocumentClassification
from src.models.context import CampoContexto, DocumentoContexto


class TestModels(unittest.TestCase):

    def test_expediente_model(self):
        # Test valid data
        data = {'id': 1, 'tipo_expediente': 'test'}
        model = ExpedienteModel(**data)
        self.assertEqual(model.id, 1)
        self.assertEqual(model.tipo_expediente, 'test')

        # Test invalid data
        with self.assertRaises(ValidationError):
            ExpedienteModel(id='a', tipo_expediente='test')

    def test_documento_model(self):
        # Test valid data
        data = {'tipo_documento': 'test', 'nombre_archivo': 'test.txt'}
        model = DocumentoModel(**data)
        self.assertEqual(model.tipo_documento, 'test')
        self.assertEqual(model.nombre_archivo, 'test.txt')

        # Test invalid data
        with self.assertRaises(ValidationError):
            DocumentoModel(tipo_documento='test', nombre_archivo=123)

    def test_campo_extraido_model(self):
        # Test valid data
        data = {'nombre_campo': 'test', 'valor': 'test', 'confianza': 0.9}
        model = CampoExtraidoModel(**data)
        self.assertEqual(model.nombre_campo, 'test')
        self.assertEqual(model.valor, 'test')
        self.assertEqual(model.confianza, 0.9)

        # Test invalid data
        with self.assertRaises(ValidationError):
            CampoExtraidoModel(nombre_campo='test', valor='test', confianza='a')

    def test_document_classification_model(self):
        # Test valid data
        data = {
            'expediente': {'id': 1, 'tipo_expediente': 'test'},
            'documento': {'tipo_documento': 'test', 'nombre_archivo': 'test.txt'},
            'campos_extraidos': [],
            'confianza_total': 0.9,
            'razon': 'test'
        }
        model = DocumentClassification(**data)
        self.assertEqual(model.expediente.id, 1)
        self.assertEqual(model.documento.tipo_documento, 'test')
        self.assertEqual(model.confianza_total, 0.9)

        # Test invalid data
        with self.assertRaises(ValidationError):
            DocumentClassification(
                expediente={'id': 'a', 'tipo_expediente': 'test'},
                documento={'tipo_documento': 'test', 'nombre_archivo': 'test.txt'},
                campos_extraidos=[],
                confianza_total=0.9,
                razon='test'
            )

    def test_campo_contexto_model(self):
        # Test valid data
        data = {'nombre': 'test', 'tipo': 'test', 'requerido': True, 'descripcion': 'test'}
        model = CampoContexto(**data)
        self.assertEqual(model.nombre, 'test')
        self.assertEqual(model.tipo, 'test')
        self.assertEqual(model.requerido, True)
        self.assertEqual(model.descripcion, 'test')

        # Test invalid data
        with self.assertRaises(ValidationError):
            CampoContexto(nombre='test', tipo='test', requerido='a', descripcion='test')

    def test_documento_contexto_model(self):
        # Test valid data
        data = {
            'nombre': 'test',
            'descripcion': 'test',
            'campos': [{'nombre': 'test', 'tipo': 'test', 'requerido': True, 'descripcion': 'test'}]
        }
        model = DocumentoContexto(**data)
        self.assertEqual(model.nombre, 'test')
        self.assertEqual(model.descripcion, 'test')
        self.assertEqual(len(model.campos), 1)
        self.assertEqual(model.campos[0].nombre, 'test')

        # Test invalid data
        with self.assertRaises(ValidationError):
            DocumentoContexto(
                nombre='test',
                descripcion='test',
                campos=[{'nombre': 'test', 'tipo': 'test', 'requerido': 'a'}]
            )


if __name__ == '__main__':
    unittest.main()
