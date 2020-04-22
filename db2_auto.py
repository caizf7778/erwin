# coding:utf-8
import re
import ibm_db
import ibm_db_dbi
import os
os.chdir(r'C:\Users\rrden\Desktop\erwin自动化') 
from config import conn_str, tab_in, tab_notend, tab_notbegin
ibm_db_conn = ibm_db.connect(conn_str,'','')
conn = ibm_db_dbi.Connection(ibm_db_conn)
tabs = [ i['TABLE_NAME'] for i in conn.tables('PAS')]   # 获取所有表
columns = conn.columns('PAS')   #获取所有字段及属性


def string_letter(str):
    '''
    判断字符串是否以字母结尾
    '''
    text = re.compile(r".*[a-zA-Z]$")
    if text.match(str):
        return True
    else:
        return False

def string_number(str):
    '''
    判断字符串是否包含4、6、8位数字（日期）
    '''
    pattern = re.compile("[0-9]+")
    match = pattern.findall(str)
    if match:
        for i in match:
            if len(i) ==8:
                return True
            else:
                return False
    else:
        return False

def tables_needed():
    '''
    返回需要维护更新的表名
    '''
    tab_list = []
    for tab in tabs:
        if string_letter(tab) and not string_number(tab) and tab.startswith(tab_in) and not tab.endswith(tab_notend) and not tab.startswith(tab_notbegin):
            tab_list.append(tab)
    return tab_list

def select_indexes():
    '''
    返回数据库中所有索引所在表的表名，索引名，索引字段名
    '''
    select = "SELECT TABNAME,INDNAME,COLNAMES FROM syscat.INDEXES WHERE owner='PAS'"
    cur = conn.cursor()
    cur.execute(select)
    row=cur.fetchall()
    return row

def column_deal():
    '''
    返回表主键字段信息
    '''
    select = "SELECT a.TABNAME,COLNAME,COLNAMES,COLNO,(CASE WHEN TYPENAME='DECIMAL' THEN 'DECIMAL('||LENGTH||','||SCALE||')' WHEN TYPENAME in('TIMESTAMP', 'INTEGER') THEN TYPENAME ELSE TYPENAME||'('||LENGTH||')' end) TYPENAME,(CASE NULLS WHEN 'Y' THEN 0 ELSE 1 END) AS NULLS FROM syscat.INDEXES a ,syscat.columns b WHERE owner='PAS' AND a.TABNAME=b.TABNAME AND INDNAME LIKE 'XPK%' ORDER BY a.TABNAME "
    cur = conn.cursor()
    cur.execute(select)
    row=cur.fetchall()
    lst = []
    for i in row:
        tp = 100
        if i[1] in re.split('[+-]',i[2])[1:]:
            tp = 0
        lst.append(i[0],i[1],tp,i[3],i[4],i[5])
    return lst

def tables_hasindexes():
    '''
    返回数据库中有索引的表的表名
    '''
    tab_index = []
    for index in select_indexes():
        tab_index.append(index[0])
    return tab_index

def indexes_member(tablesname=None):
    '''
    获取所有索引及索引字段成员（未筛选需要维护的表）
    '''
    indexes = {}
    sin = set()
    for i in select_indexes():
        if not i[0] in sin:
            dic = {}
        sin.add(i[0])
        dic[i[1]] = re.split('[+-]',i[2]) [1:]
        indexes[i[0]] = dic
    if tablesname:
        try:
            return indexes[tablesname]
        except (KeyError, NameError):
            pass
    else:
        return indexes

  

