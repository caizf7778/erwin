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

def tables_primarykey(tablesname):
    try :
        for i in indexes_member(tablesname).keys():
            if i.startswith('XPK'):
                return indexes_member(tablesname)[i]
    except AttributeError:
        return False


                
                
                
set(tables_needed()).difference(set(tables_hasindexes()))
set(tables_hasindexes()).intersection(set(tables_needed()))
  

for key in indexes_member():
        print(indexes_member()[key])


tabnoindex = set(tables_needed()).difference(set(tables_hasindexes()))
for t in tables_needed():
    for c in columns:
        if c['TABLE_NAME'] == t:
            tp = 100
            tablename = c['TABLE_NAME']
            columnname = c['COLUMN_NAME']
            order = c['ORDINAL_POSITION']
            nulloption = int(not c['NULLABLE'])
            # if c['TYPE_NAME'] == 'DECIMAL':
                # datatype = c['TYPE_NAME'] + '(' + str(c['COLUMN_SIZE']) + ',' + str(c['DECIMAL_DIGITS']) +')'
            # elif c['TYPE_NAME'] in ['TIMESTAMP', 'INTEGER']:
                # datatype = c['TYPE_NAME']
            # else:
                # datatype = c['TYPE_NAME'] + '(' + str(c['COLUMN_SIZE']) +')'
            if t in tabnoindex：
                tp = 0
            for member in indexes_member(c['TABLE_NAME']).keys():
                    if c['COLUMN_NAME'] in member:
                        tp = 0
                    print(c['TABLE_NAME'],c['COLUMN_NAME'],tp)       


                    
            print(tablename, ' | COLUMN_NAME: ', columnname, ' | DataType: ',datatype, ' | Order: ', order, ' | Null Option:', nulloption)


def columns_needed(tablename=None):
    cols = {}
    scol = set()
    for cols in columns:
        if not cols['TABLE_NAME'] in scol:
            dic = {}
            scol.add(cols['TABLE_NAME'])
            dic[]

    