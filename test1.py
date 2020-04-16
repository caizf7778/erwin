#coding:utf-8
import win32com.client
from collections import Counter
import xlwt
scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\2.er1", "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root
scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
scSubArCol = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
# 事务控制-开始
scTranId = scSession.BeginTransaction()
# 事务控制-结束（提交）
scSession.CommitTransaction (scTranId)
# 关闭scSession
scSession.Close()
scapi.Sessions.Remove(scSession)
# 模型另存为（newfilename为新模型的路径）
scPUnit.Save(newfilename)
# 断开内存中模型的连接
scapi.PersistenceUnits.clear()
scPUnit = None
scSession = None

# 遍历所有域里引用的实体
mlid = [] # 
nmlid  = []
nrl = []
for scSubjectArea in scSubArCol:
    scSubMember = scSession.ModelObjects.Collect(scSubjectArea.ObjectId)
    for scReferencedEntity in scSubMember:
        if scReferencedEntity.classname =="Drawing Object Entity":
            if scSubjectArea.name =='<Main Subject Area>':
                mlid.append(scReferencedEntity.Properties('DO Reference Object').Value)
            else:
                nmlid.append(scReferencedEntity.Properties('DO Reference Object').Value)


def column_in_table(table):
    

for scEntObj in scEntObjCol:
    for i in scEntObj.Properties:
        l1.append(str(i))
        if 'Logical Only' in l1:
            print(scEntObj.Name)
d1 = {}
for scEntObj in scEntObjCol:
    try:
        Logical_Only = scEntObj.Properties('Logical Only').Value
    except Exception as ex:
        Logical_Only = False
    if Logical_Only:
        print(scEntObj.ObjectId,scEntObj.Name)
        
for scSA in scSubArCol:
    print(scSA.ObjectId, scSA.name, scSA.ClassName)
for scSA in scSubArCol:
    for i in scSA.Properties:
        try:
            a = scSA.Properties(i).Value
        except Exception as ex:
            a = '---'
        print(str(i), ":", a, "|", end=" ")
    print()
for scObj in scMObjects:
    scMpc = scObj.CollectProperties("")

        
for oEntObject in scEntObjCol:
    oEntSA = scSession.ModelObjects.Collect(oEntObject, 'Subject Area')
    for i in oEntSA:
        print(i)
    
d_sm = {}        
for scSubjectArea in scSubArCol:
    l_sm =[]
    scSubMember = scSession.ModelObjects.Collect(scSubjectArea.ObjectId)
    for scReferencedEntity in scSubMember:
        if scReferencedEntity.classname =="Drawing Object Entity":
            l_sm.append(scReferencedEntity.Properties('DO Reference Object').Value)
    d_sm[scSubjectArea.name] = l_sm


    # print(oEntObject.ObjectId, oEntObject.Name ,oEntObject.ClassName)
# 输出实体表6个关键属性至excel表
def 
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


        
for oEntObject in scEntObjCol:    
    # 获取该Entity的所有Attribute对象
    for i in oEntObject.Properties:
        print(str(i),':',oEntObject.Properties(i).Value,end=' | ')
    print()
    print('-----------------------')
    oEntCol = scSession.ModelObjects.Collect(oEntObject, 'Attribute', 1)
    for scAttrObj in oEntCol:
        print(scAttrObj.type)
        # 打印所有表字段的英文和中文名称
        print(scAttrObj.Properties('Physical Name').Value,",",scAttrObj.Properties('Name').Value,",",scAttrObj.Properties('Datatype').Value,scAttrObj.Properties('Null Option').Value)

for oEntObject in scEntObjCol:
    try:
        scColor = oEntObject.Properties('DB Name').Value
    except Exception as ex:
        scColor = 'ABC'
    print(scColor,oEntObject.Name)
# test
s1 = set()
s2 = set()
s3 = set()
s4 = set()
s5 = set()
for oEntObject in scEntObjCol:  
    for scOP in oEntObject.Properties:
        # s1为实体属性的集合
        s1.add(str(scOP))
    oEntCol = scSession.ModelObjects.Collect(oEntObject, 'Attribute')
    for scAttrObj in oEntCol:    
        for scAP in scAttrObj.Properties:
            # s2为字段属性的集合
            s2.add(str(scAP))


for scSA in scSubjectArea:
    for i in scSA.Properties:
        s3.add(str(i))


for i in scRootObj.Properties:
    s4.add(str(i))
# 
for oEntObject in scEntObjCol:
    oEntCol = scSession.ModelObjects.Collect(oEntObject, 'Attribute')
    for oAttObject In oEntCol:
        oUserNote = SCSession.ModelObjects.Collect(oAttObject).Add("Extended_Notes")
        oUserNote.Properties("Comment").Value = "Test note1"
        oUserNote.Properties("Note_Importance").Value = "0"
        oUserNote.Properties("Status").Value = "1"
        
for oEntObject in scEntObjCol:
    oEntCol = scSession.ModelObjects.Collect(oEntObject, 'Attribute')
    for scAttrObj in oEntCol:
        try:
            scAPPR = scAttrObj.Properties('Parent Relationship').Value
        except Exception as ex:
            scAPPR = ' '
        print(scAPPR)
    

# 读取所有实体表的属性值
for oEntObject in scEntObjCol:
    for scOP in oEntObject.Properties:
        print(str(scOP),":",oEntObject.Properties(str(scOP)).Value,"|", end=" ")
    print()
    print()
    print()

for i in scTEST:
    for j in i.Properties:
        print(str(j),":",i.Properties(str(j)).Value,"|", end=" ")
    print()
for i in scTEST:
    print(i.Properties('').Value)
l1 = []   
for oEntObject in scEntObjCol:
    for scOP in oEntObject.Properties:
        try: 
            scIn = oEntObject.Properties('Index Generate').Value
        except Exception as ex:
            scIn = 'NULL'
        print(scIn)
    print()
    print()
    print()    
    
    
for oEntObject in scEntObjCol:
    oEntObject.Properties('Name').Value
    oEntCol = scSession.ModelObjects.Collect(oEntObject, 'Table Name', 1)
    print('1')




    
系统运维-运维报告项 {BD63AA4D-2D38-4B28-BB2E-95D0EA67F9B2}+00000000
系统运维-运维报告项 {886BD97B-F2C7-4213-9653-A9B16D33F327}+00000000