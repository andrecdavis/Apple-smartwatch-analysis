import re

def extract_model(text):
    text = str(text).lower()
    
    # Model Ultra
    ultra_num_match = re.search(r'ultra\s*(\d)', text)
    ultra_match = re.search(r'\bultra\b', text)
    if ultra_num_match:
        return f'Ultra {ultra_num_match.group(1).strip()}'
    if ultra_match:
        return 'Ultra 1'
    
    # Model SE
    se_num_match = re.search(r'\bse\s*(\d+)', text)
    se_match = re.search(r'\bse\b',text)
    if se_num_match:
        return f'SE {se_num_match.group(1).strip()}'
    if se_match:
        return 'SE 1'
    
    # Model Series
    series_num_match = re.search(r'\bseries\b\s*(\d+)', text)
    series_match = re.search(r'\bseries\b', text)
    s_match = re.search(r'\bs(\d+)\b|gen\s*(\d+)', text)
    watch_match = re.search(r'watch\s*(\d+)', text)
    series_zero = re.search(r'a1553|a1554|1st\s*gen', text)
    serie_match = re.search(r'serie\s*(\d+)|seri\s*(\d+)', text)
    gen_match = re.search(r'\bgen\b\s*(\d+)', text)
    if series_zero:
        return 'Series 0'
    if series_num_match:
        return f'Series {series_num_match.group(1).strip()}'
    if gen_match:
        return f'Series {gen_match.group(1).strip()}'
    if series_match:
        return 'Series 1'
    if s_match:
        return f'Series {s_match.group(1)}'
    if watch_match:
        return f'Series {watch_match.group(1)}'
    if serie_match:
        return f'Series {serie_match.group(1)}'
    return None

def extract_family(text):
    text = str(text).lower()
    
    # Ultra family 
    ultra_fam_match = re.search(r'\bultra\b', text)

    if ultra_fam_match:
        return f'Ultra'
    
    # Series family 
    series_fam_match = re.search(r'\bseries\b', text)

    if series_fam_match:
        return f'Series'
    
    # SE family 
    se_fam_match = re.search(r'\bse\b', text)

    if se_fam_match:
        return f'SE'


def add_model_col(df):
    df = df.copy()
    
    df['model'] = df['title'].apply(extract_model)
    
    bad_models = ['None', 'Series 24', 'Series 44', 'Series None', 'SE 44']

    df = df[~((df['model'].isin(bad_models)) & (df['model'].notna())  )]
    
    return df


def add_family_col(df):
    df = df.copy()
    
    df['family'] = df['model'].apply(extract_family)
    
    return df



def add_premium_cols(df):
    df = df.copy()
    
    premium_patterns = {'hermes':r'\bhermes\b',
                    'cellular':r'cellular|lte',
                    'titanium':r'\btitanium\b',
                    'gold':r'24k|24ct|24\skarat',
                    'premium_band':r'milanese|link',
                    'ceramic':r'ceramic'
                   }
    
    for col, pattern in premium_patterns.items():
        
        df[col] = (df['title']
                    .str.contains(pattern, case=False, na=False)
                    .astype(int)
                  )
        
    # All Ultra models are titanium==0
    df.loc[
        df['model'].str.contains('ultra', case=False, na=False),
        'titanium'
    ] = 0
    
    return df




def add_features(df):
    df = df.copy()
    
    df = add_premium_cols(df)
    
    return df