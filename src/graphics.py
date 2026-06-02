import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


def plot_price_density(df, model_list = [
    'ultra 3', 'series 9', 'ultra 2',
    'series 10', 'series 11',
    'ultra 1'
], save_path = None):
    
    order = model_list

    df_plot = df.copy()
    df_plot = df_plot[df_plot['model'].isin(order)]
    df_plot['model'] = pd.Categorical(df_plot['model'], categories=order, ordered=True)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 6))

    # KDE "bell curves" per model
    for model in order:
        subset = df_plot[df_plot['model'] == model]
    
        sns.kdeplot(
            data=subset,
            x='price',
            fill=True,
            alpha=0.3,
            linewidth=2,
            label=model
        )

    plt.title("Resale Price Distributions")
    plt.xlabel("Price")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    
    if save_path is not None:
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
        
    plt.show()
    

    
def plot_price_distribution(
    df,
    model_list,
    column='model',
    title='Price Distribution',
    save_path=None,
    figure_size=(16, 9),
    alpha=0.5,
    linewidth=2
):
    """
    Bell curve (KDE) plot comparing price distributions for multiple models/families.
    Layers distributions on top of each other for comparison.
    
    Parameters
    ----------
    df : pandas DataFrame
    model_list : list
        List of models or families to plot
    column : str
        Column to filter by ('model' or 'family')
    title : str
        Plot title
    save_path : str or None
        Path to save figure
    figure_size : tuple
        Figure size (width, height)
    alpha : float
        Transparency of filled areas (0-1)
    linewidth : float
        Line width for KDE curves
    """
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.set_theme(style="whitegrid")
    
    fig, ax = plt.subplots(figsize=figure_size)
    
    palette = sns.color_palette("colorblind", n_colors=len(model_list))
    
    # Sort model_list numerically if possible
    try:
        model_list = sorted(model_list, key=lambda x: int(x.split()[-1]))
    except:
        pass  # Keep original order if not numeric
    
    for i, model in enumerate(model_list):
        # Filter data for this model
        model_data = df[df[column] == model]['price'].dropna()
        
        if len(model_data) > 0:
            # Plot KDE (density curve)
            sns.kdeplot(
                model_data,
                ax=ax,
                label=model,
                color=palette[i],
                alpha=alpha,
                linewidth=linewidth,
                fill=True
            )
    
    ax.set_xlabel('Price', fontsize=14)
    ax.set_ylabel('Density', fontsize=14)
    ax.set_title(title, fontsize=18, pad=20)
    ax.tick_params(labelsize=12)
    
    # Legend
    ax.legend(
        loc='best',
        frameon=True,
        fontsize=10,
        ncol=2 if len(model_list) > 5 else 1
    )
    
    fig.tight_layout()
    
    if save_path is not None:
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    
    plt.show()    
    

