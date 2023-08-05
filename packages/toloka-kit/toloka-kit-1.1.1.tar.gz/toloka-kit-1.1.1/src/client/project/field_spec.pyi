__all__ = [
    'FieldType',
    'FieldSpec',
    'BooleanSpec',
    'StringSpec',
    'IntegerSpec',
    'FloatSpec',
    'UrlSpec',
    'FileSpec',
    'CoordinatesSpec',
    'JsonSpec',
    'ArrayBooleanSpec',
    'ArrayStringSpec',
    'ArrayIntegerSpec',
    'ArrayFloatSpec',
    'ArrayUrlSpec',
    'ArrayFileSpec',
    'ArrayCoordinatesSpec',
]
import toloka.client.primitives.base
import toloka.util._extendable_enum
import typing


class FieldType(toloka.util._extendable_enum.ExtendableStrEnum):
    """An enumeration.
    """

    BOOLEAN = 'boolean'
    STRING = 'string'
    FLOAT = 'float'
    INTEGER = 'integer'
    URL = 'url'
    FILE = 'file'
    COORDINATES = 'coordinates'
    JSON = 'json'
    ARRAY_BOOLEAN = 'array_boolean'
    ARRAY_STRING = 'array_string'
    ARRAY_INTEGER = 'array_integer'
    ARRAY_FLOAT = 'array_float'
    ARRAY_URL = 'array_url'
    ARRAY_FILE = 'array_file'
    ARRAY_COORDINATES = 'array_coordinates'
    ARRAY_JSON = 'array_json'


class FieldSpec(toloka.client.primitives.base.BaseTolokaObject):
    """A base class for field specifications used in project's `input_spec` and `output_spec`
    for input and response data validation specification respectively. Use subclasses of this
    class defined below to define the data type (string, integer, URL, etc.) and specify
    validation parameters (such as string length).

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False
    ) -> None:
        """Method generated by attrs for class FieldSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]


class BooleanSpec(FieldSpec):
    """A boolean field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        allowed_values: Allowed values
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        allowed_values: typing.Optional[typing.List[bool]] = None
    ) -> None:
        """Method generated by attrs for class BooleanSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    allowed_values: typing.Optional[typing.List[bool]]


class StringSpec(FieldSpec):
    """A string field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_length: Minimum length of the string
        max_length: Maximum length of the string
        allowed_values: Allowed values
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_length: typing.Optional[int] = None,
        max_length: typing.Optional[int] = None,
        allowed_values: typing.Optional[typing.List[str]] = None
    ) -> None:
        """Method generated by attrs for class StringSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_length: typing.Optional[int]
    max_length: typing.Optional[int]
    allowed_values: typing.Optional[typing.List[str]]


class IntegerSpec(FieldSpec):
    """An integer field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        allowed_values: Allowed values
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_value: typing.Optional[int] = None,
        max_value: typing.Optional[int] = None,
        allowed_values: typing.Optional[typing.List[int]] = None
    ) -> None:
        """Method generated by attrs for class IntegerSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_value: typing.Optional[int]
    max_value: typing.Optional[int]
    allowed_values: typing.Optional[typing.List[int]]


class FloatSpec(FieldSpec):
    """An floating point field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_value: Minimum value of the number
        max_value: Maximum value of the number
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_value: typing.Optional[float] = None,
        max_value: typing.Optional[float] = None
    ) -> None:
        """Method generated by attrs for class FloatSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_value: typing.Optional[float]
    max_value: typing.Optional[float]


class UrlSpec(FieldSpec):
    """A url field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False
    ) -> None:
        """Method generated by attrs for class UrlSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]


class FileSpec(FieldSpec):
    """A file field specification (only for output data)

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False
    ) -> None:
        """Method generated by attrs for class FileSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]


class CoordinatesSpec(FieldSpec):
    """Geographical coordinates field specification, such as “53.910236,27.531110

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        current_location: put the Toloker's current coordinates in the field (true/false).
            Used in tasks for the mobile app.
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        current_location: typing.Optional[bool] = None
    ) -> None:
        """Method generated by attrs for class CoordinatesSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    current_location: typing.Optional[bool]


class JsonSpec(FieldSpec):
    """A JSON object field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False
    ) -> None:
        """Method generated by attrs for class JsonSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]


class ArrayBooleanSpec(BooleanSpec):
    """A boolean array field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        allowed_values: Allowed values
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        allowed_values: typing.Optional[typing.List[bool]] = None,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayBooleanSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    allowed_values: typing.Optional[typing.List[bool]]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]


class ArrayStringSpec(StringSpec):
    """A string array field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_length: Minimum length of the string
        max_length: Maximum length of the string
        allowed_values: Allowed values
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_length: typing.Optional[int] = None,
        max_length: typing.Optional[int] = None,
        allowed_values: typing.Optional[typing.List[str]] = None,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayStringSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_length: typing.Optional[int]
    max_length: typing.Optional[int]
    allowed_values: typing.Optional[typing.List[str]]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]


class ArrayIntegerSpec(IntegerSpec):
    """An integer array field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        allowed_values: Allowed values
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_value: typing.Optional[int] = None,
        max_value: typing.Optional[int] = None,
        allowed_values: typing.Optional[typing.List[int]] = None,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayIntegerSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_value: typing.Optional[int]
    max_value: typing.Optional[int]
    allowed_values: typing.Optional[typing.List[int]]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]


class ArrayFloatSpec(FloatSpec):
    """An floating point array field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_value: typing.Optional[float] = None,
        max_value: typing.Optional[float] = None,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayFloatSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_value: typing.Optional[float]
    max_value: typing.Optional[float]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]


class ArrayUrlSpec(UrlSpec):
    """A url array field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayUrlSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]


class ArrayFileSpec(FileSpec):
    """A file array field specification (only for output data)

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayFileSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]


class ArrayCoordinatesSpec(CoordinatesSpec):
    """Geographical coordinates array field specification

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
        current_location: put the Toloker's current coordinates in the field (true/false).
            Used in tasks for the mobile app.
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """

    def __init__(
        self,
        *,
        required: typing.Optional[bool] = True,
        hidden: typing.Optional[bool] = False,
        current_location: typing.Optional[bool] = None,
        min_size: typing.Optional[int] = None,
        max_size: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class ArrayCoordinatesSpec.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    required: typing.Optional[bool]
    hidden: typing.Optional[bool]
    current_location: typing.Optional[bool]
    min_size: typing.Optional[int]
    max_size: typing.Optional[int]
