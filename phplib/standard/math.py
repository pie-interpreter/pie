import math
from pie.interpreter.function import SCALAR
from pie.interpreter.function import builtin_function
from pie.objspace import space


@builtin_function(args=[SCALAR])
def cos(context, params):
    arg = params[0].as_float()
    return space.float(math.cos(arg.value))
