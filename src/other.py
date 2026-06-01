import pandas as pd

def load_data(path='Global_Smartwatch_Marketplace.csv'):
    df = pd.read_csv(path)
    pd.set_option('display.max_colwidth', None)
    return df


def calculate_price_increase(df, feature):
    
    # Returns dollar_increase, percent_increase for gold vs retail models

    df_copy = df.copy()

    # Creates df of gold percentages

    plot_df = (
        df_copy.groupby('model')[feature]
        .mean()
        .mul(100)
        .sort_values()
        .to_frame('premium_pct')
    )

    # All models that have gold listings
    gold_list = [model for model in plot_df.index if (plot_df.loc[model, 'premium_pct'] > 0)]

    # Filter by gold models
    df_copy = df_copy[df_copy['model'].isin(gold_list)]

    df_comparison = (
        df_copy.groupby(['model', feature])['price']
        .mean()
        .unstack()
    )

    df_comparison = df_comparison.rename(columns = {0:'Retail', 1:feature })

    df_comparison['difference'] = df_comparison[feature] - df_comparison['Retail']
    df_comparison['percent'] = df_comparison[feature] / df_comparison['Retail']

    percent_increase = round((df_comparison['percent'].mean() - 1)*100, 1)
    dollar_increase = int(df_comparison['difference'].mean())

    return dollar_increase, percent_increase