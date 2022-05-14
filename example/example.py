import typing
import pandas as pd
import numpy as np

from flytekit import task, workflow

@task
def generate_normal_df(n:int, mean: float, sigma: float) -> pd.DataFrame:
    return pd.DataFrame({"numbers": np.random.normal(mean, sigma,size=n)})

@task
def compute_stats(df: pd.DataFrame) -> typing.Tuple[float, float]:
    return float(df["numbers"].mean()), float(df["numbers"].std())

@workflow
def wf(n: int = 200, mean: float = 0.0, sigma: float = 1.0) -> typing.Tuple[float, float]:
    return compute_stats(df=generate_normal_df(n=n, mean=mean, sigma=sigma))

@task
def compute_stats2(df: pd.DataFrame) -> typing.Tuple[float, float]:
    return float(df["numbers"].mean()), float(df["numbers"].std())

@workflow
def wf2(n: int = 200, mean: float = 0.0, sigma: float = 1.0) -> typing.Tuple[float, float]:
    return compute_stats2(df=generate_normal_df(n=n, mean=mean, sigma=sigma))


@workflow
def wf3(n: str = "200", mean: float = 0.0, sigma: float = 1.0) -> typing.Tuple[float, float]:
    """
    this workflow should error cause types dont make any sense
    """
    return compute_stats2(df=generate_normal_df(n=n, mean=mean, sigma=sigma))
