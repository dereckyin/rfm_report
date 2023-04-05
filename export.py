import cx_Oracle
import pandas as pd
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from base64 import b64decode
# from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5
import base64
from datetime import date
import pandas as pd # 引用套件並縮寫為 pd  
import os
import datetime as dt
import calendar
from dateutil.relativedelta import relativedelta

User = os.getenv("USER", default="")
Pwd = os.getenv("PWD", default="")
Db = os.getenv("DB", default=None)

d1 = os.getenv("D1", default=None)
d2 = os.getenv("D2", default=None)

def decodeBase64(data):
    return base64.b64decode(data).decode('UTF8', 'replace')

def encodeBase64(data):
    return base64.b64encode(data)

key = decodeBase64(d1)
iv = decodeBase64(d2)

def amount_level(amount):
    level = 0
    if amount > 20000:
        level = 1
    elif amount > 10000:
        level = 2
    elif amount > 8000:
        level = 3
    elif amount > 6000:
        level = 4
    elif amount > 4000:
        level = 5
    elif amount > 3500:
        level = 6
    elif amount > 3000:
        level = 7
    elif amount > 2500:
        level = 8
    elif amount > 2000:
        level = 9
    elif amount > 1500:
        level = 10
    elif amount > 1000:
        level = 11
    elif amount > 500:
        level = 12
    elif amount > 1:
        level = 13
    else:
        level = 14

    return level

def myfunc(now_date, data_date, cnt):
    level = 0
    date_format = "%Y/%m/%d"
    a = dt.datetime.strptime(now_date, date_format)
    b = dt.datetime.strptime(data_date, date_format)
    delta = a - b

    if delta.days >= 365:
        level = 1
    elif delta.days >= 270:
        level = 2
    elif delta.days >= 90 and cnt == 1:
        level = 3
    elif delta.days >= 90 and cnt > 1:
        level = 4
    elif delta.days >= 30 and cnt == 1:
        level = 5
    else:
        level = 6

    return level

def mylevel(his_amount, im_amount):
    his_level = 1
    im_level = 1

    ret_level = 1

    if his_amount >= 10000:
        his_level = 4
    elif his_amount >= 5000:
        his_level = 3
    elif his_amount >= 1:
        his_level = 2
    else:
        his_level = 1

    if im_amount >= 10000:
        im_level = 4
    elif im_amount >= 5000:
        im_level = 3
    elif im_amount >= 1:
        im_level = 2
    else:
        im_level = 1

    ret_level = his_level if his_level > im_level else im_level
    return ret_level

def myProtencial(now_date, data_date, cnt):
    level = 0
    date_format = "%Y/%m/%d"
    a = dt.datetime.strptime(now_date, date_format)
    b = dt.datetime.strptime(data_date, date_format)
    delta = a - b

    if delta.days >= 365:
        level = 1
    elif delta.days >= 270:
        level = 2
    elif delta.days >= 90 and cnt == 1:
        level = 3
    elif delta.days >= 90 and cnt > 1:
        level = 4
    elif delta.days >= 30 and cnt == 1:
        level = 5
    else:
        level = 6

    return level

def daysdiff(created_date, order_date):
    # return diff days
    date_format = "%Y/%m/%d"
    a = dt.datetime.strptime(created_date, date_format)
    b = dt.datetime.strptime(order_date, date_format)
    delta = abs(a - b)
    return delta.days

def decrypt2(second_encrypt):
    ret = second_encrypt
    if ret == "" or len(ret) < 10:
        return ret

    cwd = os.getcwd()
    if second_encrypt[ 0 : 3 ] == second_encrypt[-3:]:
        try:
            # secondary period
            second_encrypt = second_encrypt[5:]
            second_encrypt = second_encrypt[:-3]
            decode_data = b64decode(second_encrypt)
            rsa_key = RSA.importKey(open(cwd + 'key.pem', "rb").read())
            rsa_private_key = PKCS1_v1_5.new(rsa_key)
            decrypted_text = rsa_private_key.decrypt(decode_data, 'sentinel')
            d_t = b64decode(decrypted_text)
            # first period
            cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv=iv.encode("utf8"))
            ret = cipher.decrypt(d_t).decode("utf8").replace('\x00', '')
        except:
            # try decrypt first period
            ret = second_encrypt
    else:
        try:
            # try decrypt first period
            cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv=iv.encode("utf8"))
            first = cipher.decrypt(b64decode(second_encrypt)).decode("utf8").replace('\x00', '')
            ret = first
        except:
            # try decrypt first period
            ret = second_encrypt
            
    return ret


def generate_order():
    today = date.today()

    con = cx_Oracle.connect(User, Pwd, Db, encoding="UTF-8", nencoding="UTF-8")
    query = f"""
    select to_char(a.crt_time, 'YYYY/MM/DD') SO_TIME, a.cust_id CUST_ID, a.MAS_NO SO_NO, a.total_amount - a.ec_price - a.out_bonus_amt - a.trgdisc_amt TTL_SO_AMOUNT, sum(b.stk_qty) TTL_SO_QTY from order_mas   a,
    order_item  b
    WHERE
        a.pk_no = b.mas_pk_no
    AND b.cust_rtn_flg = 'N'
        AND b.status_flg = 'E'
            AND a.cust_id NOT IN ( 'CJjMsUpVZthoNnjmcikmyQ==', 'rwrp8AQs2UVgNjmlClaANQ==', 'yESIcFoDlw9bsLSgxrhT7Q==', 'Rppnd3Ew7ShvtO6CLChZcQ==',
                                   'f3mgVFLXsm15Jnnd4BNjqpvhQhFOZEofTKIPLcgDRVw=',
                                   'senxQ3p1kbVPSQOFLvIeog==', 'HQgxlps0Y0aD3yX1WhPUBpoFBIBJ1Y4fSNg9qeLrvwE=',
                                   '1BKx/siUDhZTWOyoM6BAj746qr3coEJm8OMwYbsEkxE=', 'Cde5cqfFOa474zdw6rrtJR9aqDWH8irTnoKKrgTu4+s=')
   AND to_char(a.crt_time, 'YYYYMMDD') >= '20120901'
                    AND to_char(a.crt_time, 'YYYYMMDD') < '""" + today.strftime('%Y%m') + '01' + """'
    GROUP BY
    a.CRT_TIME, a.cust_id, a.MAS_NO, a.total_amount, a.ec_price, a.out_bonus_amt, a.trgdisc_amt
    order by a.crt_time
    """   

    df_ora = pd.read_sql(query, con)
    con.close() 

    df_ora['CUST_ID'] = df_ora['CUST_ID'].apply(lambda x: decrypt2(x))

    df_ora.to_csv('orders.csv', header=True, index=None, encoding='utf-8', sep=',', mode='w')

