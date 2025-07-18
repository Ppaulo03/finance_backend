from pydantic import BaseModel, field_validator
from datetime import datetime
import pandas as pd
from pytz import timezone


class PluggyTransactionSchema(BaseModel):
    date: datetime
    amount: float
    description: str

    @field_validator("date", mode="before")
    def clean_date(cls, v):
        return (
            pd.Timestamp(v)
            .tz_convert("UTC")
            .astimezone(timezone("America/Sao_Paulo"))
            .replace(microsecond=0)
        )
