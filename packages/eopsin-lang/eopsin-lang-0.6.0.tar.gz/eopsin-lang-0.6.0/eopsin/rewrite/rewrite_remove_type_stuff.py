from typing import Optional

from ..util import TypedNodeTransformer
from ..typed_ast import *

"""
Inject initialising the builtin functions
"""


class RewriteRemoveTypeStuff(TypedNodeTransformer):
    def visit_Assign(self, node: TypedAssign) -> Optional[TypedAssign]:
        assert (
            len(node.targets) == 1
        ), "Assignments to more than one variable not supported yet"
        try:
            if isinstance(node.targets[0].typ, ClassType):
                # Assigning a class type to another class type is equivalent to a ClassDef - a nop
                return None
        except AttributeError:
            # untyped names (such as default class attributes) are obv fine
            pass
        return node
