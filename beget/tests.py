import unittest
import tempfile
import os.path
import re
import fudge


def get_is_valid_name():
    from beget import is_valid_name
    return is_valid_name


class TestBeget(unittest.TestCase):

    def test_replace_in_file(self):
        from beget import replace_in_file
        with tempfile.NamedTemporaryFile('w', delete=True) as a:
            a.write('foobarbaz')
            a.seek(0)
            content = replace_in_file(a, r'bar', 'RAB')
            content = open(a.name, 'r').read()
        self.assertEqual(content, 'fooRABbaz')

    def test_writing_secret_key(self):
        from beget import replace_in_file
        from beget import create_secret_key

        secret_key = "SECRET_KEY = '%s'" % create_secret_key()

        with tempfile.NamedTemporaryFile('w', delete=True) as a:
            here = os.path.dirname(__file__)
            content = u"SECRET_KEY = ''\nFOO = '100\n\nTEST = 'useful'"
            assert secret_key not in content
            a.write(content)
            a.seek(0)
            replace_in_file(a, r"SECRET_KEY = ''", secret_key)
            a.seek(0)
            content = open(a.name, 'r').read()
            assert secret_key in content, content

    def test_secret_key(self):
        from beget import create_secret_key
        key = create_secret_key(length=10)
        self.assertEqual(len(key), 10)
        match = re.search('[^a-z0-9!@#$%^&*(\-_=+)]', key)
        assert not match, u'"%s" is not an valid key char' % match.group()

    def test_valid_name_cannot_start_with_digit(self):
        from beget import InvalidName
        fn = get_is_valid_name()
        self.assertRaises(InvalidName, fn, '321')

    def test_valid_name_can_start_with_underscore(self):
        fn = get_is_valid_name()
        message = fn('_321')
        assert message is None

    def test_valid_name_can_start_with_letter(self):
        fn = get_is_valid_name()
        message = fn('a321')
        assert message is None

    @fudge.patch('beget.beget.os')
    def test_candidate_search(self, os):
        from beget import build_file_list
        from os.path import join as _join
        output = [
            ('/tmp/foo', ['bar'], ['something.py', 'something.pyc']),
            ('/tmp/foo/bar', [], ['filename.py', 'filename.pyc']),
        ]
        (os.expects('walk').returns(output)
         .has_attr(path=fudge.Fake().expects('join').calls(_join)))
        matches = build_file_list('nope')
        self.assertEqual(['/tmp/foo/something.py',
                          '/tmp/foo/bar/filename.py'], matches)


class TestArgs(unittest.TestCase):

    @fudge.patch('beget.beget.parser')
    def test_less_then_one_arg_causes_error(self, parser):
        from beget import validate_args
        fake_args = {}, []
        parser.expects('parse_args').returns(fake_args).expects('error')
        validate_args(parser)

    @fudge.patch('beget.beget.parser')
    def test_more_than_one_arg_causes_error(self, parser):
        from beget import validate_args
        fake_args = {}, [1002, u'sring value']
        (parser.expects('parse_args')
         .returns(fake_args).expects('error'))
        validate_args(parser)

    @fudge.patch('beget.beget.parser')
    def test_one_arg_expected(self, parser):
        from beget import validate_args
        fake_args = {}, ['a']
        (parser.expects('parse_args')
         .returns(fake_args).provides('error').times_called(0))
        validate_args(parser)