def generate_order_rtn():
    today = date.today()

    con = cx_Oracle.connect(User, Pwd, Db, encoding="UTF-8", nencoding="UTF-8")
    query = f"""
    select to_char(a.crt_time, 'YYYY/MM/DD') SO_TIME, a.cust_id CUST_ID, a.MAS_NO SO_NO, a.total_amount - a.ec_price - a.out_bonus_amt - a.trgdisc_amt TTL_SO_AMOUNT, sum(b.stk_qty) TTL_SO_QTY, case when  b.status_flg = 'R' then 'R' when (b.cust_rtn_flg = 'Y'
        or b.status_flg = 'R') then '' end status from order_mas   a,
    order_item  b
    WHERE
        a.pk_no = b.mas_pk_no
            AND a.cust_id NOT IN ( 'CJjMsUpVZthoNnjmcikmyQ==', 'rwrp8AQs2UVgNjmlClaANQ==', 'yESIcFoDlw9bsLSgxrhT7Q==', 'Rppnd3Ew7ShvtO6CLChZcQ==',
                                   'f3mgVFLXsm15Jnnd4BNjqpvhQhFOZEofTKIPLcgDRVw=',
                                   'senxQ3p1kbVPSQOFLvIeog==', 'HQgxlps0Y0aD3yX1WhPUBpoFBIBJ1Y4fSNg9qeLrvwE=',
                                   '1BKx/siUDhZTWOyoM6BAj746qr3coEJm8OMwYbsEkxE=', 'Cde5cqfFOa474zdw6rrtJR9aqDWH8irTnoKKrgTu4+s=')
   AND to_char(a.crt_time, 'YYYYMMDD') >= '20120901'
                    AND to_char(a.crt_time, 'YYYYMMDD') < '""" + today.strftime('%Y%m') + '01' + """'
    GROUP BY
    a.CRT_TIME, a.cust_id, a.MAS_NO, a.total_amount, a.ec_price, a.out_bonus_amt, a.trgdisc_amt, case when  b.status_flg = 'R' then 'R' when (b.cust_rtn_flg = 'Y' or b.status_flg = 'R') then '' end
    order by a.crt_time
    """   

    df_ora = pd.read_sql(query, con)

    # remove same so_no but different status
    df_ora = df_ora.drop_duplicates(subset=['SO_NO'], keep='last')

    con.close() 

    df_ora['CUST_ID'] = df_ora['CUST_ID'].apply(lambda x: decrypt2(x))

    df_ora.to_csv('orders_rtn.csv', header=True, index=None, encoding='utf-8', sep=',', mode='w')

def generate_customer():
    con = cx_Oracle.connect(User, Pwd, Db, encoding="UTF-8", nencoding="UTF-8")
    query = f"""
    select cust_id, to_char(crt_time, 'YYYY/MM/DD') crt_time from customer
    order by crt_time
    """   

    df_ora = pd.read_sql(query, con)
    con.close() 

    #df_ora['CUST_ID'] = df_ora['CUST_ID'].apply(lambda x: decrypt2(x))

    df_ora.to_csv('customer.csv', header=True, index=None, encoding='utf-8', sep=',', mode='w')

def generate_customer_with_email():
    con = cx_Oracle.connect(User, Pwd, Db, encoding="UTF-8", nencoding="UTF-8")
    query = f"""
    select cust_id, to_char(crt_time, 'YYYY/MM/DD') crt_time, mail_main from customer
    order by crt_time
    """   

    df_ora = pd.read_sql(query, con)
    con.close() 

    #df_ora['CUST_ID'] = df_ora['CUST_ID'].apply(lambda x: decrypt2(x))

    df_ora.to_csv('customer_email.csv', header=True, index=None, encoding='utf-8', sep=',', mode='w')

