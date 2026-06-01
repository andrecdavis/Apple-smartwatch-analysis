import pandas as pd
import numpy as np

import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# MAIN MODEL FUNCTION
# =========================================================

def build_price_model(
    df,
    target='price',
    include_features=None,
    exclude_features=None,
    log_transform=False,
    min_count_for_category=30,
    test_size=0.2,
    random_state=42
):
    """
    Build interpretable regression model predicting watch price.

    PARAMETERS
    ----------
    df : pandas DataFrame

    target : str
        Target variable (default = 'price')

    include_features : list or None
        Explicit list of features to use.
        If None, uses all columns except target.

    exclude_features : list or None
        Features to remove.

    log_transform : bool
        If True:
            model predicts log(price)

    min_count_for_category : int
        Rare categories grouped into 'OTHER'

    RETURNS
    -------
    results : dict
    """

    model_df = df.copy()

    # -----------------------------------------------------
    # Feature selection
    # -----------------------------------------------------

    if include_features is None:

        features = [c for c in model_df.columns if c != target]

    else:

        features = include_features.copy()

    if exclude_features is not None:

        features = [
            f for f in features
            if f not in exclude_features
        ]

    # -----------------------------------------------------
    # Keep only needed cols
    # -----------------------------------------------------

    model_df = model_df[features + [target]].copy()

    # -----------------------------------------------------
    # Drop missing
    # -----------------------------------------------------

    model_df = model_df.dropna()

    # -----------------------------------------------------
    # Handle categorical variables
    # -----------------------------------------------------

    categorical_cols = model_df.select_dtypes(
        include=['object']
    ).columns.tolist()

    # reduce sparse categories
    for col in categorical_cols:

        counts = model_df[col].value_counts()

        rare = counts[counts < min_count_for_category].index

        model_df[col] = model_df[col].replace(
            rare,
            'OTHER'
        )

    # -----------------------------------------------------
    # Log transform target
    # -----------------------------------------------------

    if log_transform:

        model_df[target] = np.log(model_df[target])

    # -----------------------------------------------------
    # One-hot encoding
    # -----------------------------------------------------

    X = pd.get_dummies(
        model_df[features],
        drop_first=True
    )

    y = model_df[target]

    # -----------------------------------------------------
    # Train/test split
    # -----------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )

    # -----------------------------------------------------
    # Statsmodels OLS
    # -----------------------------------------------------

    X_train_const = sm.add_constant(X_train)
    X_test_const = sm.add_constant(X_test)

    model = sm.OLS(
        y_train,
        X_train_const
    ).fit()

    # -----------------------------------------------------
    # Predictions
    # -----------------------------------------------------

    preds = model.predict(X_test_const)

    # undo log transform for metrics
    if log_transform:

        preds_eval = np.exp(preds)
        y_eval = np.exp(y_test)

    else:

        preds_eval = preds
        y_eval = y_test

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    r2 = r2_score(y_eval, preds_eval)

    mae = mean_absolute_error(
        y_eval,
        preds_eval
    )

    # -----------------------------------------------------
    # Feature importance
    # -----------------------------------------------------

    coef_df = pd.DataFrame({
        'feature': model.params.index,
        'coefficient': model.params.values,
        'abs_effect': np.abs(model.params.values),
        'p_value': model.pvalues.values
    })

    coef_df = coef_df.sort_values(
        'abs_effect',
        ascending=False
    )

    # remove intercept
    coef_df = coef_df[
        coef_df['feature'] != 'const'
    ]

    # -----------------------------------------------------
    # Output
    # -----------------------------------------------------

    results = {
        'model': model,
        'X_columns': X.columns.tolist(),
        'feature_importance': coef_df,
        'r2': r2,
        'mae': mae,
        'log_transform': log_transform,
        'features_used': features
    }

    return results

