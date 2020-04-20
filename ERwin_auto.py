# coding:utf-8
import win32com.client
from collections import Counter
from collections import defaultdict
import xlwt
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

def tables_object(NotLogicalOnly=True):
    '''
    返回表ID及表名
    '''
    ent_all = {}   # 表ID(未删减LogicalOnly)
    ent_nlo = {}   # 表ID(删减LogicalOnly)
    for oEntObject in scEntObjCol:
        ent_all[oEntObject.ObjectId] = oEntObject.Name
        try:
            EntLogical_Only = oEntObject.Properties('Logical Only').Value
        except Exception as ex:
            EntLogical_Only = False
        if not EntLogical_Only:
            ent_nlo[oEntObject.ObjectId] = oEntObject.Name
    if NotLogicalOnly:
        return ent_nlo
    else:
        return ent_all

def columns_object(NotLogicalOnly=True):
    '''
    返回字段ID及字段名
    '''
    att_all = {}   # 字段ID(未删减LogicalOnly)
    att_nlo = {}   # 字段ID(删减LogicalOnly)
    for oAtt in scAttCol:
        att_all[oAtt.ObjectId] = oAtt.Name
        try:
            AttLogical_Only = oAtt.Properties('Logical Only').Value
        except Exception as ex:
            AttLogical_Only = False
        if not AttLogical_Only:
            att_nlo[oAtt.ObjectId] = oAtt.Name
    if NotLogicalOnly:
        return att_nlo
    else:
        return att_all
        

def reference_object(LogicalOnly=True):
    '''
    返回域引用的实体对象
    '''
    d_sm_all = {}   # 域引用的实体对象(未删减LogicalOnly)
    d_sm_nlo = {}   # 域引用的实体对象(删减LogicalOnly)
    for scSubjectArea in scSubArCol:
        l_sm =[]
        l_sm_nlo = []
        scSubMember = scSession.ModelObjects.Collect(scSubjectArea.ObjectId)
        for scReferencedEntity in scSubMember:
            if scReferencedEntity.classname =="Drawing Object Entity":
                ReferenceEntity = scReferencedEntity.Properties('DO Reference Object').Value
                l_sm.append(ReferenceEntity)
                if ReferenceEntity in tables_object(NotLogicalOnly=True):
                    l_sm_nlo.append(ReferenceEntity)
        d_sm_all[scSubjectArea.name] = l_sm
        d_sm_nlo[scSubjectArea.name] = l_sm_nlo
    if LogicalOnly:
        return d_sm_nlo
    else:
        return d_sm_all


def tabspaceID(spacename=None):
    '''
    返回表空间ID及表空间名称
    '''
    d_tabspace ={}  # 模型包含的表空间
    for scTablespace in  scTablespaceCol:
        d_tabspace[scTablespace.Name] = scTablespace.ObjectId
    if spacename == None:
        return d_tabspace
    if spacename not in d_tabspace.keys():
        scTranId = scSession.BeginTransaction()
        oTabspace = scSession.ModelObjects.Add("DB2 UDB Tablespace")
        oTabspace.Properties("Name").Value = spacename
        scSession.CommitTransaction (scTranId)
        d_tabspace[spacename] = oTabspace.ObjectId
    return d_tabspace[spacename]

def subject_areas():
    '''
    查询域名ID及域名名称
    '''
    d_subarea = {}
    for scSA in scSubArCol:
        d_subarea[scSA.ObjectId] = scSA.name
    return d_subarea

def add_subject_area(areaname):
    '''
    添加域，输入需要添加的域名
    '''
    if not areaname in list(subject_areas().values()):
        scTranId = scSession.BeginTransaction()
        oSubject = scSession.ModelObjects.Add("Subject Area")   #创建域至少需要Name属性
        oSubject.Properties("Name").Value = areaname
        scSession.CommitTransaction (scTranId)
        return list(subject_areas().values())    
    else:
        return False

def subarea_ent():
    '''
    返回未被域引用的实体表集
    '''
    mlid = []   # 总域实体表集
    nmlid = []  # 其他域实体表集
    for scSubjectArea in scSubArCol:
        scSubMember = scSession.ModelObjects.Collect(scSubjectArea.ObjectId)
        for scReferencedEntity in scSubMember:
            if scReferencedEntity.classname =="Drawing Object Entity":
                if scSubjectArea.name =='<Main Subject Area>':
                    mlid.append(scReferencedEntity.Properties('DO Reference Object').Value)
                else:
                    nmlid.append(scReferencedEntity.Properties('DO Reference Object').Value)
    return [item for item in mlid if item not in nmlid]

def dup_tab():
    '''
    查找重复表及表重复次数
    '''
    PN_List = []
    for oEntObject in scEntObjCol:
        oen = oEntObject.Properties('Physical Name').Value
        oeid = oEntObject.ObjectId
        if oen == '%EntityName()':
            oen = oEntObject.Name
        PN_List.append(oen)
    DC_PN_List = dict(Counter(PN_List))
    return {key:value for key,value in DC_PN_List.items() if value > 1}

def export_ent():
    '''
    输出实体表6个关键属性至excel表
    '''
    AL = []
    for oEntObject in scEntObjCol:
        oEntCol = scSession.ModelObjects.Collect(oEntObject, 'Attribute')
        for scAttrObj in oEntCol:
            scOPN = oEntObject.Properties('Physical Name').Value # 实体表物理名称(英文)
            scON = oEntObject.Properties('Name').Value # 实体表名称(中文)
            scAPN = scAttrObj.Properties('Physical Name').Value # 字段物理名称(英文)
            scAN = scAttrObj.Properties('Name').Value # 字段名称(中文)
            scAD = scAttrObj.Properties('Datatype').Value # 字段数据类型
            scANO = scAttrObj.Properties('Null Option').Value # 字段空值设置
            if scOPN == '%EntityName()':
                scOPN = oEntObject.Name
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