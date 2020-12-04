import json
import re
from dataclasses import dataclass
from typing import Union, Callable, Iterator, Optional, TypeVar, Iterable, Type

T = TypeVar("T")
U = TypeVar("U")

NL = "\n"
NLNL = "\n\n"
COMMA = ","


def JSON(data: str) -> dict:
    return json.loads(data)


@dataclass
class Tokenized(Iterable[Type[T]]):
    tokenizer: Union[re.Pattern, str]
    token_type: Optional[Callable[[str], T]] = str
    data: Optional[str] = None

    def __class_getitem__(cls, params) -> "Tokenized[Type[T]]":
        if isinstance(params, str):
            params = (params,)

        tokenizer = params[0]
        return cls(tokenizer)

    def __call__(self, data: str) -> "Tokenized[Type[T]]":
        return Tokenized(self.tokenizer, self.token_type, data)

    def __iter__(self) -> Iterator[T]:
        return (self.token_type(t.strip()) for t in re.split(self.tokenizer, self.data))

    def each_token_as(self, token_type: Callable[[str], U]) -> "Tokenized[U]":
        return Tokenized(
            tokenizer=self.tokenizer, token_type=token_type, data=self.data
        )
