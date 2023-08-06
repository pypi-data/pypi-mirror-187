import abc
from typing import Any, Dict, Iterable, Tuple

import pydantic

from classiq.interface.generator.arith.arithmetic_operations import (
    ArithmeticOperationParams,
    RegisterOrConst,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import get_zero_input_name

Numeric = (float, int)


class Extremum(ArithmeticOperationParams):
    left_arg: RegisterOrConst
    right_arg: RegisterOrConst

    @pydantic.root_validator(pre=True)
    def _validate_one_is_register(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        left_arg = values.get("left_arg")
        right_arg = values.get("right_arg")
        if isinstance(left_arg, Numeric) and isinstance(right_arg, Numeric):
            raise ValueError("One argument must be a register")
        if isinstance(left_arg, RegisterUserInput) and isinstance(
            right_arg, RegisterUserInput
        ):
            assert left_arg.name != right_arg.name
        if left_arg is right_arg and isinstance(left_arg, pydantic.BaseModel):
            # In case both arguments refer to the same object, copy it.
            # This prevents changes performed on one argument to affect the other.
            values["right_arg"] = left_arg.copy(deep=True)
        return values

    def _create_ios(self) -> None:
        self._inputs = dict()
        if isinstance(self.left_arg, RegisterUserInput):
            self._inputs[self.left_arg.name] = self.left_arg
        if isinstance(self.right_arg, RegisterUserInput):
            self._inputs[self.right_arg.name] = self.right_arg
        zero_input_name = get_zero_input_name(self.output_name)
        self._zero_inputs = {zero_input_name: self.result_register}
        self._outputs = {**self._inputs, **{self.output_name: self.result_register}}

    def is_inplaced(self) -> bool:
        return False

    def get_params_inplace_options(self) -> Iterable["Extremum"]:
        return ()

    @classmethod
    @abc.abstractmethod
    def _bound_calculator(cls, args: Tuple[float, ...]) -> float:
        pass

    def _get_result_register(self) -> RegisterUserInput:
        left_arg = self._arg_as_obj(self.left_arg)
        right_arg = self._arg_as_obj(self.right_arg)
        integer_part_size = max(left_arg.integer_part_size, right_arg.integer_part_size)
        fraction_places = max(left_arg.fraction_places, right_arg.fraction_places)
        required_size = integer_part_size + fraction_places
        bounds = (
            self._bound_calculator((min(left_arg.bounds), min(right_arg.bounds))),
            self._bound_calculator((max(left_arg.bounds), max(right_arg.bounds))),
        )
        return RegisterUserInput(
            size=self.output_size or required_size,
            fraction_places=fraction_places,
            is_signed=self._include_sign and min(bounds) < 0,
            name=self.output_name,
            bounds=self._legal_bounds(bounds),
        )


class Min(Extremum):
    output_name: str = "min_value"

    @classmethod
    def _bound_calculator(cls, args: Tuple[float, ...]) -> float:
        return min(args)


class Max(Extremum):
    output_name: str = "max_value"

    @classmethod
    def _bound_calculator(cls, args: Tuple[float, ...]) -> float:
        return max(args)
