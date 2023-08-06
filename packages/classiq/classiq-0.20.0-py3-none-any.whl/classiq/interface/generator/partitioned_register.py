from dataclasses import dataclass
from typing import FrozenSet, List, Sequence, Tuple, TypeVar

from classiq.exceptions import ClassiqValueError


@dataclass(frozen=True)
class PartitionedRegister:
    name: str

    # There are num_qubits qubits within the partitions, from 0 to num_qubits-1
    num_qubits: int
    partitions: Tuple[FrozenSet[int], ...]

    def __post_init__(self) -> None:
        if not self.partitions:
            message = f"Error creating {self.name}. Must contain at least one partition"
            raise ClassiqValueError(message)

        if not all(self.partitions):
            message = f"Error creating {self.name}. Each partition must have at least one qubit"
            raise ClassiqValueError(message)

        intersection = frozenset.intersection(*self.partitions)
        if len(self.partitions) > 1 and intersection:
            message = (
                f"Overlapping partitions in {self.name}. Intersection: {intersection}"
            )
            raise ClassiqValueError(message)

        union = frozenset.union(*self.partitions)
        expected_union = frozenset(range(self.num_qubits))
        if union != expected_union:
            message = f"""Qubits missing or extra in {self.name}.
            Extra qubits: {union - expected_union}
            Missing qubits: {expected_union - union}"""
            raise ClassiqValueError(message)

    @staticmethod
    def from_partitions(
        name, partitions: Sequence[FrozenSet[int]]
    ) -> "PartitionedRegister":
        max_index = 0
        if partitions and all(partitions):
            max_index = max(max(qubit_index) for qubit_index in partitions) + 1
        return PartitionedRegister(
            name=name, partitions=tuple(partitions), num_qubits=max_index
        )

    def get_partition(self, index: int) -> "RegisterPartition":
        return RegisterPartition(self, index)


@dataclass(frozen=True)
class RegisterPartition:
    partitioned_register: PartitionedRegister
    index: int

    def __post_init__(self) -> None:
        num_partitions = len(self.partitioned_register.partitions)
        if self.index >= num_partitions or self.index < 0:
            message = f"Partition does not exist in {self.partitioned_register.name}. Index {self.index} not in range [0, {num_partitions})"
            raise ClassiqValueError(message)

    @property
    def qubits(self) -> FrozenSet[int]:
        return self.partitioned_register.partitions[self.index]


T = TypeVar("T")


def slices_to_partitions_with_payload(
    name: str, slices_with_payloads: Sequence[Tuple[slice, T]], the_range: Sequence[int]
) -> List[Tuple[RegisterPartition, T]]:
    partitions = [frozenset(the_range[slice_]) for slice_, _ in slices_with_payloads]
    x = PartitionedRegister.from_partitions(name, partitions)
    return [
        (x.get_partition(index), slice_and_payload[1])
        for index, slice_and_payload in enumerate(slices_with_payloads)
    ]
