from src.screener.engine import ScreenerEngine


class PresetScreeners:

    def __init__(self):
        self.engine = ScreenerEngine()
        self.df = self.engine.load_data()

    def quality_compounder(self):

        df = self.df.copy()

        return df[
            (df["return_on_equity_pct"] > 15)
            & (df["debt_to_equity"] < 1)
            & (df["free_cash_flow_cr"] > 0)
        ]

    def value_pick(self):

        df = self.df.copy()

        if "price_to_earnings" not in df.columns:
            return df.head(0)

        return df[(df["price_to_earnings"] < 20) & (df["debt_to_equity"] < 2)]

    def growth_accelerator(self):

        df = self.df.copy()

        if "pat_cagr_5yr" not in df.columns:
            return df.head(0)

        return df[(df["pat_cagr_5yr"] > 20)]

    def dividend_champion(self):

        df = self.df.copy()

        if "dividend_payout_ratio_pct" not in df.columns:
            return df.head(0)

        return df[
            (df["dividend_payout_ratio_pct"] < 80) & (df["free_cash_flow_cr"] > 0)
        ]

    def debt_free_bluechip(self):

        df = self.df.copy()

        return df[(df["debt_to_equity"] == 0) & (df["return_on_equity_pct"] > 12)]

    def turnaround_watch(self):

        df = self.df.copy()

        if "revenue_cagr_3yr" not in df.columns:
            return df.head(0)

        return df[df["revenue_cagr_3yr"] > 10]