def level():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'level.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        lastDayOfMonth = dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

        df_mask=rfmTable[(rfmTable['SO_TIME'] <= lastDayOfMonth.strftime('%Y/%m/%d'))]

        # 20210910~20210914 times two
        #df_mask.loc[(rfmTable['SO_TIME'] >= '2021/09/10') & (rfmTable['SO_TIME'] <= '2021/09/14'), ['TTL_SO_AMOUNT']] = rfmTable * 2


        df_rank = df_mask.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x), # Frequency
                                                'SO_TIME': lambda x: x.max()}) # Monetary Value

        df_rank['RANK'] = df_rank.apply(lambda x: myfunc(lastDayOfMonth.strftime('%Y/%m/%d'), x.SO_TIME, x.SO_NO), axis=1)

        df_cnt = df_rank.groupby(["RANK"]).size().reset_index(name=lastDayOfMonth.strftime('%Y/%m'))

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.merge(df_merge, df_cnt, on='RANK', how='left')

    #df_merge.columns = ['CUST_ID', 'SO_COUNT0', 'LAST_TIME0', 'RANK0', 'SO_COUNT1', 'LAST_TIME1', 'RANK1', 'SO_COUNT2', 'LAST_TIME2', 'RANK2', 'SO_COUNT3', 'LAST_TIME3', 'RANK3', 'SO_COUNT4', 'LAST_TIME4', 'RANK4', 'SO_COUNT5', 'LAST_TIME5', 'RANK5', 'SO_COUNT6', 'LAST_TIME6', 'RANK6', 'SO_COUNT7', 'LAST_TIME7', 'RANK7', 'SO_COUNT8', 'LAST_TIME8', 'RANK8', 'SO_COUNT9', 'LAST_TIME9', 'RANK9', 'SO_COUNT10', 'LAST_TIME10', 'RANK10', 'SO_COUNT11', 'LAST_TIME11', 'RANK11']
    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def first_seconde_order():
    today = date.today()
    end = today+relativedelta(months=-1)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    # get customer first order date and TTL_SO_AMOUNT,TTL_SO_QTY
    cwd = os.getcwd()
    rpath = os.path.join(cwd, 'orders.csv')
    firstpath = os.path.join(cwd, 'first_order.csv')
    secondpath = os.path.join(cwd, 'second_order.csv')
    rfmTable = pd.read_csv(rpath,  sep=',')

    firstorder = rfmTable.drop_duplicates(subset=['CUST_ID'], keep='first')
    firstorder.to_csv(firstpath, sep='\t', encoding='utf-8')

    #rfmTable[rfmTable.apply(lambda x: x.values() not in firstorder.values.tolist(), axis=1)]
    # rfmTable[rfmTable.apply(lambda x: x.values.tolist() not in firstorder.values.tolist(), axis=1)]

    # seconde_order = rfmTable.drop_duplicates(subset=['CUST_ID'], keep='first')
    # seconde_order.to_csv(secondpath, sep='\t', encoding='utf-8')

