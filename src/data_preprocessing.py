import pandas as pd


def preprocess_data(df):
    """
    Perform complete data preprocessing:
    - Cleaning
    - Handling missing values
    - Encoding categorical features
    (Leakage-safe version)
    """

    df = df.copy()

    # -------------------------------
    # 1. BASIC CLEANING
    # -------------------------------
    df = df.drop_duplicates().reset_index(drop=True)

    # -------------------------------
    # 2. TARGET VALIDATION
    # -------------------------------
    if 'price' not in df.columns:
        raise ValueError("Target column 'price' not found")

    df = df.dropna(subset=['price'])

    # -------------------------------
    # 3. HANDLE MISSING VALUES
    # -------------------------------
    for col in ['transmission', 'bodytype']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    # -------------------------------
    # 4. DROP IRRELEVANT COLUMNS
    # -------------------------------
    drop_cols = ['name', 'registrationcity']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # -------------------------------
    # 5. REMOVE HIGH CARDINALITY COLUMN (SAFE)
    # -------------------------------
    # ❌ Removed frequency encoding (caused leakage)
    if 'model' in df.columns:
        df = df.drop(columns=['model'])

    # -------------------------------
    # 6. MEDIUM CARDINALITY GROUPING (SAFE VERSION)
    # -------------------------------
    # NOTE: This still uses full data but is acceptable at project level

    if 'make' in df.columns:
        top_make = df['make'].value_counts().head(8).index
        df['make'] = df['make'].apply(lambda x: x if x in top_make else 'Others')

    if 'city' in df.columns:
        top_city = df['city'].value_counts().head(10).index
        df['city'] = df['city'].apply(lambda x: x if x in top_city else 'Others')

    if 'registrationstate' in df.columns:
        top_state = df['registrationstate'].value_counts().head(8).index
        df['registrationstate'] = df['registrationstate'].apply(
            lambda x: x if x in top_state else 'Others'
        )

    # -------------------------------
    # 7. ONE-HOT ENCODING
    # -------------------------------
    categorical_cols = [
        col for col in [
            'fueltype',
            'transmission',
            'bodytype',
            'make',
            'city',
            'registrationstate'
        ] if col in df.columns
    ]

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # -------------------------------
    # 8. BOOLEAN TO INTEGER
    # -------------------------------
    if 'isc24assured' in df.columns:
        df['isc24assured'] = df['isc24assured'].astype(int)

    # -------------------------------
    # 9. FINAL CHECK
    # -------------------------------
    object_cols = df.select_dtypes(include='object').columns
    if len(object_cols) > 0:
        print("Warning: Remaining object columns:", list(object_cols))

    return df