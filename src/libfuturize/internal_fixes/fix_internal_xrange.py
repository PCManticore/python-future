from __future__ import absolute_import

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name


class FixInternalXrange(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """
              power<
                 (name='xrange') trailer< '(' args=any ')' >
              rest=any* >
              """

    def start_tree(self, tree, filename):
        super(FixInternalXrange, self).start_tree(tree, filename)
        self.transformed_xranges = set()

    def finish_tree(self, tree, filename):
        self.transformed_xranges = None

    def transform(self, node, results):
        return self.transform_xrange(node, results)

    def transform_xrange(self, node, results):
        name = results["name"]
        name.replace(Name("range", prefix=name.prefix))
        # This prevents the new range call from being wrapped in a list later.
        self.transformed_xranges.add(id(node))
