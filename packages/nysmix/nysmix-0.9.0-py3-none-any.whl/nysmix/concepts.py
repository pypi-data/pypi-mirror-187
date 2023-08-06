"""
general concepts
"""

from enum import Enum, auto
from typing import Dict, Set


class Timezone(Enum):
    EST = "EST"
    EDT = "EDT"


class Fuel(Enum):
    HYDRO = "Hydro"
    WIND = "Wind"
    OTHER_RENEWABLES = "Other Renewables"
    NUCLEAR = "Nuclear"
    NATURAL_GAS = "Natural Gas"
    DUAL_FUEL = "Dual Fuel"
    OTHER_FOSSIL_FUELS = "Other Fossil Fuels"


class SimpleFuel(Enum):
    FOSSIL_FUEL = "Fossil fuel"
    RENEWABLE = "Renewable"
    NUCLEAR = "Nuclear"


MEMBERS: Dict[SimpleFuel, Set[Fuel]] = {
    SimpleFuel.FOSSIL_FUEL: {Fuel.NATURAL_GAS, Fuel.DUAL_FUEL, Fuel.OTHER_FOSSIL_FUELS},
    SimpleFuel.RENEWABLE: {Fuel.HYDRO, Fuel.WIND, Fuel.OTHER_RENEWABLES},
    SimpleFuel.NUCLEAR: {Fuel.NUCLEAR},
}
