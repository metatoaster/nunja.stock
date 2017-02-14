# -*- coding: utf-8 -*-
import unittest
import json
from pkg_resources import resource_filename
from os import makedirs
from os.path import join
from os.path import pardir
from os.path import sep

from nunja.stock.model import fsnavtree
from calmjs.rjs.ecma import parse

from calmjs.testing.utils import mkdtemp


def _dict_clone_filtered(d, filtered=['created']):
    return {k: v for k, v in d.items() if k not in filtered}


class MiscTestCase(unittest.TestCase):

    def test_to_filetype(self):
        self.assertEqual(fsnavtree.to_filetype(0o100000), 'file')
        self.assertEqual(fsnavtree.to_filetype(0o40000), 'folder')
        self.assertEqual(fsnavtree.to_filetype(0), 'unknown')


class FSNavTreeModelTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpdir = mkdtemp(self)
        self.dummydir1 = join(self.tmpdir, 'dummydir1')
        self.dummydir2 = join(self.tmpdir, 'dummydir2')
        self.dummydir23 = join(self.tmpdir, 'dummydir2', 'dummydir3')

        makedirs(self.dummydir1)
        makedirs(self.dummydir2)
        makedirs(self.dummydir23)

        self.test_file = join(self.tmpdir, 'test_file.txt')
        self.dummydirfile1 = join(self.dummydir2, 'file1')
        self.dummydirfile2 = join(self.dummydir2, 'file2')

        with open(self.test_file, 'w') as fd:
            fd.write('test_file.txt contents')

        with open(self.dummydirfile1, 'w') as fd:
            fd.write('dummydirfile1')

        with open(self.dummydirfile2, 'w') as fd:
            fd.write('dummydirfile2')

    def tearDown(self):
        pass

    def test_base_get_filetype(self):
        self.assertEqual(fsnavtree.get_filetype(self.dummydir1), 'folder')
        self.assertEqual(fsnavtree.get_filetype(self.test_file), 'file')

    def test_base_model_initialize(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(model.id_, 'fsnav')
        self.assertEqual(len(model.active_columns), 4)
        self.assertEqual(model.cls, {})

        model = fsnavtree.Base(
            'fsnav', self.tmpdir, '/script.py?{path}', active_columns=['size'])
        self.assertEqual(len(model.active_columns), 1)

        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}', cls={
            'table': 'tbl main',
        })
        self.assertEqual(model.cls, {'table': 'tbl main'})

    def test_finalize(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(model.finalize({}), {
            'id_': 'fsnav',
            'cls': {},
            'navtree_config': '{}',
        })
        value = {'cls': {'test': 'class'}}
        self.assertEqual(model.finalize(value), {
            'id_': 'fsnav',
            'cls': {'test': 'class'},
            'navtree_config': '{}',
        })

        # apply the class directly to the model
        model.cls = {'table': 'some-table'}
        value = {'cls': {'test': 'class'}}
        self.assertEqual(model.finalize(value), {
            'id_': 'fsnav',
            'cls': {'test': 'class', 'table': 'some-table'},
            'navtree_config': '{}',
        })

        # apply the class directly to the model
        model.cls = {'table': 'some-table'}
        # the provided value has priority
        value = {'cls': {'table': 'provided'}}
        self.assertEqual(model.finalize(value), {
            'id_': 'fsnav',
            'cls': {'table': 'provided'},
            'navtree_config': '{}',
        })

    def test_finalize_config(self):
        model = fsnavtree.Base(
            'static',
            self.tmpdir, '/script.py?{path}', config={'key1': 'value1'})
        self.assertEqual(model.finalize({}), {
            'id_': 'static',
            'cls': {},
            'navtree_config': '{"key1": "value1"}',
        })

        value = {
            'id_': 'replaced',
            'cls': {'test': 'class'},
            'navtree_config': {'key2': 'value2'},
        }
        finalized = model.finalize(value)
        self.assertEqual(finalized['id_'], 'static')
        self.assertEqual(finalized['cls'], {'test': 'class'})
        self.assertEqual(json.loads(finalized['navtree_config']), {
            "key1": "value1", "key2": "value2"})

        value = {
            'cls': {'test': 'class'},
            'navtree_config': {'key1': 'alternative'},
        }
        self.assertEqual(model.finalize(value), {
            'id_': 'static',
            'cls': {'test': 'class'},
            'navtree_config': '{"key1": "alternative"}',
        })

    def test_format_uri_root(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(
            '/script.py?/',
            model.format_uri('/'),
        )

    def test_format_uri_path(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(
            '/script.py?/some/path',
            model.format_uri('/some/path'),
        )

    def test_fs_path_format_uri_root(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(
            '/script.py?/',
            model._fs_path_format_uri(self.tmpdir),
        )

    def test_fs_path_format_uri_file(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(
            '/script.py?/dummydir2/file1',
            model._fs_path_format_uri(self.dummydirfile1),
        )

    def test_fs_path_format_uri_pardir(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(
            '/script.py?/dummydir2/',
            model._fs_path_format_uri(join(self.dummydir23, pardir)),
        )

    def test_get_attrs(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(self.test_file)), {
                '@type': 'file',
                'type': 'file',
                'size': 22,
                '@id': 'test_file.txt',
                'name': 'test_file.txt',
                'href': '/script.py?/test_file.txt'
            }
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(self.dummydir1), [
                'created', 'size',
            ]), {
                '@type': 'folder',
                'type': 'folder',
                '@id': 'dummydir1',
                'name': 'dummydir1',
                'href': '/script.py?/dummydir1/'
            }
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(self.dummydirfile1)), {
                '@type': 'file',
                'type': 'file',
                'size': 13,
                '@id': 'file1',
                'name': 'file1',
                'href': '/script.py?/dummydir2/file1'
            }
        )

    def test_listdir(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        self.assertEqual(sorted(model.listdir(sep)), [])

        # No issue between this or the one with a separtor
        self.assertEqual(sorted(model.listdir(self.tmpdir)), [
            'dummydir1', 'dummydir2', 'test_file.txt'])
        self.assertEqual(sorted(model.listdir(self.tmpdir + sep)), [
            'dummydir1', 'dummydir2', 'test_file.txt'])

        self.assertEqual(sorted(model.listdir(self.dummydir1)), ['..'])

        self.assertEqual(sorted(model.listdir(self.dummydir2)), [
            '..', 'dummydir3', 'file1', 'file2'])

    def test_get_attrs_data(self):
        model = fsnavtree.Base(
            'fsnav',
            self.tmpdir, '/script.py?{path}',
            uri_template_json='/json.py{path}',
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(self.test_file)), {
                '@type': 'file',
                'type': 'file',
                'size': 22,
                '@id': 'test_file.txt',
                'name': 'test_file.txt',
                'href': '/script.py?/test_file.txt',
            }
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(self.dummydir1), [
                'created', 'size',
            ]), {
                'type': 'folder',
                '@type': 'folder',
                '@id': 'dummydir1',
                'name': 'dummydir1',
                'href': '/script.py?/dummydir1/',
                'data_href': '/json.py/dummydir1/',
            }
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(self.dummydirfile1)), {
                'type': 'file',
                '@type': 'file',
                'size': 13,
                '@id': 'file1',
                'name': 'file1',
                'href': '/script.py?/dummydir2/file1',
            }
        )

    def test_get_attrs_data_pardir(self):
        # for the case where legitimate parent dir entry is required

        model = fsnavtree.Base(
            'fsnav',
            self.tmpdir, '/script.py?{path}',
            uri_template_json='/json.py{path}',
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_attrs(
                join(self.dummydir2, pardir)
            )), {
                'type': 'folder',
                '@type': 'folder',
                'size': 0,
                '@id': '..',
                'name': '..',
                'data_href': '/json.py/',
                'href': '/script.py?/',
            }
        )

    def test_get_struct_file(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')

        self.assertEqual(
            _dict_clone_filtered(model._get_struct_file(self.test_file)[
                'result'
            ]), {
                'type': 'file',
                '@type': 'file',
                'size': 22,
                '@id': 'test_file.txt',
                'name': 'test_file.txt',
                'href': '/script.py?/test_file.txt'
            }
        )

        self.assertEqual(
            _dict_clone_filtered(model._get_struct_file(self.dummydirfile1)[
                'result'
            ]), {
                'type': 'file',
                '@type': 'file',
                'size': 13,
                '@id': 'file1',
                'name': 'file1',
                'href': '/script.py?/dummydir2/file1'
            }
        )

    def test_get_struct_dir(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')

        result = model._get_struct_dir(self.dummydir1)
        self.assertEqual(_dict_clone_filtered(result['result'], [
                'created', 'size', 'items',
            ]), {
                'type': 'folder',
                '@type': 'folder',
                '@id': 'dummydir1',
                'name': 'dummydir1',
                'href': '/script.py?/dummydir1/'
            }
        )
        self.assertEqual(len(result['result']['items']), 1)

        result = model._get_struct_dir(self.dummydir2)
        self.assertEqual(_dict_clone_filtered(result['result'], [
                'created', 'size', 'items',
            ]), {
                'type': 'folder',
                '@type': 'folder',
                '@id': 'dummydir2',
                'name': 'dummydir2',
                'href': '/script.py?/dummydir2/'
            }
        )
        self.assertEqual(len(result['result']['items']), 4)

    def test_path_to_fs_path(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        with self.assertRaises(ValueError):
            model.path_to_fs_path('welp')

        result = model.path_to_fs_path('/readme.txt')
        self.assertTrue(result.startswith(self.tmpdir))
        self.assertTrue(result.endswith('readme.txt'))

    def test_get_struct(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        with self.assertRaises(ValueError):
            model.get_struct('welp')

        missing = model.get_struct('/readme.txt')
        self.assertIn('error', missing)

    def test_get_struct_errors(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        with self.assertRaises(ValueError):
            model.get_struct('welp')

        errored = model.get_struct('/readme.txt')
        self.assertEqual(errored['error'], 'path "/readme.txt" not found')

    def test_get_struct_success(self):
        model = fsnavtree.Base('fsnav', self.tmpdir, '/script.py?{path}')
        results = model.get_struct('/test_file.txt')
        self.assertEqual(results['result']['size'], 22)
        results = model.get_struct('/dummydir2')
        self.assertEqual(len(results['result']['items']), 4)


class FSNavTreeModelMirrorTestCase(unittest.TestCase):

    def setUp(self):
        with open(resource_filename(
                'nunja.stock.tests', 'fsnavtree_examples.js')) as fd:
            self.data = json.loads(parse(fd.read()).children()[0].children(
                )[0].initializer.to_ecma())

        self.tmpdir = mkdtemp(self)
        self.dummydir2 = join(self.tmpdir, 'dummydir2')
        self.dummydir2dir = join(self.tmpdir, 'dummydir2', 'dir')
        makedirs(self.dummydir2dir)
        self.dummydirfile1 = join(self.dummydir2, 'file1')
        self.dummydirfile2 = join(self.dummydir2, 'file2')

        with open(self.dummydirfile1, 'w') as fd:
            fd.write('dummydirfile1')

        with open(self.dummydirfile2, 'w') as fd:
            fd.write('dummydirfile2')

    def test_get_struct_success_limited_columns_no_data(self):
        model = fsnavtree.Base(
            'fsnav',
            self.tmpdir, '/script.py?{path}', active_columns=[
                'name', 'type', 'size',
            ]
        )
        self.maxDiff = None
        results = model.get_struct('/dummydir2')
        self.assertEqual(results, self.data['standard rendering'][0])

    def test_get_struct_success_limited_columns_with_data(self):
        model = fsnavtree.Base(
            'fsnav',
            self.tmpdir, '/script.py?{path}',
            uri_template_json='/json.py?{path}',
            active_columns=[
                'name', 'type', 'size',
            ]
        )
        self.maxDiff = None
        results = model.get_struct('/dummydir2')
        self.assertEqual(results, self.data['configured rendering'][0])
