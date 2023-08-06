"""
General utilities
"""


# @check_types
# def summarize(df: DataFrame[Snapshot]) -> DataFrame[Summary]:
#     df[Summary.date] = df[Snapshot.timestamp].dt.date
#     return (
#         df.rename(columns={get_name_field_gen_mw(df): Summary.gen_mw})
#         .groupby([Summary.date, Snapshot.fuel], as_index=False)
#         .agg({Summary.gen_mw: "sum"})
#     )


# @check_types
# def collect_summaries(
#     time_units: List[TimeUnit], last_modified: Optional[str] = None
# ) -> DataFrame[Summary]:
#     return concat([time_unit.summary for time_unit in time_units])


# def get_end_of_last_month() -> date:
#     now = datetime.now(TZ)
#     return date(year=now.year, month=now.month, day=1) - timedelta(days=1)
