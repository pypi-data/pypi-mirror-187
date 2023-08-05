__all__ = [
    'VariantRegistry',
    'autocast_to_enum',
    'fix_attrs_converters',
    'BaseTolokaObjectMetaclass',
    'BaseTolokaObject',
    'BaseParameters',
]
import attr._make
import enum
import typing

from toloka.util._codegen import fix_attrs_converters


E = typing.TypeVar('E', bound=enum.Enum)

class VariantRegistry:
    def __init__(
        self,
        field: str,
        enum: typing.Type[E]
    ): ...

    def register(
        self,
        type_: type,
        value: E
    ) -> type: ...

    def __getitem__(self, value: E): ...


class BaseTolokaObjectMetaclass(type):
    @staticmethod
    def __new__(
        mcs,
        name,
        bases,
        namespace,
        auto_attribs=True,
        kw_only=True,
        frozen=False,
        order=True,
        eq=True,
        **kwargs
    ): ...

    @staticmethod
    def transformer(type_: type, fields: typing.List[attr._make.Attribute]) -> typing.List[attr._make.Attribute]: ...


class BaseTolokaObject(metaclass=BaseTolokaObjectMetaclass):
    """A base class for classes representing Toloka objects.



    Subclasses of BaseTolokaObject will:
    * Automatically convert annotated attributes attributes via attrs making them optional
      if not explicitly configured otherwise
    * Skip missing optional fields during unstructuring with client's cattr converter
    """

    @staticmethod
    def __new__(
        cls,
        *args,
        **kwargs
    ):
        """Overriding new for our check to be executed before auto-generated __init__
        """
        ...

    def __getattr__(self, item): ...

    @classmethod
    def is_variant_base(cls) -> bool: ...

    @classmethod
    def is_variant_incomplete(cls) -> bool: ...

    @classmethod
    def is_variant_spec(cls) -> bool: ...

    @classmethod
    def get_variant_specs(cls) -> dict: ...

    @classmethod
    def get_spec_subclass_for_value(cls, spec_value: typing.Union[str, E] = None) -> type: ...

    def unstructure(self) -> typing.Optional[dict]: ...

    @classmethod
    def structure(cls, data: typing.Any): ...

    def to_json(self, pretty: bool = False) -> str: ...

    @classmethod
    def from_json(cls, json_str: str): ...

    def __init__(self) -> None:
        """Method generated by attrs for class BaseTolokaObject.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]


def autocast_to_enum(func: typing.Callable) -> typing.Callable:
    """Function decorator that performs str -> Enum conversion when decorated function is called

    This decorator modifies function so that every argument annotated with any subclass of Enum type (including Enum
    itself) can be passed a value of str (or any )
    """
    ...


class ExpandParametersMetaclass(BaseTolokaObjectMetaclass):
    @staticmethod
    def __new__(
        mcs,
        name,
        bases,
        namespace,
        **kwargs
    ): ...


class BaseParameters(BaseTolokaObject, metaclass=ExpandParametersMetaclass):
    class Parameters(BaseTolokaObject):
        def __init__(self) -> None:
            """Method generated by attrs for class BaseParameters.Parameters.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]

    def __init__(self, *, parameters: typing.Optional[Parameters] = None) -> None:
        """Method generated by attrs for class BaseParameters.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    parameters: typing.Optional[Parameters]