def level_cnt():
        
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'level_cnt.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        lastDayOfMonth = dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

        df_mask=rfmTable[(rfmTable['SO_TIME'] <= lastDayOfMonth.strftime('%Y/%m/%d'))]

        # for static last year
        start_od_temp = end + relativedelta(months=-12)
        end_od_temp = end + relativedelta(months=-1)
        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(end_od_temp.year, end_od_temp.month, calendar.monthrange(end_od_temp.year, end_od_temp.month)[1])


        # 20210910~20210914 times two
        #df_mask.loc[(rfmTable['SO_TIME'] >= '2021/09/10') & (rfmTable['SO_TIME'] <= '2021/09/14'), ['TTL_SO_AMOUNT']] = rfmTable * 2
        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        df_rank = df_mask.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x), 
                                                'SO_TIME': lambda x: x.max()}) 

        df_rank_order = df_order.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x)}) # count Value

        df_rank['RANK'] = df_rank.apply(lambda x: myfunc(lastDayOfMonth.strftime('%Y/%m/%d'), x.SO_TIME, x.SO_NO), axis=1)

        df_rank_merge = pd.merge(df_rank, df_rank_order, on='CUST_ID', how='outer')

        df_cnt = df_rank_merge.groupby(["RANK"])['SO_NO_y'].agg('sum').reset_index(name=end.strftime('%Y/%m'))

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.merge(df_merge, df_cnt, on='RANK', how='left')

    #df_merge.columns = ['CUST_ID', 'SO_COUNT0', 'LAST_TIME0', 'RANK0', 'SO_COUNT1', 'LAST_TIME1', 'RANK1', 'SO_COUNT2', 'LAST_TIME2', 'RANK2', 'SO_COUNT3', 'LAST_TIME3', 'RANK3', 'SO_COUNT4', 'LAST_TIME4', 'RANK4', 'SO_COUNT5', 'LAST_TIME5', 'RANK5', 'SO_COUNT6', 'LAST_TIME6', 'RANK6', 'SO_COUNT7', 'LAST_TIME7', 'RANK7', 'SO_COUNT8', 'LAST_TIME8', 'RANK8', 'SO_COUNT9', 'LAST_TIME9', 'RANK9', 'SO_COUNT10', 'LAST_TIME10', 'RANK10', 'SO_COUNT11', 'LAST_TIME11', 'RANK11']
    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def level_amount():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'level_amount.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        lastDayOfMonth = dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

        df_mask=rfmTable[(rfmTable['SO_TIME'] <= lastDayOfMonth.strftime('%Y/%m/%d'))]

        # for static last year
        start_od_temp = end + relativedelta(months=-12)
        end_od_temp = end + relativedelta(months=-1)
        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(end_od_temp.year, end_od_temp.month, calendar.monthrange(end_od_temp.year, end_od_temp.month)[1])


        # 20210910~20210914 times two
        #df_mask.loc[(rfmTable['SO_TIME'] >= '2021/09/10') & (rfmTable['SO_TIME'] <= '2021/09/14'), ['TTL_SO_AMOUNT']] = rfmTable * 2
        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        df_rank = df_mask.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x), 
                                                'SO_TIME': lambda x: x.max()}) 

        df_rank_order = df_order.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: sum(x)}) # count Value

        df_rank['RANK'] = df_rank.apply(lambda x: myfunc(lastDayOfMonth.strftime('%Y/%m/%d'), x.SO_TIME, x.SO_NO), axis=1)

        df_rank_merge = pd.merge(df_rank, df_rank_order, on='CUST_ID', how='outer')

        df_cnt = df_rank_merge.groupby(["RANK"])['TTL_SO_AMOUNT'].agg('sum').reset_index(name=end.strftime('%Y/%m'))

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.merge(df_merge, df_cnt, on='RANK', how='left')

    #df_merge.columns = ['CUST_ID', 'SO_COUNT0', 'LAST_TIME0', 'RANK0', 'SO_COUNT1', 'LAST_TIME1', 'RANK1', 'SO_COUNT2', 'LAST_TIME2', 'RANK2', 'SO_COUNT3', 'LAST_TIME3', 'RANK3', 'SO_COUNT4', 'LAST_TIME4', 'RANK4', 'SO_COUNT5', 'LAST_TIME5', 'RANK5', 'SO_COUNT6', 'LAST_TIME6', 'RANK6', 'SO_COUNT7', 'LAST_TIME7', 'RANK7', 'SO_COUNT8', 'LAST_TIME8', 'RANK8', 'SO_COUNT9', 'LAST_TIME9', 'RANK9', 'SO_COUNT10', 'LAST_TIME10', 'RANK10', 'SO_COUNT11', 'LAST_TIME11', 'RANK11']
    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def yao():
    today = date.today()
    end = today+relativedelta(months=-1)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'yao.csv')

    upath = os.path.join(cwd, 'customer.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 
    usrTable = pd.read_csv(upath, sep=',')

    # get lastest 12 month data
    for i in range(0, 12, 1):
        rpdate = NOW + relativedelta(months=-i)

        # for normal level
        if rpdate.month > 9:
            start_his = dt.date(rpdate.year-1, 8, 1)
            end_his = dt.date(rpdate.year, 7, 31)
        else:
            start_his = dt.date(rpdate.year-2, 8, 1)
            end_his = dt.date(rpdate.year-1, 7, 31)

        # for immediate level
        if rpdate.month > 9:
            start_his_im = dt.date(rpdate.year, 8, 1)
            end_his_im_temp = rpdate + relativedelta(months=-2)
            end_his_im = dt.date(end_his_im_temp.year, end_his_im_temp.month, calendar.monthrange(end_his_im_temp.year, end_his_im_temp.month)[1])
        else:
            start_his_im = dt.date(rpdate.year - 1, 8, 1)
            end_his_im_temp = rpdate + relativedelta(months=-2)
            end_his_im = dt.date(end_his_im_temp.year, end_his_im_temp.month, calendar.monthrange(end_his_im_temp.year, end_his_im_temp.month)[1])
        
        # 9月份是重新統計年度 by eric
        if rpdate.month == 9:
            start_his = start_his_im
            end_his = end_his_im
        # print month
        header_date = rpdate + relativedelta(months=-1)
        
        #rfmTable['TIME'] = rfmTable['SO_TIME'].apply(lambda x: pd.datetime.strptime(x, '%Y/%m/%d'))

        df_his = rfmTable[(rfmTable['SO_TIME'] <= end_his.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_his.strftime('%Y/%m/%d'))]
        df_im = rfmTable[(rfmTable['SO_TIME'] <= end_his_im.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_his_im.strftime('%Y/%m/%d'))]

        df_rank_his = df_his.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value
        df_rank_im = df_im.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value

        df_rank_merge = pd.merge(df_rank_his, df_rank_im, on='CUST_ID', how='outer')
        df_rank_merge.fillna(2)

        df_rank_merge['RANK'] = df_rank_merge.apply(lambda x: mylevel(x.TTL_SO_AMOUNT_x, x.TTL_SO_AMOUNT_y), axis=1)

        df_usr = usrTable[usrTable.CRT_TIME <= rpdate.strftime('%Y/%m/%d')]

        df_cnt = df_rank_merge.groupby(["RANK"]).size().reset_index(name=header_date.strftime('%Y/%m'))

        if (df_cnt.RANK == 1).any():
            df_cnt.loc[df_cnt.RANK==1, header_date.strftime('%Y/%m')] = df_usr.count()[0] - df_cnt[df_cnt.RANK != 1].sum()[1]
        else:
            df_cnt = df_cnt.append({'RANK': 1, header_date.strftime('%Y/%m'): df_usr.count()[0] - df_cnt.sum()[1]}, ignore_index=True)

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.merge(df_merge, df_cnt, on='RANK', how='left')

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def yao_cnt():
    today = date.today()
    end = today+relativedelta(months=-1)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'yao_cnt.csv')

    upath = os.path.join(cwd, 'customer.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 

    # get lastest 12 month data
    for i in range(0, 12, 1):
        rpdate = NOW + relativedelta(months=-i)

        # for normal level
        if rpdate.month > 9:
            start_his = dt.date(rpdate.year-1, 8, 1)
            end_his = dt.date(rpdate.year, 7, 31)
        else:
            start_his = dt.date(rpdate.year-2, 8, 1)
            end_his = dt.date(rpdate.year-1, 7, 31)

        # for immediate level
        if rpdate.month > 9:
            start_his_im = dt.date(rpdate.year, 8, 1)
            end_his_im_temp = rpdate + relativedelta(months=-2)
            end_his_im = dt.date(end_his_im_temp.year, end_his_im_temp.month, calendar.monthrange(end_his_im_temp.year, end_his_im_temp.month)[1])
        else:
            start_his_im = dt.date(rpdate.year - 1, 8, 1)
            end_his_im_temp = rpdate + relativedelta(months=-2)
            end_his_im = dt.date(end_his_im_temp.year, end_his_im_temp.month, calendar.monthrange(end_his_im_temp.year, end_his_im_temp.month)[1])
        
        # 9月份是重新統計年度 by eric
        if rpdate.month == 9:
            start_his = start_his_im
            end_his = end_his_im
        # print month
        header_date = rpdate + relativedelta(months=-1)

        # for static last year
        start_od_temp = rpdate + relativedelta(months=-12)
        end_od_temp = rpdate + relativedelta(months=-1)
        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(end_od_temp.year, end_od_temp.month, calendar.monthrange(end_od_temp.year, end_od_temp.month)[1])
        #rfmTable['TIME'] = rfmTable['SO_TIME'].apply(lambda x: pd.datetime.strptime(x, '%Y/%m/%d'))

        df_his = rfmTable[(rfmTable['SO_TIME'] <= end_his.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_his.strftime('%Y/%m/%d'))]
        df_im = rfmTable[(rfmTable['SO_TIME'] <= end_his_im.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_his_im.strftime('%Y/%m/%d'))]

        df_rank_his = df_his.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value
        df_rank_im = df_im.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value

        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        df_rank_his = df_his.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value
        df_rank_im = df_im.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value

        df_rank_order = df_order.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x)}) # count Value

        df_rank_merge = pd.merge(df_rank_his, df_rank_im, on='CUST_ID', how='outer')
        df_rank_merge.fillna(2)

        df_rank_merge = pd.merge(df_rank_merge, df_rank_order, on='CUST_ID', how='outer')
        df_rank_merge.fillna(3)

        df_rank_merge['RANK'] = df_rank_merge.apply(lambda x: mylevel(x.TTL_SO_AMOUNT_x, x.TTL_SO_AMOUNT_y), axis=1)

        df_cnt = df_rank_merge.groupby(['RANK'])['SO_NO'].agg('sum').reset_index(name=header_date.strftime('%Y/%m'))

        if (df_cnt.RANK == 1).any():
            df_cnt.loc[df_cnt.RANK==1, header_date.strftime('%Y/%m')] = 0
        else:
            df_cnt = df_cnt.append({'RANK': 1, header_date.strftime('%Y/%m'): 0}, ignore_index=True)

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.merge(df_merge, df_cnt, on='RANK', how='left')
            
    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def yao_amount():
    today = date.today()
    end = today+relativedelta(months=-1)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'yao_amount.csv')

    upath = os.path.join(cwd, 'customer.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 

    # get lastest 12 month data
    for i in range(0, 12, 1):
        rpdate = NOW + relativedelta(months=-i)

        # for normal level
        if rpdate.month > 9:
            start_his = dt.date(rpdate.year-1, 8, 1)
            end_his = dt.date(rpdate.year, 7, 31)
        else:
            start_his = dt.date(rpdate.year-2, 8, 1)
            end_his = dt.date(rpdate.year-1, 7, 31)

        # for immediate level
        if rpdate.month > 9:
            start_his_im = dt.date(rpdate.year, 8, 1)
            end_his_im_temp = rpdate + relativedelta(months=-2)
            end_his_im = dt.date(end_his_im_temp.year, end_his_im_temp.month, calendar.monthrange(end_his_im_temp.year, end_his_im_temp.month)[1])
        else:
            start_his_im = dt.date(rpdate.year - 1, 8, 1)
            end_his_im_temp = rpdate + relativedelta(months=-2)
            end_his_im = dt.date(end_his_im_temp.year, end_his_im_temp.month, calendar.monthrange(end_his_im_temp.year, end_his_im_temp.month)[1])
        
        # 9月份是重新統計年度 by eric
        if rpdate.month == 9:
            start_his = start_his_im
            end_his = end_his_im
        # print month
        header_date = rpdate + relativedelta(months=-1)


        # for static last year
        start_od_temp = rpdate + relativedelta(months=-12)
        end_od_temp = rpdate + relativedelta(months=-1)
        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(end_od_temp.year, end_od_temp.month, calendar.monthrange(end_od_temp.year, end_od_temp.month)[1])
        #rfmTable['TIME'] = rfmTable['SO_TIME'].apply(lambda x: pd.datetime.strptime(x, '%Y/%m/%d'))

        df_his = rfmTable[(rfmTable['SO_TIME'] <= end_his.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_his.strftime('%Y/%m/%d'))]
        df_im = rfmTable[(rfmTable['SO_TIME'] <= end_his_im.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_his_im.strftime('%Y/%m/%d'))]

        df_rank_his = df_his.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value
        df_rank_im = df_im.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value

        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        df_rank_his = df_his.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value
        df_rank_im = df_im.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: x.sum()}) # Monetary Value

        df_rank_order = df_order.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': lambda x: sum(x)}) # count Value # count Value

        df_rank_merge = pd.merge(df_rank_his, df_rank_im, on='CUST_ID', how='outer')
        df_rank_merge.fillna(2)

        df_rank_merge = pd.merge(df_rank_merge, df_rank_order, on='CUST_ID', how='outer')
        df_rank_merge.fillna(3)

        df_rank_merge['RANK'] = df_rank_merge.apply(lambda x: mylevel(x.TTL_SO_AMOUNT_x, x.TTL_SO_AMOUNT_y), axis=1)

        df_cnt = df_rank_merge.groupby(['RANK'])['TTL_SO_AMOUNT'].agg('sum').reset_index(name=header_date.strftime('%Y/%m'))

        if (df_cnt.RANK == 1).any():
            df_cnt.loc[df_cnt.RANK==1, header_date.strftime('%Y/%m')] = 0
        else:
            df_cnt = df_cnt.append({'RANK': 1, header_date.strftime('%Y/%m'): 0}, ignore_index=True)

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.merge(df_merge, df_cnt, on='RANK', how='left')

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')


