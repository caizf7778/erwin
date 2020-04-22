# coding:utf-8
import win32com.client
import configparser
import os
import xlwt
from collections import Counter
from collections import defaultdict
scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\V4.0.er1", "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root
scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
scSubArCol = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
scTablespaceCol = scSession.ModelObjects.Collect(scRootObj, 'DB2 UDB Tablespace')
scKeyGroupCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group')
scKeyGroupMemberCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group Member')

def tables(logical_only=False):
    '''
    返回表ID及表名
    '''
    ent_all = {}   # 表ID(未删减LogicalOnly)
    ent_nlo = {}   # 表ID(删减LogicalOnly)
    for ent in scEntObjCol:
        ent_all.setdefault(ent.Name, []).append(ent.ObjectId)
        try:
            ent_logicalonly = ent.Properties('Logical Only').Value
        except Exception:
            ent_logicalonly = False
        if not ent_logicalonly:
            ent_nlo.setdefault(ent.Name, []).append(ent.ObjectId)
    if  not logical_only:
        return ent_nlo
    else:
        return ent_all


def add_table_head(tablename):
    '''
    只创建表名，没有任何字段
    '''
    scTranId = scSession.BeginTransaction()
    entity = scSession.ModelObjects.Add("Entity")  # 创建表至少需要Type属性
    entity.Properties("Name").Value = tablename
    entity.Properties("Type").Value = 1    # 值为1表示为表
    scSession.CommitTransaction (scTranId)
    return entity.ObjectId


def columns(logical_only=False):
    '''
    返回字段ID及字段名
    '''
    att_all = {}   # 字段ID(未删减LogicalOnly)
    att_nlo = {}   # 字段ID(删减LogicalOnly)
    for att in scAttCol:
        att_all[att.ObjectId] = att.Name
        try:
            att_logicalonly = att.Properties('Logical Only').Value
        except Exception:
            att_logicalonly = False
        if not att_logicalonly:
            att_nlo[att.ObjectId] = att.Name
    if not logical_only:
        return att_nlo
    else:
        return att_all
        

def reference_object(logical_only=True):
    '''
    返回域引用的实体对象
    '''
    d_sm_all = {}   # 域引用的实体对象(未删减LogicalOnly)
    d_sm_nlo = {}   # 域引用的实体对象(删减LogicalOnly)
    tables_logicalonly =[]
    for i in tables(True).values():
        for j in i:
            tables_logicalonly.append(j)
    for subject_area in scSubArCol:
        l_sm =[]
        l_sm_nlo = []
        subect_area_members = scSession.ModelObjects.Collect(subject_area.ObjectId)
        for member in subect_area_members:
            if member.classname =="Drawing Object Entity":
                reference_entity = member.Properties('DO Reference Object').Value
                l_sm.append(reference_entity)
                if reference_entity in tables_logicalonly:
                    l_sm_nlo.append(reference_entity)
        d_sm_all[subject_area.name] = l_sm
        d_sm_nlo[subject_area.name] = l_sm_nlo
    if logical_only:
        return d_sm_nlo
    else:
        return d_sm_all

def tabspaceID(space_name=None):
    '''
    返回表空间名称及ID，也可添加表空间
    '''
    d_tabspace ={}  # 模型包含的表空间
    for tablespace in  scTablespaceCol:
        d_tabspace[tablespace.Name] = tablespace.ObjectId
    if space_name == None:
        add_tabspace_config()
        return d_tabspace
    if space_name not in d_tabspace.keys():
        scTranId = scSession.BeginTransaction()
        oTabspace = scSession.ModelObjects.Add("DB2 UDB Tablespace")
        oTabspace.Properties("Name").Value = space_name
        scSession.CommitTransaction (scTranId)
        d_tabspace[space_name] = oTabspace.ObjectId
    add_tabspace_config()
    return d_tabspace[space_name]

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

def subarea_ent():
    '''
    返回未被域引用的实体表集
    '''
    mlid = []   # 总域实体表集
    nmlid = []  # 其他域实体表集
    for subject_area in scSubArCol:
        subect_area_members = scSession.ModelObjects.Collect(subject_area.ObjectId)
        for member in subect_area_members:
            if member.classname =="Drawing Object Entity":
                if subject_area.name =='<Main Subject Area>':
                    mlid.append(member.Properties('DO Reference Object').Value)
                else:
                    nmlid.append(member.Properties('DO Reference Object').Value)
    return [item for item in mlid if item not in nmlid]


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


def column_dictionary():
    '''
    返回字典类型的字段词典
    '''
    allcolumn = []
    for scAtt in scAttCol:
        sn = scAtt.Name
        spn = scAtt.Properties('Physical Name').Value
        if sn != spn and spn !='%AttName':
            allcolumn.append((spn.upper(), sn))
    removal = set(allcolumn)
    d = {}
    for en,zh in removal:
        d.setdefault(en, []).append(zh)
    return d


def column_dictionary2():
    '''
    返回defaultdict(<class 'list'>类型的字段词典，可通过append()方法添加键值对
    '''
    allcolumn = []
    for scAtt in scAttCol:
        sn = scAtt.Name
        spn = scAtt.Properties('Physical Name').Value
        if sn != spn and spn !='%AttName':
            allcolumn.append((spn.upper(), sn))
    removal = set(allcolumn)
    d = defaultdict(list)
    for en,zh in removal:
        d[en].append(zh)
    return d

# 事务控制-开始
# scTranId = scSession.BeginTransaction()
# 事务控制-结束（提交）
# scSession.CommitTransaction (scTranId)
# 关闭scSession
# scSession.Close()
# scapi.Sessions.Remove(scSession)
# 模型另存为（newfilename为新模型的路径）
# scPUnit.Save(newfilename)
# 断开内存中模型的连接
# scapi.PersistenceUnits.clear()
# scPUnit = None
# scSession = None