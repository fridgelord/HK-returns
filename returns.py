import pandas as pd
import sys


def sales_df(path):
    sales = pd.read_excel(
        path,
        dtype={
          'Billing Doc':'str',
          'Item':'str',
          'SoldToCur':'str',
          'Sold-to party':'str',
          'Product':'str',
          'qt':'int',
          'alreadyReturned':'str',
        },
    )
    sales.alreadyReturned.fillna("0", inplace=True)
    sales.alreadyReturned = sales.alreadyReturned.astype(int)
    return sales


def returns_df(path):
    """ Returns dataframe from file (xlsx or csv)"""
    DTYPE = {
        "material": "str",
        "material2": "str",
        "material3": "str",
        "qt": "int",
    }
    if path[-4:] == ".csv":
        returns = pd.read_csv(
            path,
            sep=";",
            dtype=DTYPE,
        )
    elif path[-5:]:
        returns = pd.read_excel(
            path,
            dtype=DTYPE,
        )
    else:
        sys.exit(f"Path {path} is not valid, please select an xlsx or csv file")
    return returns


def parse_sales_df(sales_df, client, is_client_soldToCur):
    if is_client_soldToCur:
        available_clients = sales_df.SoldToCur.unique()
    else:
        available_clients = sales_df["Sold-to party"].unique()
    if client not in available_clients:
        sys.exit(f"There is no sales for {client}")
    if 'currentReturn' in sales_df.columns:
        sales_df['currentReturn'] = sales_df['currentReturn'].astype(int)
    else:
        sales_df['currentReturn'] = 0
    sales_df = sales_df[sales_df['SoldToCur'] == client]
    sales_df.reset_index(inplace=True)
    return sales_df


def parse_returns_df(return_df):
    for column_name in ('material', 'material2', 'material3', 'qt'):
        if column_name not in return_df.columns:
            sys.exit(f"{column_name} missing in return file")
    for column_name in ('material2', 'material3', 'comments'):
        if column_name not in return_df.columns:
            return_df[column_name] = ''
    return_df['qt'].fillna('0', inplace=True)
    return_df['qt'] = return_df['qt'].astype(int)
    return return_df


def create_returns_df(sales_df, return_df, client):
    for index, row in return_df.iterrows():
        initial = row['qt']
        if row['qt'] > 0:
            for ind, row_sales_df in sales_df.iterrows():
                if (row['qt'] > 0
                        and row_sales_df['qt'] > 0
                        and row_sales_df['Product'] in [row['material'], row['material2'], row['material3']]):
                    b = row_sales_df['qt'] + row_sales_df['alreadyReturned'] - row_sales_df['currentReturn']
                    a = min(row['qt'], b)
                    sales_df.loc[sales_df.index[ind], 'currentReturn'] += a
                    row['qt'] -= a
                    return_df.loc[return_df.index[index], 'qt'] -= a
                    if row['qt'] == 0:
                        break
            else:
                if initial == row['qt']:
                    return_df.loc[return_df.index[index], 'comments'] = "didn't buy this code"
                else:
                    return_df.loc[return_df.index[index], 'comments'] = f"{(initial - row['qt'])} can be returned, {row['qt']} left"
                print('insufficient bought', client, row['material'], row['qt'], 'pc(s) left')

    sales_df['rozmiar_bieznik'] = sales_df['Dimension'] + ' ' + sales_df['Pattern']
    sales_df = sales_df.query('currentReturn != 0')
    return sales_df


def main(sales_input_path, returns_input_path, client, is_client_soldToCur):
    sales = sales_df(sales_input_path)
    sales = parse_sales_df(sales, client, is_client_soldToCur)
    returns_input = returns_df(returns_input_path)
    returns_input = parse_returns_df(returns_input)
    returns = create_returns_df(sales, returns_input, client)
    returns.to_excel("./zwrot.xlsx", index=False)

if __name__ == "__main__":
    main(
        "./sprzedaz.xlsx",
        "./923853.csv",
        "923853",
        True
    )