def level_email():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    customer_email = os.path.join(cwd, 'level_email.csv')
    opath = os.path.join(cwd, 'level.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 
    customer_email = pd.read_csv(customer_email,  sep=',')

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        lastDayOfMonth = dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

        df_mask=rfmTable[(rfmTable['SO_TIME'] <= lastDayOfMonth.strftime('%Y/%m/%d'))]

        # 20210910~20210914 times two
        #df_mask.loc[(rfmTable['SO_TIME'] >= '2021/09/10') & (rfmTable['SO_TIME'] <= '2021/09/14'), ['TTL_SO_AMOUNT']] = rfmTable * 2


        df_rank = df_mask.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x), # Frequency
                                                'SO_TIME': lambda x: x.max()}) # Monetary Value

        df_rank['RANK'] = df_rank.apply(lambda x: myfunc(lastDayOfMonth.strftime('%Y/%m/%d'), x.SO_TIME, x.SO_NO), axis=1)

        # get df_rank['RANK'] = 4
        df_rank = df_rank[df_rank['RANK'] == 4]
        # join customer_email
        df_rank = pd.merge(df_rank, customer_email, on='CUST_ID', how='left')
        # get 2000 random emails from df_rank
        df_rank = df_rank.sample(n=2000)

        df_rank.to_csv(opath, sep='\t', encoding='utf-8')

        break

