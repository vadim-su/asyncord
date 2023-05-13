from typing import Any, Callable, Self
from pydantic import BaseModel
from pydantic_core import CoreSchema, core_schema, SchemaValidator


class SomeStrWrap:
    __slots__ = ('_raw_value',)

    def __init__(self, raw_data: int | str) -> None:
        self._raw_value = int(raw_data)

    def build(self, _some_data: Any) -> Self:
        ...

    def some_operation(self) -> tuple[int, str]:
        ...

    @classmethod
    def validate(cls, value: str | int | Self, _) -> Self:
        if isinstance(value, (str, int)):
            return cls(value)

        if isinstance(value, cls):
            return value

        raise ValueError('Invalid value type')

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source: type[BaseModel], _handler: Callable[[Any], CoreSchema],
    ) -> CoreSchema:
        schema = core_schema.union_schema([
            core_schema.int_schema(),
            core_schema.str_schema(),
            core_schema.is_instance_schema(cls),
        ])

        return core_schema.general_after_validator_function(
            function=cls.validate,
            schema=schema,
            serialization=core_schema.to_string_ser_schema(),
        )

    def __str__(self) -> str:
        return str(self._raw_value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._raw_value})'


class TestModel(BaseModel):
    data: SomeStrWrap


for value in (1, '1', SomeStrWrap(1)):
    test_model = TestModel(data=value)
    print(test_model.model_dump_json())
    print(test_model.model_dump(mode='json'))
