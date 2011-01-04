import unittest
import tempfile
import os.path
import re


def fakefile_factory():
    from beget import File

    class FakeFile(File):

        written = 0
        content = None

        def open(self, mode='r'):
            return True

        def read(self):
            return self.content or u'mocking {{ project_name }}'

        def write(self, s):
            self.written += 1
            self.content = s

        def close(self):
            return True

    return FakeFile


class TestBeget(unittest.TestCase):

    def test_replace_in_file(self):
        import beget
        from beget import replace_in_file

        _File = fakefile_factory()
        beget.File = _File
        a = _File(tempfile.NamedTemporaryFile('r'))
        a.content = 'foobarbaz'
        content = replace_in_file(a, r'bar', 'RAB')
        self.assertEqual(a.read(), 'fooRABbaz')
        self.assertEqual(a.written, 1)

    def test_writing_secret_key(self):
        import beget
        from beget import replace_in_file
        from beget import create_secret_key
        _File = fakefile_factory()
        beget.File =_File

        a = _File(tempfile.NamedTemporaryFile('r'))
        here = os.path.dirname(__file__)
        a.content = open(os.path.join(here, 'project_template/settings.py')).read()

        secret_key = "'%s'" % create_secret_key()
        assert secret_key not in a.content
        replace_in_file(a, r"(?<=SECRET_KEY = )''", secret_key)
        assert secret_key in a.read()

    def test_secret_key(self):
        from beget import create_secret_key
        key = create_secret_key(length=10)
        self.assertEqual(len(key), 10)
        match = re.search('[^a-z0-9!@#$%^&*(\-_=+)]', key)
        assert not match, u'"%s" is not an valid key char' % match.group()

    def test_valid_name_cannot_start_with_digit(self):
        fn = get_is_valid_name()
        message = fn('321')
        assert message
        assert 'make sure the name begins' in message

    def test_valid_name_can_start_with_underscore(self):
        fn = get_is_valid_name()
        message = fn('_321')
        assert message is None

    def test_valid_name_can_start_with_letter(self):
        fn = get_is_valid_name()
        message = fn('a321')
        assert message is None


def get_is_valid_name():
    from beget import is_valid_name
    return is_valid_name
