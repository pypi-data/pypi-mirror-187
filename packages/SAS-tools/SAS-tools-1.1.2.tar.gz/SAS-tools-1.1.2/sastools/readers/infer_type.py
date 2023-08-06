"""Function for infering AnIML data type from Python data types."""

from typing import Any

import numpy


def infer_type(var_to_infer: Any) -> str:
    """Infer the AnIML data type corresponding to the input variable.

    Args:
        var_to_infer (Any): Variable of which AnIML type is to be inferred.

    Raises:
        ValueError: If var_to_infer is of invalid type.

    Returns:
        str: AnIML type as specified in AnIML core schema.
    """
    if (var_to_infer == True) or (var_to_infer == False):
        if isinstance(var_to_infer, bool):
            return "Boolean"
    elif isinstance(var_to_infer, str):
        return "String"
    elif numpy.issubdtype(type(var_to_infer), numpy.int32):
        return "Int32"
    elif numpy.issubdtype(type(var_to_infer), numpy.integer):
        return "Int64"
    elif numpy.issubdtype(type(var_to_infer), numpy.float32):
        return "Float32"
    elif numpy.issubdtype(type(var_to_infer), numpy.floating):
        return "Float64"
    else:
        raise ValueError(f"{type(var_to_infer)} not a valid type.")
