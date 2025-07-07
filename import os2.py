if not file_exists:
    print("File doesn't exist. Creating...")
    print("Directory exists:", os.path.exists(directory))
    with open(FILE_NAME, 'w'):
        pass  # Create the file

df.to_csv(FILE_NAME, index=False)