def plot_resale_comparison(
    df, 
    model_list, 
    method = 'mean', 
    figure_size = (16,9), 
    save_path = None
):
    
    retail_master = {
        'series 0': 349,
        'series 1': 269,
        'series 2': 369,
        'series 3': 329,
        'series 4': 399,
        'series 5': 399,
        'se': 279,
        'series 6': 399,
        'series 7': 399,
        'series 8': 399,
        'ultra 1': 799,
        'se 2': 249,
        'series 9': 399,
        'ultra 2': 799,
        'series 10': 529,
        'series 11': 529,
        'se 3': 299,
        'ultra 3': 799
    }

    retail_prices = {model:retail_master[model] for model in model_list}


    # --- Prepare data ---
    df_plot = df.copy()
    df_plot = df_plot[df_plot['model'].isin(model_list)]
    df_plot['model'] = pd.Categorical(df_plot['model'], categories=model_list, ordered=True)

    # Mean resale
    mean_resale = df_plot.groupby('model', as_index=False)['price'].mean()
    
    # Median resale
    median_resale = df_plot.groupby('model', as_index=False)['price'].median()

    if method == 'mean':
        resale_method = mean_resale
    
    if method == 'median':
        resale_method = median_resale
    
    # Retail df
    retail_df = pd.DataFrame({
        'model': model_list,
        'retail': [retail_prices[model] for model in model_list]
    })

    sns.set_theme(style="whitegrid")
    
    # Setting Figure Size
    
    plt.figure(figsize=figure_size)
    

    # Get colors 
    palette = sns.color_palette("colorblind")

    # --- 1. Raw resale distribution (jittered) ---
    sns.stripplot(
        data=df_plot,
        x='model',
        y='price',
        jitter=0.25,
        alpha=0.35,
        color=palette[0],
        size=4
    )

    if method == 'mean':
        label_name = 'Mean resale'
    
    if method == 'median':
        label_name = 'Median resale'
    
    # --- 2. Mean/Median resale ---
    sns.scatterplot(
        data=resale_method,
        x='model',
        y='price',
        color=palette[0],
        s=120,
        label=label_name,
        zorder=5
    )

    # --- 3. Retail price ---
    sns.scatterplot(
        data=retail_df,
        x='model',
        y='retail',
        color=palette[1],
        s=120,
        label='Retail price',
        zorder=5
    )

    # --- 4. Connect means (trend line across generations) ---
    plt.plot(
        model_list,
        resale_method.set_index('model').loc[model_list]['price'].values,
        color=palette[0],
        alpha=0.5,
        linestyle='--',
        linewidth=2
    )

    # --- 5. Connect retail (baseline reference line) ---
    plt.plot(
        model_list,
        retail_df.set_index('model').loc[model_list]['retail'].values,
        color=palette[1],
        alpha=0.5,
        linewidth=2
    )

    plt.xticks(rotation=45)
    plt.ylabel("Price")
    plt.title("Retail vs Resale Prices Across Product Generations")
    plt.legend()
    plt.tight_layout()
    
    
    if save_path is not None:
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    
    plt.show()
    

    
    

    
    
    
    
#### -----------------------------------Plot by-------------------------------------------