def get_level_protencial_email():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'protencial.csv')
    epath = os.path.join(cwd, 'customer_email.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 

    cust_email = pd.read_csv(epath, sep=',')

    # get lastest 12 month data
    for i in range(0, 1, 1):
        end = NOW+relativedelta(months=-i)
        lastDayOfMonth = dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

        df_mask=rfmTable[(rfmTable['SO_TIME'] <= lastDayOfMonth.strftime('%Y/%m/%d'))]

        # for static last year
        start_od_temp = end + relativedelta(months=-12)
        end_od_temp = end + relativedelta(months=-1)
        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(end_od_temp.year, end_od_temp.month, calendar.monthrange(end_od_temp.year, end_od_temp.month)[1])


        # 20210910~20210914 times two
        #df_mask.loc[(rfmTable['SO_TIME'] >= '2021/09/10') & (rfmTable['SO_TIME'] <= '2021/09/14'), ['TTL_SO_AMOUNT']] = rfmTable * 2
        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]


        df_rank = df_mask.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x), # Frequency
                                                'SO_TIME': lambda x: x.max()}) # Monetary Value
        
        df_rank_order = df_order.groupby('CUST_ID').agg({'SO_NO': lambda x: len(x)}) # count Value

        df_rank['RANK'] = df_rank.apply(lambda x: myProtencial(lastDayOfMonth.strftime('%Y/%m/%d'), x.SO_TIME, x.SO_NO), axis=1)

        df_rank_merge = pd.merge(df_rank, df_rank_order, on='CUST_ID', how='outer')

        # filter df_rank_merge['RANK'] == 1
        df_rank_merge = df_rank_merge[df_rank_merge['RANK'] == 3]
      
        df_rank_merge = pd.merge(df_rank_merge, cust_email, on='CUST_ID', how='inner')

        # get only email field
        df_rank_merge = df_rank_merge[['MAIL_MAIN']]

        # select distinct email
        df_rank_merge = df_rank_merge.drop_duplicates(subset=['MAIL_MAIN'], keep='first')

        df_rank_merge.to_csv(opath, sep='\t', encoding='utf-8')


