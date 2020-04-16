# coding:utf-8
import win32com.client
from collections import Counter
import xlwt
scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\10.er1", "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root
scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
scSubArCol = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
scTablespaceCol = scSession.ModelObjects.Collect(scRootObj, 'DB2 UDB Tablespace')

# 事务控制-开始
# scTranId = scSession.BeginTransaction()



ent_all = {}   # 表ID(未删减LogicalOnly)
ent_nlo = {}   # 表ID(删减LogicalOnly)
ent_lo = {}    # 表ID(LogicalOnly)
for oEntObject in scEntObjCol:
    ent_all[oEntObject.ObjectId] = oEntObject.Name
    try:
        EntLogical_Only = oEntObject.Properties('Logical Only').Value
    except Exception as ex:
        EntLogical_Only = False
    if not EntLogical_Only:
        ent_nlo[oEntObject.ObjectId] = oEntObject.Name
    if EntLogical_Only:
        ent_lo[oEntObject.ObjectId] = oEntObject.Name

att_all = {}   # 字段ID(未删减LogicalOnly)
att_nlo = {}   # 字段ID(删减LogicalOnly)
att_lo = {}    # 字段ID(LogicalOnly)
for oAtt in scAttCol:
    att_all[oAtt.ObjectId] = oAtt.Name
    try:
        AttLogical_Only = oAtt.Properties('Logical Only').Value
    except Exception as ex:
        AttLogical_Only = False
    if not AttLogical_Only:
        att_nlo[oAtt.ObjectId] = oAtt.Name
    if AttLogical_Only:
        att_lo[oAtt.ObjectId] = oAtt.Name

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
            if ReferenceEntity in ent_nlo:
                l_sm_nlo.append(ReferenceEntity)
    d_sm_all[scSubjectArea.name] = l_sm
    d_sm_nlo[scSubjectArea.name] = l_sm_nlo

d_tabspace ={}  # 模型包含的表空间
for scTablespace in  scTablespaceCol:
    d_tabspace[scTablespace.ObjectId] = scTablespace.Name
    d_tabspace['---'] = '无表空间'

d_subarea = {}
for scSA in scSubArCol:
    d_subarea[scSA.ObjectId] = scSA.name



def subarea_ent():
    '''
    遍历所有域里引用的实体
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
    return [item for item in mlid if item not in nmlid]   # 返回不存在总域实体表集

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