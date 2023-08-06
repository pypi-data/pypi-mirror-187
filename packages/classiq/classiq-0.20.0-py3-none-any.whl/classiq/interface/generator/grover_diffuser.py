from typing import List

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.state_preparation import StatePreparation


class GroverDiffuser(FunctionParams):
    variables: List[RegisterUserInput]
    state_preparation: StatePreparation

    def _create_ios(self) -> None:
        self._inputs = {reg.name: reg for reg in self.variables}
        self._outputs = {reg.name: reg for reg in self.variables}

    @pydantic.validator("variables")
    def _validate_variables(
        cls, variables: List[RegisterUserInput]
    ) -> List[RegisterUserInput]:
        names = {reg.name for reg in variables}
        assert len(variables) == len(names), "Repeating names not allowed"
        return variables
