import sys


def load_data(messages_filepath, categories_filepath):
    # read csv files
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    # merge csv files
    df = messages.merge(categories, on="id")


def clean_data(df):
    
    # create a dataframe of the 36 individual category columns
    categories = categories['categories'].str.split(";", expand=True)
    row = categories.iloc[0]

    category_colnames = row.apply(lambda x: x.split("-")[0]).tolist() 
    categories.columns = category_colnames

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: int(x[-1]))
        
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    df.drop_duplicates(inplace=True)

def save_data(df, database_filename):
    engine = create_engine('sqlite:///' + database_filepath)
    df.to_sql('Disaster_data', engine, index=False)  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()