def second_buy():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()
    rpath = os.path.join(cwd, 'orders.csv')
    epath = os.path.join(cwd, 'first_order.csv')

    opath = os.path.join(cwd, '二次消費.csv')

    orders = pd.read_csv(rpath,  sep=',')
    firstorder = pd.read_csv(epath,  sep='\t')

    first_two_order = orders.groupby('CUST_ID').head(2)

    counts = first_two_order['CUST_ID'].value_counts()

    first_two_order = first_two_order[~first_two_order['CUST_ID'].isin(counts[counts == 1].index)]

    secondorder = first_two_order.groupby('CUST_ID').tail(1)
    rfmTable = pd.merge(secondorder, firstorder, on='CUST_ID', how='inner')

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        # for static last year
        start_od_temp = end

        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(start_od_temp.year, start_od_temp.month, calendar.monthrange(start_od_temp.year, start_od_temp.month)[1])

        header_date = end + relativedelta(months=0)
        # header_date get year and month
        header_date = header_date.strftime('%Y/%m')

        df_order = rfmTable[(rfmTable['SO_TIME_x'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME_x'] >= start_od.strftime('%Y/%m/%d'))]

        df_order['DAYS'] = df_order.apply(lambda x: daysdiff(x.SO_TIME_x, x.SO_TIME_y), axis=1)

        df_cnt = pd.DataFrame({
            header_date: [0, 0, 0, 0, 0, 0, 0],
        }, index=["二次消費會員數", "二次消費總金額", "二次消費回購天數(min)", "二次消費回購天數(25%)", "二次消費回購天數(50%)", "二次消費回購天數(75%)", "二次消費回購天數(max)"])
        # new dataframe first row save the count of df_order
        df_cnt.at['二次消費會員數', header_date] = df_order["SO_NO_x"].count()
        #df_cnt second row save the total amount of df_order['TTL_SO_AMOUNT']
        df_cnt.at['二次消費總金額', header_date] = df_order['TTL_SO_AMOUNT_x'].sum()
        #df_cnt third row save the QUARTILE of df_order['DAYS']
        df_cnt.at['二次消費回購天數(min)', header_date] = df_order['DAYS'].quantile(q=0.0)
        df_cnt.at['二次消費回購天數(25%)', header_date] = df_order['DAYS'].quantile(q=0.25).round(0)
        df_cnt.at['二次消費回購天數(50%)', header_date] = df_order['DAYS'].quantile(q=0.50).round(0)
        df_cnt.at['二次消費回購天數(75%)', header_date] = df_order['DAYS'].quantile(q=0.75).round(0)
        df_cnt.at['二次消費回購天數(max)', header_date] = df_order['DAYS'].quantile(q=1.0)

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.concat([df_merge, df_cnt], axis=1)

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def first_buy():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'first_order.csv')
    epath = os.path.join(cwd, 'customer.csv')

    opath = os.path.join(cwd, '首次消費.csv')

    rfmTable = pd.read_csv(rpath,  sep='\t') 
    customer = pd.read_csv(epath, sep=',')

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        # for static last year
        start_od_temp = end

        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(start_od_temp.year, start_od_temp.month, calendar.monthrange(start_od_temp.year, start_od_temp.month)[1])

        header_date = end + relativedelta(months=0)
        # header_date get year and month
        header_date = header_date.strftime('%Y/%m')

        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        df_order = pd.merge(df_order, customer, on='CUST_ID', how='inner')

        df_order['DAYS'] = df_order.apply(lambda x: daysdiff(x.CRT_TIME, x.SO_TIME), axis=1)

        df_cnt = pd.DataFrame({
            header_date: [0, 0, 0, 0, 0, 0, 0],
        }, index=["首次消費會員數", "首次消費總金額", "首次消費天數(min)", "首次消費天數(25%)", "首次消費天數(50%)", "首次消費天數(75%)", "首次消費天數(max)"])
        # new dataframe first row save the count of df_order
        df_cnt.at['首次消費會員數', header_date] = df_order["SO_NO"].count()
        #df_cnt second row save the total amount of df_order['TTL_SO_AMOUNT']
        df_cnt.at['首次消費總金額', header_date] = df_order['TTL_SO_AMOUNT'].sum()
        #df_cnt third row save the QUARTILE of df_order['DAYS']
        df_cnt.at['首次消費天數(min)', header_date] = df_order['DAYS'].quantile(q=0.0)
        df_cnt.at['首次消費天數(25%)', header_date] = df_order['DAYS'].quantile(q=0.25).round(0)
        df_cnt.at['首次消費天數(50%)', header_date] = df_order['DAYS'].quantile(q=0.50).round(0)
        df_cnt.at['首次消費天數(75%)', header_date] = df_order['DAYS'].quantile(q=0.75).round(0)
        df_cnt.at['首次消費天數(max)', header_date] = df_order['DAYS'].quantile(q=1.0)

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.concat([df_merge, df_cnt], axis=1)

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def first_buy_rtn():
    today = date.today()
    end = today+relativedelta(months=-2)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders_rtn.csv')
    epath = os.path.join(cwd, 'customer.csv')

    opath = os.path.join(cwd, '首次消費取消.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 
    customer = pd.read_csv(epath, sep=',')

    firstorder = rfmTable.groupby('CUST_ID').head(1)
    # get row of firstorder STATUS = 'R'
    firstorder_cancel = firstorder[firstorder['STATUS'] == 'R']

    # get lastest 12 month data
    for i in range(0, 12, 1):
        end = NOW+relativedelta(months=-i)
        # for static last year
        start_od_temp = end

        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(start_od_temp.year, start_od_temp.month, calendar.monthrange(start_od_temp.year, start_od_temp.month)[1])

        header_date = end + relativedelta(months=0)
        # header_date get year and month
        header_date = header_date.strftime('%Y/%m')

        df_order = firstorder_cancel[(firstorder_cancel['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (firstorder_cancel['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        df_order = pd.merge(df_order, customer, on='CUST_ID', how='inner')

        df_order['DAYS'] = df_order.apply(lambda x: daysdiff(x.CRT_TIME, x.SO_TIME), axis=1)

        df_cnt = pd.DataFrame({
            header_date: [0, 0],
        }, index=["首次消費取消會員數", "首次消費取消訂單數"])
        # new dataframe first row save the count of df_order
        df_cnt.at['首次消費取消會員數', header_date] = df_order["CUST_ID"].count()
        #df_cnt second row save the total amount of df_order['TTL_SO_AMOUNT']
        df_cnt.at['首次消費取消訂單數', header_date] = df_order['SO_NO'].count()

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.concat([df_merge, df_cnt], axis=1)

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def cust_season_buy():
    today = date.today()
    end = today+relativedelta(months=-1)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'seasonly.csv')

    # upath = os.path.join(cwd, 'customer.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 
    # usrTable = pd.read_csv(upath, sep=',')

    # get latest four season data
    for i in range(0, 4, 1):
        end = NOW+relativedelta(months=-i*3)
        # for static last year
        start_od_temp = end

        start_od = dt.date(start_od_temp.year, start_od_temp.month, 1)
        end_od = dt.date(start_od_temp.year, start_od_temp.month, calendar.monthrange(start_od_temp.year, start_od_temp.month)[1])

        header_date = end + relativedelta(months=0)
        # header_date get year and month
        header_date = header_date.strftime('%Y/%m')

        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        # SUM TTL_SO_AMOUNT by CUST_ID
        df_order = df_order.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': 'sum'})

        df_order['RANK'] = df_order.apply(lambda x: amount_level( x.TTL_SO_AMOUNT), axis=1)
        
        # get count of each level as a row
        df_cnt = pd.DataFrame({
            header_date: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }, index=["消費金額(1, 500)", "消費金額(500, 1000)", "消費金額(1000, 1500)", "消費金額(1500, 2000)", "消費金額(2000, 2500)", "消費金額(2500, 3000)", "消費金額(3000, 3500)", "消費金額(3500, 4000)", "消費金額(4000, 6000)", "消費金額(6000, 8000)", "消費金額(8000, 10000)", "消費金額(10000, 20000)", "消費金額(20000, max)"])

        df_cnt.at['消費金額(20000, max)', header_date] = df_order[df_order['RANK'] == 1].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(10000, 20000)', header_date] = df_order[df_order['RANK'] == 2].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(8000, 10000)', header_date] = df_order[df_order['RANK'] == 3].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(6000, 8000)', header_date] = df_order[df_order['RANK'] == 4].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(4000, 6000)', header_date] = df_order[df_order['RANK'] == 5].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(3500, 4000)', header_date] = df_order[df_order['RANK'] == 6].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(3000, 3500)', header_date] = df_order[df_order['RANK'] == 7].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(2500, 3000)', header_date] = df_order[df_order['RANK'] == 8].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(2000, 2500)', header_date] = df_order[df_order['RANK'] == 9].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(1500, 2000)', header_date] = df_order[df_order['RANK'] == 10].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(1000, 1500)', header_date] = df_order[df_order['RANK'] == 11].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(500, 1000)', header_date] = df_order[df_order['RANK'] == 12].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(1, 500)', header_date] = df_order[df_order['RANK'] == 13].count().TTL_SO_AMOUNT

        if i == 0:
            df_merge = df_cnt
        else:
            df_merge = pd.concat([df_merge, df_cnt], axis=1)

    # pivot table
    df_merge = df_merge.T
    df_merge = df_merge.reset_index()
    df_merge = df_merge.rename(columns={'index': '季度'})

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def cust_yearly_buy():
    today = date.today()
    end = today+relativedelta(months=-1)
    NOW=dt.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])

    cwd = os.getcwd()

    rpath = os.path.join(cwd, 'orders.csv')
    opath = os.path.join(cwd, 'yearly.csv')

    upath = os.path.join(cwd, 'customer.csv')

    rfmTable = pd.read_csv(rpath,  sep=',') 
    usrTable = pd.read_csv(upath, sep=',')

    # get latest 10 years data
    for i in range(1, 15, 1):
        end = NOW+relativedelta(years=-i)
        # for static last year
        start_od_temp = end

        start_od = dt.date(start_od_temp.year, 1, 1)
        end_od = dt.date(start_od_temp.year, 12, 31)

        header_date = end + relativedelta(months=0)
        # header_date get year and month
        header_date = header_date.strftime('%Y')

        df_order = rfmTable[(rfmTable['SO_TIME'] <= end_od.strftime('%Y/%m/%d')) & (rfmTable['SO_TIME'] >= start_od.strftime('%Y/%m/%d'))]

        # SUM TTL_SO_AMOUNT by CUST_ID
        df_order = df_order.groupby('CUST_ID').agg({'TTL_SO_AMOUNT': 'sum'})

        df_order['RANK'] = df_order.apply(lambda x: amount_level( x.TTL_SO_AMOUNT), axis=1)

        # get count of each level as a row
        df_cnt = pd.DataFrame({
            header_date: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }, index=["消費金額(1, 500)", "消費金額(500, 1000)", "消費金額(1000, 1500)", "消費金額(1500, 2000)", "消費金額(2000, 2500)", "消費金額(2500, 3000)", "消費金額(3000, 3500)", "消費金額(3500, 4000)", "消費金額(4000, 6000)", "消費金額(6000, 8000)", "消費金額(8000, 10000)", "消費金額(10000, 20000)", "消費金額(20000, max)"])

        df_cnt.at['消費金額(20000, max)', header_date] = df_order[df_order['RANK'] == 1].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(10000, 20000)', header_date] = df_order[df_order['RANK'] == 2].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(8000, 10000)', header_date] = df_order[df_order['RANK'] == 3].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(6000, 8000)', header_date] = df_order[df_order['RANK'] == 4].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(4000, 6000)', header_date] = df_order[df_order['RANK'] == 5].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(3500, 4000)', header_date] = df_order[df_order['RANK'] == 6].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(3000, 3500)', header_date] = df_order[df_order['RANK'] == 7].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(2500, 3000)', header_date] = df_order[df_order['RANK'] == 8].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(2000, 2500)', header_date] = df_order[df_order['RANK'] == 9].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(1500, 2000)', header_date] = df_order[df_order['RANK'] == 10].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(1000, 1500)', header_date] = df_order[df_order['RANK'] == 11].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(500, 1000)', header_date] = df_order[df_order['RANK'] == 12].count().TTL_SO_AMOUNT
        df_cnt.at['消費金額(1, 500)', header_date] = df_order[df_order['RANK'] == 13].count().TTL_SO_AMOUNT

        if i == 1:
            df_merge = df_cnt
        else:
            df_merge = pd.concat([df_merge, df_cnt], axis=1)

    # pivot table
    df_merge = df_merge.T
    df_merge = df_merge.reset_index()
    df_merge = df_merge.rename(columns={'index': '年度'})

    df_merge.to_csv(opath, sep='\t', encoding='utf-8')

