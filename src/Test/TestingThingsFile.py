import pandas as pd

def get_corr():
    df = pd.DataFrame({
        'data1': [1, 2, 3, 4, 5],
        'data2': [2, 3, 4, 5, 9]
    })

    # Calculate correlation coefficient
    correlation_coefficient = df['data1'].corr(df['data2'])

    print(f"Correlation Coefficient: {correlation_coefficient}")

get_corr()