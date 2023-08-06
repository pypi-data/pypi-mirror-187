from __future__ import annotations

import math
from typing import List, Optional, Tuple, Union, overload

import pydantic
from typing_extensions import Literal

MAX_FRACTION_PLACES = 5
BitString = Literal["0", "1"]


# TODO This class is fundamentally broken, as it's __iter__ function disagrees with its __len__ and __getitem__
# functions. As a result, both of those code snippets do different things:
# - list(fixed_point_number)  # Iterates over fields
# - [fixed_point_number[i] for i in range(len(fixed_point_number))]  # Iterates over bits


class FixPointNumber(pydantic.BaseModel):
    float_value: float = pydantic.Field()
    max_fraction_places: int = pydantic.Field(default=MAX_FRACTION_PLACES)
    _is_signed: bool = pydantic.PrivateAttr()
    fraction_places: pydantic.NonNegativeInt = pydantic.Field(default=None)
    integer_part_size: pydantic.NonNegativeInt = pydantic.Field(default=None)
    _int_val: int = pydantic.PrivateAttr()
    _size: pydantic.PositiveInt = pydantic.PrivateAttr()

    def __init__(
        self,
        *,
        float_value: float,
        max_fraction_places: int = MAX_FRACTION_PLACES,
        fraction_places: Optional[int] = None,
        integer_part_size: Optional[int] = None,
    ) -> None:
        self._int_val, fraction_places_needed = self._get_int_representation(
            float_value=float_value, max_fraction_places=max_fraction_places
        )
        integer_part_size_needed = max(self.bit_length() - fraction_places_needed, 0)

        fraction_places = (
            fraction_places_needed if fraction_places is None else fraction_places
        )
        integer_part_size = (
            integer_part_size_needed if integer_part_size is None else integer_part_size
        )
        if self.int_val != 0:
            fraction_places = max(fraction_places, fraction_places_needed)
            integer_part_size = max(integer_part_size, integer_part_size_needed)

        max_fraction_places = max(fraction_places, max_fraction_places)
        self._int_val = math.floor(
            self.int_val * 2 ** (fraction_places - fraction_places_needed)
        )
        super().__init__(
            float_value=float_value,
            max_fraction_places=max_fraction_places,
            integer_part_size=integer_part_size,
            fraction_places=fraction_places,
        )
        self._is_signed = self.float_value < 0.0
        self._size = self.integer_part_size + self.fraction_places

    @classmethod
    def _get_int_representation(
        cls, float_value: float, max_fraction_places: int
    ) -> Tuple[int, int]:
        int_val = cls.signed_int_to_unsigned(
            int(float_value * 2**max_fraction_places)
        )
        if int_val == 0:
            return 0, 0
        bin_val = bin(int_val)[2:]
        fraction_places = max_fraction_places
        for b in reversed(bin_val):
            if b == "1" or fraction_places == 0:
                break
            fraction_places -= 1
        int_val = int_val >> (max_fraction_places - fraction_places)
        return int_val, fraction_places

    @staticmethod
    def signed_int_to_unsigned(number: int) -> int:
        """Return the integer value of a signed int if it would we read as un-signed in binary representation"""
        if number >= 0:
            return number

        not_power2 = abs(number) & (abs(number) - 1) != 0
        return number + 2 ** (number.bit_length() + 1 * not_power2)

    @staticmethod
    def _binary_to_int(bin_rep: str, is_signed: bool) -> int:
        negative_offset: int = -(2 ** len(bin_rep)) * (bin_rep[0] == "1") * is_signed
        return int(bin_rep, 2) + negative_offset

    @staticmethod
    def _binary_to_float(
        bin_rep: str, fraction_part_size: int = 0, is_signed: bool = False
    ) -> float:
        return (
            FixPointNumber._binary_to_int(bin_rep, is_signed) / 2**fraction_part_size
        )

    @staticmethod
    def binary_to_float_or_int(
        bin_rep: str, fraction_part_size: int = 0, is_signed: bool = False
    ) -> Union[float, int]:
        if fraction_part_size == 0:
            return FixPointNumber._binary_to_int(bin_rep, is_signed)
        return FixPointNumber._binary_to_float(bin_rep, fraction_part_size, is_signed)

    @property
    def is_signed(self) -> bool:
        return self._is_signed

    @property
    def int_val(self) -> int:
        return self._int_val

    def bit_length(self) -> pydantic.PositiveInt:
        return 1 if self.int_val == 0 else self.int_val.bit_length()

    @property
    def size(self) -> pydantic.PositiveInt:
        return self._size

    def __len__(self) -> pydantic.NonNegativeInt:
        return self.size

    @property
    def bin_val(self) -> str:
        bin_rep = bin(self._int_val)[2:]
        size_diff = self.size - len(bin_rep)
        extension_bit = "0" if self.float_value >= 0 else "1"
        return extension_bit * size_diff + bin_rep

    @property
    def bounds(self) -> Tuple[float, float]:
        value = self.float_value
        return value, value

    def __eq__(self, other) -> bool:
        return self.float_value == other

    def __ge__(self, other) -> bool:
        return self.float_value >= other

    def __gt__(self, other) -> bool:
        return self.float_value > other

    def __le__(self, other) -> bool:
        return self.float_value <= other

    def __lt__(self, other) -> bool:
        return self.float_value < other

    def __ne__(self, other) -> bool:
        return self.float_value != other

    @overload
    def __getitem__(self, item: int) -> BitString:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[BitString]:
        ...

    def __getitem__(self, item: Union[slice, int]) -> Union[List[BitString], BitString]:
        return [v for v in self.bin_val[::-1]][  # type: ignore[return-value]
            item
        ]  # follow qiskit convention that LSB is the top wire, bigendian

    def __neg__(self) -> FixPointNumber:
        return FixPointNumber(
            float_value=-self.float_value, max_fraction_places=self.max_fraction_places
        )

    def __float__(self) -> float:
        return self._binary_to_float(
            self.bin_val, self.fraction_places, self._is_signed
        )

    class Config:
        frozen = True