def plot_by(
    df,
    by = 'mean',
    model_list = None,
    title = 'Average Resale Prices',
    retail_prices = None,
    save_path=None,
    y_lower=None,
    y_upper=None,
    highlight_models = None,
    highlight_labels = None,
    column = 'model',
    order = None,
    whiskers = False,
    ax=None,
    figure_size = (16,9),
    xlabel = None,
    ylabel = None
):
    """
    Horizontal bar chart of average resale prices
    for standard (non-Hermès, non-gold) models.

    Parameters
    ----------
    df : pandas DataFrame

    model_list : list or None
        Optional subset/order of models (or families if column='family')

    column : str
        Which column to group by. Default is 'model'. 
        Can also be 'family' to group by family instead.
    
    highlight_models : list or list of lists or None
        Single list: [item1, item2, ...] highlighted with one color
        List of lists: [[group1_items], [group2_items]] highlighted with different colors
    
    highlight_labels : list or None
        Labels for each highlight group (used with list of lists)
        Example: ['Current gen', 'Previous gen']
    
    y_lower and y_upper : limits for display
    """

    
    df_plot = df.copy()

    # --- Optional filtering ---
    if model_list == None:
        model_list = list(df[column].dropna().unique())
    
    if model_list is not None:
        df_plot = df_plot[df_plot[column].isin(model_list)]
        
        

    # --- Aggregate ---
    if by == 'count':
        plot_df = (
            df_plot.groupby(column)['price']
            .agg([by])
            .sort_values(by)
            .reset_index()
        )
    
    if by != 'count':
        plot_df = (
            df_plot.groupby(column)['price']
            .agg([by, 'count'])
            .sort_values(by)
            .reset_index()
        )

    # Custom ordering of bars. Default is by mean.
    if order is not None:

        plot_df[column] = pd.Categorical(
            plot_df[column],
            categories=order,
            ordered=True
        )

        plot_df = plot_df.sort_values(column)

    sns.set_theme(style="whitegrid")

    # --- Create axis only if not supplied ---
    if ax is None:
        fig, ax = plt.subplots(figsize=figure_size)
        
    else:
        fig = ax.figure

    palette = sns.color_palette("colorblind")

    # --- Highlight logic (same color, different alpha for current vs previous gen) ---
    if highlight_models is None:
        colors = [palette[0]] * len(plot_df)
        highlight_info = []
    elif isinstance(highlight_models[0], list):
        # Two (or more) highlight groups
        highlight_groups = highlight_models
        if highlight_labels is None:
            highlight_labels = [f'Group {i+1}' for i in range(len(highlight_groups))]
        
        colors = [palette[0]] * len(plot_df)
        highlight_info = []
        
        # Use the SAME color for both groups (orange/red in colorblind palette)
        color_idx = 4
        base_color = palette[color_idx]
        
        for i, group in enumerate(highlight_groups):
            # Group 0 (first list) = solid color (current gen), Groups 1+ = faded (previous gen)
            if i == 0:
                alpha = 1.0  # Solid for current gen
            else:
                alpha = 0.7  # Faded for previous gen
            
            for idx, item in enumerate(plot_df[column]):
                if item in group:
                    colors[idx] = (*base_color[:3], alpha)  # RGBA tuple with alpha embedded
            
            highlight_info.append((base_color, highlight_labels[i], alpha))
    else:
        # Single highlight list (original behavior)
        colors = [
            (*palette[4][:3], 1.0) if item in highlight_models else palette[0]
            for item in plot_df[column]
        ]
        highlight_info = [(palette[4], 'Current gen' , 1.0)]

    x = np.arange(len(plot_df))

    # ==================================================
    # CASE 1: no retail prices
    # ==================================================

    if retail_prices is None:

        ax.bar(
            x,
            plot_df[by],
            color=colors,
            edgecolor='none'
        )
        
        ax.set_xticks(x)
        ax.set_xticklabels(plot_df[column])

    # ==================================================
    # CASE 2: include retail comparison bars
    # ==================================================

    else:

        width = 0.38

        retail_low = []
        retail_high = []
        retail_mid = []

        for item in plot_df[column]:

            if item in retail_prices:

                low, high = retail_prices[item]

                retail_low.append(low)
                retail_high.append(high)
                retail_mid.append((low + high) / 2)

            else:
                retail_low.append(np.nan)
                retail_high.append(np.nan)
                retail_mid.append(np.nan)

        retail_low = np.array(retail_low)
        retail_high = np.array(retail_high)
        retail_mid = np.array(retail_mid)

        # resale bars
        ax.bar(
            x - width/2,
            plot_df[by],
            width=width,
            color=colors,
            edgecolor='none',
            label='Average resale'
        )

        # retail midpoint bars
        ax.bar(
            x + width/2,
            retail_mid,
            width=width,
            color=palette[1],
            alpha=0.85,
            label='Retail (midpoint)'
        )

        # whiskers
        if whiskers:

            ax.errorbar(
                x + width/2,
                retail_mid,
                yerr=[
                    retail_mid - retail_low,
                    retail_high - retail_mid
                ],
                fmt='none',
                ecolor='black',
                capsize=5,
                linewidth=1
            )

        ax.set_xticks(x)
        ax.set_xticklabels(plot_df[column])

    # --- Labels / title ---
    ax.set_xlabel(xlabel, fontsize = 18)
    ax.set_ylabel(ylabel, fontsize = 18)

    ax.tick_params(axis='x', rotation=45, labelsize = 15)
    ax.tick_params(axis='y', labelsize = 15)


    ax.set_title(
        title,
        pad=20,
        fontsize = 22
    )

    ax.set_ylim(y_lower, y_upper)

    # --- Combined legend ---
    from matplotlib.patches import Patch

    handles, labels = ax.get_legend_handles_labels()

    generation_handles = []

    if highlight_models is not None and isinstance(highlight_models[0], list):
        # Create legend entries for each highlight group with their alpha
        for color, label, alpha in highlight_info:
            generation_handles.append(
                Patch(facecolor=color, alpha=alpha, label=label)
            )
    elif highlight_models is not None:
        # Single highlight list
        generation_handles = [
            Patch(facecolor=palette[4], label='Current Gen')
        ]

    ax.legend(
        handles=handles + generation_handles,
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        frameon=True
    )

    fig.tight_layout()

    
    if save_path is not None:
        fig.savefig(
            save_path,
            bbox_inches='tight',
            dpi=300
        )


    if ax is None:
        plt.show()
    
    



