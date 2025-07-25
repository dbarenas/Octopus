import unittest
from unittest.mock import patch
from src.prompt.classification import create_document_classification_prompt
from langchain.prompts import PromptTemplate


class TestPrompt(unittest.TestCase):

    @patch('src.prompt.classification.context_loader')
    def test_create_document_classification_prompt(self, mock_context_loader):
        # Mock the context loader
        mock_context_loader.return_value = {
            'doc1': 'desc1',
            'doc2': 'desc2'
        }

        # Call the function
        prompt = create_document_classification_prompt(documents=mock_context_loader.return_value)

        # Assert that the prompt is correct
        self.assertIsInstance(prompt, PromptTemplate)
        self.assertIn('doc1', prompt.template)
        self.assertIn('desc1', prompt.template)
        self.assertIn('doc2', prompt.template)
        self.assertIn('desc2', prompt.template)


if __name__ == '__main__':
    unittest.main()
