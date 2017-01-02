from ext.ftp.manager import FTPManager
from tests.main import MainTestClass
import pytest
import os


class TestFTPManager(MainTestClass):

    @pytest.fixture
    def manager(self):
        sample_connection = ['speedtest.tele2.net', 'anonymous', 'guest']
        ftpm = FTPManager()
        ftpm.add_connection(*sample_connection, name='speedtest')
        return ftpm

    def test_download(self, manager, example_file_path):
        to_dir = os.path.dirname(example_file_path)
        files = ['100KB.zip']
        with manager.connection('speedtest') as f:
            for name in files:
                to_path = os.path.join(to_dir, name)
                if os.path.exists(to_path):
                    os.remove(to_path)
                f.download(name, to_path)
                assert os.path.exists(to_path)
                os.remove(to_path)