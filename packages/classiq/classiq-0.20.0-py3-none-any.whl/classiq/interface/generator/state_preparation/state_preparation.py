from __future__ import annotations

from enum import Enum
from typing import Any, Collection, Dict, Optional, Tuple, Union

import numpy as np
import pydantic
from numpy.typing import ArrayLike

from classiq.interface.generator.preferences.optimization import (
    StatePrepOptimizationMethod,
)
from classiq.interface.generator.range_types import NonNegativeFloatRange
from classiq.interface.generator.state_preparation.state_preparation_template import (
    StatePreparationTemplate,
)
from classiq.interface.generator.validations.validator_functions import (
    validate_amplitudes,
    validate_probabilities,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticProbabilityFloat


class Metrics(str, Enum):
    KL = "KL"
    L2 = "L2"
    L1 = "L1"
    MAX_PROBABILITY = "MAX_PROBABILITY"
    LOSS_OF_FIDELITY = "LOSS_OF_FIDELITY"
    TOTAL_VARIATION = "TOTAL_VARIATION"
    HELLINGER = "HELLINGER"
    BHATTACHARYYA = "BHATTACHARYYA"

    @classmethod
    def from_sp_optimization_method(
        cls, sp_opt_method: StatePrepOptimizationMethod
    ) -> Metrics:
        try:
            return Metrics(sp_opt_method.value)
        except ValueError:
            raise ValueError(f"Failed to convert {sp_opt_method} to an error metric")


class PMF(pydantic.BaseModel):
    pmf: Tuple[PydanticProbabilityFloat, ...]
    _validate_amplitudes = pydantic.validator("pmf", allow_reuse=True)(
        validate_probabilities
    )

    class Config:
        frozen = True


class GaussianMoments(pydantic.BaseModel):
    mu: float
    sigma: pydantic.PositiveFloat

    class Config:
        frozen = True


class GaussianMixture(pydantic.BaseModel):
    gaussian_moment_list: Tuple[GaussianMoments, ...]
    num_qubits: pydantic.PositiveInt = pydantic.Field(
        description="Number of qubits for the provided state."
    )

    class Config:
        frozen = True


PossibleProbabilities = Union[PMF, GaussianMixture]

FlexiblePossibleProbabilities = Union[
    PossibleProbabilities, ArrayLike, dict, Collection[float]
]

FlexibleAmplitudes = Union[ArrayLike, Collection[float]]


class StatePreparation(StatePreparationTemplate):
    amplitudes: Optional[Tuple[float, ...]] = pydantic.Field(
        description="vector of probabilities", default=None
    )
    probabilities: Optional[PossibleProbabilities] = pydantic.Field(
        description="vector of amplitudes", default=None
    )
    error_metric: Dict[Metrics, NonNegativeFloatRange] = pydantic.Field(
        default_factory=lambda: {
            Metrics.L2: NonNegativeFloatRange(lower_bound=0, upper_bound=1e100)
        }
    )
    is_uniform_start: bool = True

    # The order of validations is important, first, the amplitudes, second the
    # probabilities and then num_qubits and error_metric.

    @pydantic.validator("amplitudes", always=True, pre=True)
    def _initialize_amplitudes(
        cls,
        amplitudes: Optional[FlexibleAmplitudes],
    ) -> Optional[Tuple[float, ...]]:
        if amplitudes is None:
            return None
        amplitudes = np.array(amplitudes).squeeze()
        if amplitudes.ndim == 1:
            return validate_amplitudes(tuple(amplitudes))

        raise ValueError(
            "Invalid amplitudes were given, please ensure the amplitude is a vector of float in the form of either tuple or list or numpy array"
        )

    @pydantic.validator("probabilities", always=True, pre=True)
    def _initialize_probabilities(
        cls,
        probabilities: Optional[FlexiblePossibleProbabilities],
    ) -> Optional[Union[PMF, GaussianMixture, dict]]:
        if probabilities is None:
            return None
        if isinstance(probabilities, PossibleProbabilities.__args__):  # type: ignore[attr-defined]
            return probabilities
        if isinstance(probabilities, dict):  # a pydantic object
            return probabilities
        probabilities = np.array(probabilities).squeeze()
        if probabilities.ndim == 1:
            return PMF(pmf=probabilities.tolist())

        raise ValueError(
            "Invalid probabilities were given, please ensure the probabilities is a vector of float in the form of either tuple or list or numpy array"
        )

    @pydantic.validator("error_metric", always=True, pre=True)
    def _validate_error_metric(
        cls, error_metric: Dict[Metrics, NonNegativeFloatRange], values: Dict[str, Any]
    ) -> Dict[Metrics, NonNegativeFloatRange]:
        if (
            values.get("amplitudes") is not None
            and error_metric is not None
            and (Metrics.KL in error_metric or Metrics.LOSS_OF_FIDELITY in error_metric)
        ):
            raise ValueError(
                "KL and LOSS_OF_FIDELITY are not supported as error metric in case of amplitudes preparation"
            )
        return error_metric

    @pydantic.root_validator
    def _validate_either_probabilities_or_amplitudes(
        cls,
        values: Dict[str, Any],
    ) -> Optional[Union[PMF, GaussianMixture, dict]]:
        amplitudes = values.get("amplitudes")
        probabilities = values.get("probabilities")
        if amplitudes is not None and probabilities is not None:
            raise ValueError(
                "StatePreparation can't get both probabilities and amplitudes"
            )
        return values

    @staticmethod
    def _non_gaussian_num_qubits(
        pmf: Optional[PMF], amplitudes: Optional[Tuple[float, ...]]
    ) -> int:
        if pmf is not None:
            return len(pmf.pmf).bit_length() - 1
        elif amplitudes is not None:
            return len(amplitudes).bit_length() - 1
        raise ValueError(
            "Can't get num_qubits without valid probabilities or amplitudes"
        )

    @property
    def num_state_qubits(self) -> int:
        if isinstance(self.probabilities, GaussianMixture):
            return self.probabilities.num_qubits
        return self._non_gaussian_num_qubits(self.probabilities, self.amplitudes)
