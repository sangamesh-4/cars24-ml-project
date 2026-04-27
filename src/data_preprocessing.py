import pandas as pd


TOP_MAKE = ['Maruti', 'Hyundai', 'Honda', 'Mahindra', 'Toyota', 'Tata', 'Ford', 'Renault']

TOP_MODEL = [
    'Grand I10', 'Swift', 'Baleno', 'Wagon R 1.0', 'Elite I20',
    'Alto 800', 'City', 'Creta', 'Celerio', 'Ecosport',
    'Kwid', 'New  Wagon-R', 'Alto K10', 'Alto', 'Dzire'
]

TOP_CITY = ['Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']

TOP_STATE = ['Karnataka', 'Maharashtra', 'Delhi', 'Tamil Nadu', 'Telangana', 'Gujarat', 'Rajasthan', 'Uttar Pradesh']


def preprocess_data(df, training=True):

    df = df.copy()

    # Basic Cleaning
    df = df.drop_duplicates().reset_index(drop=True)

    # Target validation
    if training:
        if 'price' not in df.columns:
            raise ValueError("Target column 'price' not found")
        df = df.dropna(subset=['price'])

    # Missing values
    for col in ['transmission', 'bodytype', 'model']:
        if col in df.columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna("Unknown")

    # Drop noisy columns
    drop_cols = ['name', 'registrationcity', 'storename', 'url', 'createdDate']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # Category grouping
    if 'make' in df.columns:
        df['make'] = df['make'].apply(lambda x: x if x in TOP_MAKE else 'Others')

    if 'model' in df.columns:
        df['model'] = df['model'].apply(lambda x: x if x in TOP_MODEL else 'Others')

    if 'city' in df.columns:
        df['city'] = df['city'].apply(lambda x: x if x in TOP_CITY else 'Others')

    if 'registrationstate' in df.columns:
        df['registrationstate'] = df['registrationstate'].apply(
            lambda x: x if x in TOP_STATE else 'Others'
        )

    # One-hot encoding
    categorical_cols = [
        col for col in [
            'fueltype',
            'transmission',
            'bodytype',
            'make',
            'model',
            'city',
            'registrationstate'
        ] if col in df.columns
    ]

    if training:
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    else:
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Bool to int
    bool_cols = df.select_dtypes(include='bool').columns
    for col in bool_cols:
        df[col] = df[col].astype(int)

    if 'isc24assured' in df.columns:
        df['isc24assured'] = df['isc24assured'].astype(int)

    return df