def tommy_1():
    NOW = dt.datetime(2023, 3, 24)
    cwd = os.getcwd()

    start_date = NOW + relativedelta(days=-90)
    end_date = NOW + relativedelta(days=-30)

    upath = os.path.join(cwd, 'customer_email.csv')
    odpath = os.path.join(cwd, 'orders.csv')

    opath = os.path.join(cwd, 'tommy_1.csv')

    usrTable = pd.read_csv(upath, sep=',')
    orderTable = pd.read_csv(odpath, sep=',')

    # get usrTable's crt_time from now between start_date and end_date and without orderTable record
    usrTable = usrTable[(usrTable['CRT_TIME'] <= end_date.strftime('%Y/%m/%d')) & (usrTable['CRT_TIME'] >= start_date.strftime('%Y/%m/%d'))]
    usrTable = usrTable[~usrTable['CUST_ID'].isin(orderTable['CUST_ID'])]

    usrTable.to_csv(opath, sep='\t', encoding='utf-8')


def tommy_2():
    NOW = dt.datetime(2023, 3, 24)
    cwd = os.getcwd()

    start_date = NOW + relativedelta(days=-365)
    end_date = NOW + relativedelta(days=-60)

    upath = os.path.join(cwd, 'customer_email.csv')
    odpath = os.path.join(cwd, 'orders.csv')

    opath = os.path.join(cwd, 'tommy_2.csv')

    usrTable = pd.read_csv(upath, sep=',')
    orderTable = pd.read_csv(odpath, sep=',')

    # keep only head 1 order 
    orderTable = orderTable.groupby('CUST_ID').head(1)
    # order time between start_date and end_date
    orderTable = orderTable[(orderTable['SO_TIME'] <= end_date.strftime('%Y/%m/%d')) & (orderTable['SO_TIME'] >= start_date.strftime('%Y/%m/%d'))]

    df_order = pd.merge(orderTable, usrTable, on='CUST_ID', how='inner')
    df_order.to_csv(opath, sep='\t', encoding='utf-8')

if __name__ == '__main__':
    generate_order()
    generate_order_rtn()
    generate_customer()
    generate_customer_with_email()
    level()
    level_cnt()
    level_amount()
    yao()
    yao_cnt()
    yao_amount()
    get_level_protencial_email()
    first_seconde_order()
    first_buy()
    first_buy_rtn()
    second_buy()
    cust_yearly_buy()
    cust_season_buy()
