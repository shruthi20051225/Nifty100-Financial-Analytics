import sqlite3
import yaml
import pandas as pd


DB_PATH = "nifty100.db"


class ScreenerEngine:

    def __init__(self):

        with open(
            "config/screener_config.yaml",
            "r"
        ) as f:

            self.config = yaml.safe_load(f)

        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        query = """
        SELECT *

        FROM financial_ratios
        """

        return pd.read_sql(query, self.conn)

    def apply_filters(self):

        df = self.load_data()

        cfg = self.config

        if "return_on_equity_pct" in df.columns:

            df = df[
                df["return_on_equity_pct"] >= cfg["roe_min"]
            ]

        if "debt_to_equity" in df.columns:

            df = df[
                df["debt_to_equity"] <= cfg["de_max"]
            ]

        if "free_cash_flow_cr" in df.columns:

            df = df[
                df["free_cash_flow_cr"] >= cfg["fcf_min"]
            ]

        if "asset_turnover" in df.columns:

            df = df[
                df["asset_turnover"] >= cfg["asset_turnover_min"]
            ]

        if "operating_profit_margin_pct" in df.columns:

            df = df[
                df["operating_profit_margin_pct"] >= cfg["opm_min"]
            ]

        return df

    def add_quality_score(self, df):

        score = 0

        if "return_on_equity_pct" in df.columns:

            score += df["return_on_equity_pct"]

        if "operating_profit_margin_pct" in df.columns:

            score += df["operating_profit_margin_pct"]

        if "asset_turnover" in df.columns:

            score += df["asset_turnover"] * 10

        if "debt_to_equity" in df.columns:

            score += (1 / (df["debt_to_equity"] + 1)) * 20

        df["composite_quality_score"] = score

        df = df.sort_values(
            "composite_quality_score",
            ascending=False
        )

        return df

    def run(self):

        df = self.apply_filters()

        df = self.add_quality_score(df)

        print(df.head())

        return df


if __name__ == "__main__":

    engine = ScreenerEngine()

    engine.run()