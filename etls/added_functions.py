def load_data_to_csv(data: pd.DataFrame):
    from datetime import datetime
    file_name = ('steam_gamesRAW_'+ str(datetime.now().date()) + "_" + str(datetime.now().time()).replace(":","_")+ '.csv')
    print(file_name)
    data.to_csv(account_name + file_name, storage_options={
        'account_key' : account_key}, index=False
    )
