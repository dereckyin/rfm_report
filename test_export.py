import os
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import pytest

from export import first_buy_rtn

def daysdiff(created_date, order_date):
    # return diff days
    date_format = "%Y/%m/%d"
    a = dt.datetime.strptime(created_date, date_format)
    b = dt.datetime.strptime(order_date, date_format)
    delta = abs(a - b)
    return delta.days


def test_output_file_created():
    first_buy_rtn()
    cwd = os.getcwd()
    opath = os.path.join(cwd, '首次消費取消.csv')
    assert os.path.exists(opath)

def test_input_files_read():
    cwd = os.getcwd()
    rpath = os.path.join(cwd, 'orders_rtn.csv')
    epath = os.path.join(cwd, 'customer.csv')
    assert os.path.exists(rpath)
    assert os.path.exists(epath)

def test_groupby_cust_id():
    cwd = os.getcwd()
    rpath = os.path.join(cwd, 'orders_rtn.csv')
    rfmTable = pd.read_csv(rpath, sep=',')
    firstorder = rfmTable.groupby('CUST_ID').head(1)
    assert 'CUST_ID' in firstorder.columns

def test_filter_status():
    cwd = os.getcwd()
    rpath = os.path.join(cwd, 'orders_rtn.csv')
    rfmTable = pd.read_csv(rpath, sep=',')
    firstorder = rfmTable.groupby('CUST_ID').head(1)
    firstorder_cancel = firstorder[firstorder['STATUS'] == 'R']
    assert all(firstorder_cancel['STATUS'] == 'R')

def test_calculate_days():
    cwd = os.getcwd()
    rpath = os.path.join(cwd, 'orders_rtn.csv')
    epath = os.path.join(cwd, 'customer.csv')
    rfmTable = pd.read_csv(rpath, sep=',')
    customer = pd.read_csv(epath, sep=',')
    firstorder = rfmTable.groupby('CUST_ID').head(1)
    firstorder_cancel = firstorder[firstorder['STATUS'] == 'R']
    df_order = pd.merge(firstorder_cancel, customer, on='CUST_ID', how='inner')
    df_order['DAYS'] = df_order.apply(lambda x: daysdiff(x.CRT_TIME, x.SO_TIME), axis=1)
    assert 'DAYS' in df_order.columns

def test_first_buy_rtn(mocker, tmp_path):
    # Create a test order_rtn.csv file
    test_rtn_data = {'CUST_ID': [1, 1, 2, 3, 3],
        'SO_NO': [1001, 1002, 1003, 1004, 1005],
        'TTL_SO_AMOUNT': [100, 200, 50, 75, 125],
        'SO_TIME': ['2022/01/01', '2022/02/01', '2021/11/01', '2021/12/01', '2022/02/01'],
        'STATUS': ['R', 'C', 'R', 'R', 'C']}
    test_rtn_df = pd.DataFrame(test_rtn_data)
    test_rtn_path = tmp_path / "orders_rtn.csv"
    test_rtn_df.to_csv(test_rtn_path, index=False)

    # Create a test customer.csv file
    test_cust_data = {'CUST_ID': [1, 2, 3],
        'CRT_TIME': ['2021/01/01', '2021/06/01', '2022/01/01']}
    test_cust_df = pd.DataFrame(test_cust_data)
    test_cust_path = tmp_path / "customer.csv"
    test_cust_df.to_csv(test_cust_path, index=False)

    # Run the function
    mocker.patch('os.getcwd', return_value=str(tmp_path))
    opath = tmp_path / '首次消費取消.csv'
    first_buy_rtn()

    # Load the output file and check the results
    output_df = pd.read_csv(opath, sep='\t', index_col=0)
    expected_output_data = {'2022/02': [1, 2],
                            '2022/01': [0, 0],
                            '2021/12': [0, 0],
                            '2021/11': [1, 1],
                            '2021/10': [0, 0],
                            '2021/09': [0, 0],
                            '2021/08': [0, 0],
                            '2021/07': [0, 0],
                            '2021/06': [0, 0],
                            '2021/05': [0, 0],
                            '2021/04': [0, 0]}
    expected_output_df = pd.DataFrame(expected_output_data, index=["首次消費取消會員數", "首次消費取消訂單數"])
    pd.testing.assert_frame_equal(output_df, expected_output_df)
