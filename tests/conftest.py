import pytest
import sys
import os

tests_folder = os.path.dirname(__file__)
project_root = os.path.join(tests_folder, '..')
src_folder = os.path.join(project_root, 'src')
full_src_path = os.path.abspath(src_folder)

sys.path.insert(0, full_src_path)

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def app_context():
    with app.app_context():
        yield