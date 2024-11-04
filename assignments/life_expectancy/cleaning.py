import argparse

import pandas as pd

from life_expectancy import OUTPUT_DIR


def clean_data(region: str):
    """Reformat and clean data from eu_life_expectancy_raw.tsv

        :region: Country to filter
    """
    data = pd.read_csv(rf"{OUTPUT_DIR}\eu_life_expectancy_raw.tsv", sep="\t")
    data[["unit", "sex", "age", "region"]] = data.iloc[:, 0].str.split(",", expand=True)
    data = data.iloc[:, 1:]
    data = data.melt(id_vars=["unit", "sex", "age", "region"]).rename(columns={"variable": "year"})
    data["value"] = data.value.str.extract(r"(\d+.\d+)")
    data = data.astype({"year": int, "value": float})
    data = data[data.value.notnull()]
    data = data[data.region == region]
    data.to_csv(rf"{OUTPUT_DIR}\pt_life_expectancy.csv", index=False)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean life expectancy data")
    parser.add_argument("--region", type=str, default="PT",
                         help="Region/Country of data expectancy")
    args = parser.parse_args()
    country = args.region
    clean_data(country)