def plot_gold_percentage(
    df,
    model_list = ['series 11', 'ultra 3', 'series 5', 'series 3', 'series 1', 'series 4', 'series 2'],
    save_path=None,
    figure_size = (16,9)
):
    """
    Plots the percentage of listings that are
    Hermès or gold-plated for each model.

    Parameters
    ----------
    df : pandas DataFrame
        Must contain columns:
        ['model', 'hermes', 'gold']

    model_list : list
        Models to include in the plot
    """

    # --- Filter models ---
    df_plot = df[df['model'].isin(model_list)].copy()

    # --- Premium flag ---
    df_plot['premium'] = (
        (df_plot['gold'] == 1)
    )

    # --- Aggregate percentages ---
    plot_df = (
        df_plot.groupby('model')['premium']
        .mean()
        .mul(100)
        .sort_values()
        .to_frame('premium_pct')
    )

    standard_list = [model for model in plot_df.index if (plot_df.loc[model, 'premium_pct'] == 0)]
    
    plot_df = plot_df.rename(
        index = {model : 'All other models' for model in standard_list}
    )
    
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=figure_size)

    palette = sns.color_palette("colorblind")

    premium_color = palette[3]
    standard_color = palette[7]

    # --- Premium first (grows rightward) ---
    ax.bar(
        plot_df.index,
        plot_df['premium_pct'],
        color=premium_color,
        label='% Gold-plated'
    )

#     # --- Standard remainder ---
#     ax.bar(
#         plot_df.index,
#         plot_df['standard_pct'],
#         left=plot_df['premium_pct'],
#         color=standard_color,
#         label='Standard listings'
#     )

    # --- Labels ---
    ax.set_xlabel('')
    ax.set_ylabel('Percent')

    ax.set_title(
    'Percent of 24k Gold-Plated Listings by Model',
    pad=35
)
    
    ax.tick_params(axis='x', rotation=45)

    ax.legend(
    loc='lower center',
    bbox_to_anchor=(0.11, 1),
    ncol=1,
    frameon=False
)

    plt.tight_layout()
    
    if save_path is not None:
        fig.savefig(
            save_path,
            bbox_inches='tight',
            dpi=300
        )
    
    plt.show()
    
    
def display_model_results(
    results,
    top_n=20,
    figsize=(10, 8),
    save_path = None
):
    """
    Display model performance + feature importance.
    """

    coef_df = results['feature_importance'].copy()

    print(f"R²:  {results['r2']:.3f}")
    print(f"MAE: ${results['mae']:,.2f}")

    # -----------------------------------------------------
    # Plot
    # -----------------------------------------------------

    plot_df = coef_df.head(top_n).copy()

    plt.figure(figsize=figsize)

    palette = sns.color_palette("colorblind")

    # Create colors list: negative = palette[8] (red), positive = palette[0] (blue)
    colors = [palette[0] if coef < 0 else palette[1] for coef in plot_df['coefficient']]

    x = range(len(plot_df))

    plt.bar(
        x,
        plot_df['coefficient'],
        color=colors,
        edgecolor='none'
    )

    plt.axhline(0, linestyle='--')

    plt.title('Largest Effects on Price')

    plt.xlabel('Feature')

    plt.ylabel('Model Coefficient')

    plt.xticks(x, plot_df['feature'], rotation=45, ha='right')

    plt.tight_layout()
    
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

    plt.show()