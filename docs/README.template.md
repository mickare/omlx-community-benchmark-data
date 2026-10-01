# Community Benchmarks - omlx.ai

This repo contains the scraped community benchmark tables from [omlx.ai](https://omlx.ai/). Please give the author a star on the omlx GitHub repository at https://github.com/jundot/omlx.

- [`performance.parquet`](./performance.parquet) is scraped from https://omlx.ai/benchmarks/performance.
- [`intelligence.parquet`](./intelligence.parquet) is scraped from https://omlx.ai/benchmarks/intelligence (alias accuracy).

The current dataset contains data from March 2026 to September 2026.

The data is provided on a best-effort basis. No guarantees.
Most fields are strings. You will need to do additional parsing for timestamps or score values.

## Usage

Both parquet files are written with `zstd` compression using the `pyarrow` engine.

Read the parquet files with [`pandas`](https://pypi.org/project/pandas/) or any other parquet library. You will need an additional package, [`pyarrow`](https://pypi.org/project/pyarrow/) or [`fastparquet`](https://pypi.org/project/fastparquet/).
```python
import pandas as pd

df_intel = pd.read_parquet('intelligence.parquet')
df_perf = pd.read_parquet('performance.parquet')

print(df_intel.head(3))
print(df_perf.head(3))
````

## Data Quality

### Performance Data
* {{PERFORMANCE_ROWS}} rows
* {{PERFORMANCE_COLUMNS}} columns
* Note: There are not many data points between the weeks 2026-08-31 and 2026-09-14. I double checked, check yourself [here](https://omlx.ai/benchmarks/performance?cursor=WyJwZXJmb3JtYW5jZTpoaWRlX3NwZWNwcmVmaWxsPTEiLCIyMDI2LTA5LTE1IDA1OjE1OjQwIiw0NjQxMDksMiw3MDAwLDY5OTkwXQ%3D%3D&hide_specprefill=1).

![Weekly distribution of performance data](docs/distribution_performance.png)

{{PERFORMANCE_SCHEMA}}

### Intelligence Data
* {{INTELLIGENCE_ROWS}} rows
* {{INTELLIGENCE_COLUMNS}} columns

![Weekly distribution of intelligence data](docs/distribution_intelligence.png)

{{INTELLIGENCE_SCHEMA}}

## License

The website omlx.ai is licensed under `© oMLX · Apache 2.0` (see [omlx.LICENSE](omlx.LICENSE) or https://github.com/jundot/omlx/blob/main/LICENSE).
All data that has been scraped falls under the same terms and conditions.