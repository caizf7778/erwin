#coding:utf-8
import win32com.client
import configparser
import os
import xlwt
from collections import defaultdict
from information import tab_check,tab_structure
from pywintypes import com_error
scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\HZPAS.er1", "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root
scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
scSubArCol = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
scTablespaceCol = scSession.ModelObjects.Collect(scRootObj, 'DB2 UDB Tablespace')
scKeyGroupCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group')
scKeyGroupMemberCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group Member')

class CreateTable:
    def __init__(self, tablename):
        self.tablename = tablename
    def get_tablename(self):
        return self.tablename
    def get_table_id(self):
        try:
            id = tab_check(tabname=self.tablename)[0][0]
        except KeyError as e:
            return False
        else:
            return id
    def get_physicalname(self):
        try:
            physicalname = tab_check(tabname=self.tablename)[0][1]
        except KeyError as e:
            return False
        else:
            return physicalname        
    def add_table_head(self):
        '''
        只创建表名，没有任何字段
        '''
        tabs = [i[1] for i in tab_check()]
        if self.tablename not in tabs:
            scTranId = scSession.BeginTransaction()
            entity = scSession.ModelObjects.Add("Entity")  # 创建表至少需要Type属性
            entity.Properties("Name").Value = self.tablename
            entity.Properties("Type").Value = 1    # 值为1表示为表
            try:
                scSession.CommitTransaction (scTranId)
            except com_error as e:
                scSession.RollbackTransaction(scTranId)
                return False
            else:
                return True
        else:
            return False

class DropTable:
    def __init__(self,table_id):
        self.table_id = table_id
    def get_table_id(self):
        return self.table_id
    def get_tablename(self):
        try:
            name = tab_check(id=self.table_id)[0][0]
        except KeyError as e:
            return False
        else:
            return name
    def get_physicalname(self):
        try:
            physical = tab_check(id=self.table_id)[0][1]
        except KeyError as e:
            return False
        else:
            return physical   
    @classmethod
    def by_physicalname(cls, physical_name):
        try:
            table_id = tab_check(physical_name=physical_name)[0][0]
        except KeyError as e:
            return False
        else:
            return cls(table_id)
    @classmethod
    def by_tablename(cls,tablename):
        try:
            table_id = tab_check(tabname=tablename)[0][0]
        except KeyError as e:
            return False
        else:
            return cls(table_id)        
    def remove_table(self):
        '''
        删除表
        '''
        scTranId = scSession.BeginTransaction()
        scEntObjCol.Remove(self.table_id)
        try:
            scSession.CommitTransaction (scTranId)
        except com_error as e:
            scSession.RollbackTransaction(scTranId)
            return False
        else:
            return True

def add_tabspace_config():
    '''
    配置文件添加表空间信息
    '''
    os.chdir(r'C:\Users\rrden\Desktop\erwin自动化')
    conf = configparser.ConfigParser()
    conf.read("erwin_config.ini")
    if 'Tablespace' not in conf.sections():
        conf.add_section("Tablespace")
    for sctabspace in  scTablespaceCol:    
        if sctabspace.Name.lower() not in conf.options("Tablespace"):
            conf.set("Tablespace", sctabspace.Name, sctabspace.ObjectId)
    conf.write(open("erwin_config.ini","w"))

def export_ent():
    '''
    输出实体表6个关键属性至excel表
    '''
    AL = []
    for ent in scEntObjCol:
        oEntCol = scSession.ModelObjects.Collect(ent, 'Attribute')
        for scAttrObj in oEntCol:
            scOPN = ent.Properties('Physical Name').Value # 实体表物理名称(英文)
            scON = ent.Properties('Name').Value # 实体表名称(中文)
            scAPN = scAttrObj.Properties('Physical Name').Value # 字段物理名称(英文)
            scAN = scAttrObj.Properties('Name').Value # 字段名称(中文)
            scAD = scAttrObj.Properties('Datatype').Value # 字段数据类型
            scANO = scAttrObj.Properties('Null Option').Value # 字段空值设置
            if scOPN == '%EntityName()':
                scOPN = ent.Name
            if scAPN == '%AttName':
                scAPN = scAttrObj.Name
            if scANO == 1:
                scANO = 'Not Null'
            if scANO == 0:
                    scANO = 'Null'    
            for i in (scOPN, scON, scAPN, scAN, scAD, scANO):
                AL.append(i)
    New_AL = [AL[i:i + 6] for i in range(0, len(AL), 6)]
    xls = xlwt.Workbook()
    sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
    heads = ['表名(英)', '表名(中)', '字段(英)', '字段(中)', '字段类型', '是否空值']
    ls = 0
    for head in heads:
        sheet.write(0, ls, head)
        ls += 1
    i = 1

    for list in New_AL:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1
    xls.save('D:\\2.xls')
