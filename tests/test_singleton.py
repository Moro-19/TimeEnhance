import sys
import os

tests_folder = os.path.dirname(__file__)
project_root = os.path.join(tests_folder, '..')
src_folder = os.path.join(project_root, 'src')
full_src_path = os.path.abspath(src_folder)

sys.path.insert(0, full_src_path)

from Utils.File_manager import FileManager

class TestSingletonPattern:
    def test_singleton_returns_same_instance(self):
        fm1 = FileManager.get_instance()
        fm2 = FileManager.get_instance()
        
        assert fm1 is fm2

    def test_singleton_has_instance_attribute(self):
        assert hasattr(FileManager, '_instance')
    
    def test_singleton_instance_persists(self):
        first = FileManager.get_instance()
        first_id = id(first)
        
        second = FileManager.get_instance()
        second_id = id(second)
        
        assert first_id == second_id
    def test_singleton_multiple_calls(self):
     first_instance = FileManager.get_instance()
     for i in range(4):
         new_instance = FileManager.get_instance()
         assert new_instance is first_instance