from datetime import datetime
from typing import Annotated

from pandera import Category, Field, SchemaModel
from pandera.typing import Series

from .concepts import Fuel, Timezone


class Snapshot(SchemaModel):
    timestamp: Series[datetime] = Field(alias="Time Stamp", coerce=True)
    timezone: Series[Annotated[Category, Timezone, False]] = Field(
        coerce=True, alias="Time Zone"
    )
    fuel: Series[Annotated[Category, Fuel, False]] = Field(
        alias="Fuel Category", coerce=True
    )
    gen_mw: Series[float] = Field(coerce=True, alias="Gen MW", ge=0)


# class Summary(SchemaModel):
#     date: Series[date] = Field(coerce=True)
#     fuel: Series[str] = Field(isin=[NAME[fuel] for fuel in Fuel], alias="Fuel Category")
#     gen_mw: Series[float] = Field(coerce=True)
