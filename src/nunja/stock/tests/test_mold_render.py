# -*- coding: utf-8 -*-
import unittest
import json
from pkg_resources import resource_filename

from calmjs.rjs.ecma import parse

from nunja.core import engine


with open(resource_filename(
        'nunja.stock.tests', 'fsnavtree_examples.js')) as fd:
    data = json.loads(
        parse(fd.read()).children()[0].children()[0].initializer.to_ecma())


# TODO move these normalizing helpers between jinja2 and nunjucks to its
# own module.

def entity_name_to_number(s):
    # for turning html entity names into the numeric form that jinja2
    # escapes into (rather than the actual name like nunjucks does).
    # TODO provide a more generic solution rather than this on-demand
    # method.
    return s.replace('&quot;', '&#34;')


def reconstitute(lines):
    return '\n'.join(entity_name_to_number(s) for s in lines if s.strip())


class FSNavTreeRenderTestCase(unittest.TestCase):

    def test_render(self):
        datum = data[0]
        raw = engine.execute('nunja.stock.molds/navtree', data=datum[0])
        answer = reconstitute(datum[1])
        rendered = reconstitute(raw.splitlines())
        self.assertEqual(answer, rendered)

    def test_render_with_data(self):
        datum = data[1]
        raw = engine.execute('nunja.stock.molds/navtree', data=datum[0])
        answer = reconstitute(datum[1])
        rendered = reconstitute(raw.splitlines())
        self.assertEqual(answer, rendered)
