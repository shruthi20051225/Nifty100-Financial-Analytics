from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

result = engine.run()

print()

print("Companies Found:", len(result))