def normalize(values):
    """
    Normalize a list of numbers to [0, 1].
    """
    total = sum(values)
    for i, v in enumerate(values):
        values[i] = v / total
    return values
def load_data():
    """
    Load some numeric data.
    """
    data = [10, 20, 30]
    if len(data) > 2:
        data = sum(data)      # ⚠️ 潜在 Bug
    return data
def process():
    data = load_data()
    result = normalize(data)
    print(result)
process()
from decimal import Decimal
x=Decimal('3.4')
print(x)
print(repr(x))