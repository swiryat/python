with open(FILE_NAME, 'w') as f:
    df.to_csv(f, index=False)
