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

df_intel = pd.read_parquet('2026-09-30_intelligence.parquet')
df_perf = pd.read_parquet('2026-09-30_performance.parquet')

print(df_intel.head(3))
print(df_perf.head(3))
````

## Data Quality

### Performance Data
* 480,618 rows
* 23 columns
* Note: There are not many data points between the weeks 2026-08-31 and 2026-09-14. I double checked, check yourself [here](https://omlx.ai/benchmarks/performance?cursor=WyJwZXJmb3JtYW5jZTpoaWRlX3NwZWNwcmVmaWxsPTEiLCIyMDI2LTA5LTE1IDA1OjE1OjQwIiw0NjQxMDksMiw3MDAwLDY5OTkwXQ%3D%3D&hide_specprefill=1).

![Weekly distribution of performance data](docs/distribution_performance.png)


|  # | Column            |  Non-Null Count | Dtype  |
| -: | ----------------- | --------------: | :----- |
|  0 | rank              | 480618 non-null | str    |
|  1 | chip              | 480618 non-null | str    |
|  2 | ram               | 480618 non-null | str    |
|  3 | model             | 480618 non-null | str    |
|  4 | quant             | 480618 non-null | str    |
|  5 | ctx               | 480618 non-null | str    |
|  6 | pp_tok_s          | 480618 non-null | str    |
|  7 | tg_tok_s          | 480618 non-null | str    |
|  8 | note              | 480618 non-null | str    |
|  9 | date              | 480618 non-null | str    |
| 10 | measurement_url   | 480618 non-null | str    |
| 11 | data_tip          | 480618 non-null | str    |
| 12 | rank_data_tip     |      0 non-null | object |
| 13 | chip_data_tip     |      0 non-null | object |
| 14 | ram_data_tip      |      0 non-null | object |
| 15 | model_data_tip    |  84213 non-null | str    |
| 16 | quant_data_tip    |      0 non-null | object |
| 17 | ctx_data_tip      |      0 non-null | object |
| 18 | pp_tok_s_data_tip |      0 non-null | object |
| 19 | tg_tok_s_data_tip |      0 non-null | object |
| 20 | note_data_tip     |  71974 non-null | str    |
| 21 | date_data_tip     | 480618 non-null | str    |
| 22 | fetched_at        | 480618 non-null | str    |

### Intelligence Data
* 13,591 rows
* 21 columns

![Weekly distribution of intelligence data](docs/distribution_intelligence.png)


|  # | Column             | Non-Null Count | Dtype  |
| -: | ------------------ | -------------: | :----- |
|  0 | rank               | 13591 non-null | str    |
|  1 | repo               | 13591 non-null | str    |
|  2 | model              | 13591 non-null | str    |
|  3 | quant              | 13591 non-null | str    |
|  4 | benchmark          | 13591 non-null | str    |
|  5 | score              | 13591 non-null | str    |
|  6 | sample             | 13591 non-null | str    |
|  7 | note               | 13591 non-null | str    |
|  8 | date               | 13591 non-null | str    |
|  9 | measurement_url    | 13591 non-null | str    |
| 10 | data_tip           | 13591 non-null | str    |
| 11 | rank_data_tip      |     0 non-null | object |
| 12 | repo_data_tip      |  9817 non-null | str    |
| 13 | model_data_tip     |  3968 non-null | str    |
| 14 | quant_data_tip     |     0 non-null | object |
| 15 | benchmark_data_tip |     0 non-null | object |
| 16 | score_data_tip     |     0 non-null | object |
| 17 | sample_data_tip    | 13591 non-null | str    |
| 18 | note_data_tip      |  8059 non-null | str    |
| 19 | date_data_tip      | 13591 non-null | str    |
| 20 | fetched_at         | 13591 non-null | str    |

## License

The website omlx.ai is licensed under `© oMLX · Apache 2.0` (see [omlx.LICENSE](omlx.LICENSE) or https://github.com/jundot/omlx/blob/main/LICENSE).
All data that has been scraped falls under the same terms and conditions.
