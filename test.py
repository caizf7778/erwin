#coding:utf-8
import win32com.client
from collections import defaultdict
scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\YCPAS.er1", "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root
scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
scSubArCol = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
scTablespaceCol = scSession.ModelObjects.Collect(scRootObj, 'DB2 UDB Tablespace')
scKeyGroupCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group')
scKeyGroupMemberCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group Member')

scRootObj.Remove()

sctest = scSession.ModelObjects.Collect('{27329F41-3FF8-4FB9-BB02-02742C934BF4}+00000000')
for i in sctest:
    for j in i.Properties:
        try:
            a = i.Properties(j).Value
        except Exception as ex:
            a = '---'
        print(str(j), ":", a, "|", end=" ")
    print()



for oEntObject in scEntObjCol:
    for i in oEntObject.Properties:
        print(str(i),':',oEntObject.Properties(i).Value,end=' | ')
    print()
    print('-----------------------')
    
for scAtt in scAttCol:
    for i in scAtt.Properties:
        if  str(i) not in ['Comment','Definition']:
            print(str(i),':',scAtt.Properties(i).Value,end=' | ')
    print()
    print('-----------------------')
    
for scKeyGroup in scKeyGroupCol:
    for i in scKeyGroup.Properties:
        print(str(i),':',scKeyGroup.Properties(i).Value,end=' | ')
    print()
    print('-----------------------')




for scKeyGroup in scKeyGroupCol:
    for i in scKeyGroup.Properties:
        print(str(i),':',scKeyGroup.Properties(i).Value,end=' | ')
    print()
    print('-----------------------')
    scKeyGroupMemberCol = scSession.ModelObjects.Collect(scKeyGroup, 'Key Group Member')
    for scKeyGroupMember in scKeyGroupMemberCol:
        for j in scKeyGroupMember.Properties:
            print(str(j),':',scKeyGroupMember.Properties(j).Value,end=' | ')
        print()
        print('-----------------------')

for scSubAr in scSubArCol:
    a = scSubAr.Properties("Created Time").Value
    b = scSubAr.Properties("Name").Value
    print(a,datetime.date.fromtimestamp(a),b)
    for i in scSubAr.properties:
        print(str(i),':',scSubAr.Properties(i).Value,end=' | ')
    print()
    print('-----------------------')



# 事务控制-开始
scTranId = scSession.BeginTransaction()

# 事务控制-结束（提交）
scSession.CommitTransaction (scTranId)
# 关闭scSession
scSession.Close()
scapi.Sessions.Remove(scSession)
# 模型另存为（newfilename为新模型的路径）
scPUnit.Save()
# 断开内存中模型的连接
scapi.PersistenceUnits.clear()
scPUnit = None
scSession = None

def check_subject_area(areaname=None):
    


def add_subject_area(areaname):
    '''
    添加域，输入需要添加的域名
    '''
    scTranId = scSession.BeginTransaction()
    oSubject = scSession.ModelObjects.Add("Subject Area")   #创建域至少需要Name属性
    oSubject.Properties("Name").Value = areaname
    scSession.CommitTransaction (scTranId)

def add_table_head(tabname, physical_only=False, tablespace='tbs_pas', index_tablespace='tbs_idx', ):
    '''
    只创建表名，没有任何字段
    '''
    scTranId = scSession.BeginTransaction()
    oEntity = scSession.ModelObjects.Add("Entity")  # 创建表至少需要Type属性
    oEntity.Properties("Name").Value = tabname
    oEntity.Properties("Type").Value = 1    # 值为1表示为表
    scSession.CommitTransaction (scTranId)
    return oEntity.ObjectId

oEntity.Properties("Physical Only").Value = False   # 是否仅在物理模式下显示
oEntity.Properties("DB2UDB TABLESPACE").Value = "{3CBD15DD-C280-46DA-A7CF-E5FA9DB42D9F}+00000000"   # 表空间
oEntity.Properties("DB2UDB INDEX TABLESPACE").Value = "{9CB8D5C1-DD33-4A33-B6E2-8A8BC817E78D}+00000000"     # 索引表空间
oEntity.Properties("Index Generate").Value = 1
oEntity.Properties("Physical Name").Value = "jxdx_ckzh"
oEntity.Properties("Entity Fill Color").Value = "{73A29D04-3F67-4DD4-9CDE-5BEFFE2EBCD3}+00000000"
oEntity.Properties("DB2UDB PARTITIONING KEY").Value = ""
oEntity.Properties("Definition").Value = ""


  # 创建字段至少需要Type属性
def add_column(tablename, tablespace, indexspace,)
oAttribute.Properties("Name").Value = "字段z"
oAttribute.Properties("Physical Name").Value = "jxdxdh"
oAttribute.Properties("Type").Value = 0     # 0/100,类型0为主键字段
oAttribute.Properties("Attribute Required").Value = False
oAttribute.Properties("Order").Value = 2
oAttribute.Properties("Datatype").Value = "DECIMAL(25,4)"
oAttribute1 = scSession.ModelObjects.Collect(oEntity).Add("Attribute")
oAttribute1.Properties("Name").Value = "字段a"
oAttribute1.Properties("Type").Value = 100    # 0/100,类型100为普通字段
oAttribute1.Properties("Attribute Required").Value = True
oAttribute1.Properties("Physical Name").Value = "qsrq"
oAttribute1.Properties("Order").Value = 1

oIndex = scSession.ModelObjects.Collect(oEntity).Add("Key Group")  
oIndex.Properties("Key Group Type").Value = PK    # PK/AK1/IE1/FK


{'Definition', 'Name', 'Entity Fill Color', 'Type', 'Index Generate', 'Physical Name', 'DB2UDB INDEX TABLESPACE', 'DB2UDB TABLESPACE',
 'DB Owner', 'DB2UDB PARTITIONING KEY', 'Physical Only'}
 
 
for oEntObject in scEntObjCol:
    try:
        ent_logicalonly = ent.Properties('Logical Only').Value
    except Exception:
        ent_logicalonly = False
    if  ent_logicalonly:
        for i in oEntObject.Properties:
            print(str(i),':',oEntObject.Properties(i).Value,end=' | ')
        print()
        print('-----------------------')



# 事务控制-开始
scTranId = scSession.BeginTransaction()

# 事务控制-结束（提交）
scSession.CommitTransaction (scTranId)
# 关闭scSession
scSession.Close()
scapi.Sessions.Remove(scSession)
# 模型另存为（newfilename为新模型的路径）
scPUnit.Save()
# 断开内存中模型的连接
scapi.PersistenceUnits.clear()
scPUnit = None
scSession = None


def add_table_head(tablename):
    '''
    只创建表名，没有任何字段
    '''
    scTranId = scSession.BeginTransaction()
    entity = scSession.ModelObjects.Add("Entity")    # 创建表至少需要Type属性
    entity.Properties("Name").Value = tablename
    entity.Properties("Type").Value = 1    # 值为1表示为表   
    try:
        scSession.CommitTransaction (scTranId)
    except com_error as e:
        scSession.RollbackTransaction(scTranId)
        print('表创建不成功')
    else:
    
    entity = scSession.ModelObjects.Add("Entity")  # 创建表至少需要Type属性
    entity.Properties("Name").Value = tablename
    entity.Properties("Type").Value = 1    # 值为1表示为表


def transaction(fun):
    try:
        scTranId = scSession.BeginTransaction()
        fun
        print('bagin')
    except com_error as e:
        def rollback():
            global scTranId
            scSession.RollbackTransaction(scTranId)
        rollback()
        print('rollback1')
    else:
        try:
            scSession.CommitTransaction (scTranId)
            print('commit')
        except com_error as e:
            scSession.RollbackTransaction(scTranId)
            print('rollback2')
# test1: 正常
scTranId = scSession.BeginTransaction()
transaction(print('test1'))
# test2: 异常-执行前已经创建事务
scTranId = scSession.BeginTransaction()
transaction(print('test2'))
# test3：异常-提交异常

            
def test()
    try:
lst = [1,2,3,4,4,4,5,6,66,7,7,7]
transaction(set(lst))

Name : TJRQ | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 1 | DB Name : TJRQ | Comment : %AttDef | Physical Name : TJRQ | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000003 | Object Order : 0 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 1 | Created Time : 1543482539 | Description : Created in the model <Model2>. |
Name : KHDXDH | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 2 | DB Name : KHDXDH | Comment : %AttDef | Physical Name : KHDXDH | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000003 | Object Order : 1 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 1 | Created Time : 1543482539 | Description : Created in the model <Model2>. |
Name : XDYJC | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 3 | DB Name : XDYJC | Comment : %AttDef | Physical Name : XDYJC | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000003 | Object Order : 2 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 1 | Created Time : 1543482539 | Description : Created in the model <Model2>. |
Name : BZSM | Type : 100 | Datatype : VARCHAR(200) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 4 | DB Name : BZSM | Comment : %AttDef | Physical Name : BZSM | Logical Datatype : VARCHAR(200) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000002 | Object Order : 3 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 1 | Created Time : 1543482539 | Description : Created in the model <Model2>. |
Name : CZR | Type : 100 | Datatype : VARCHAR(12) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 5 | DB Name : CZR | Comment : %AttDef | Physical Name : CZR | Logical Datatype : VARCHAR(12) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000002 | Object Order : 4 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 1 | Created Time : 1543482539 | Description : Created in the model <Model2>. |
Name : CZSJ | Type : 100 | Datatype : TIMESTAMP | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 6 | DB Name : CZSJ | Comment : %AttDef | Physical Name : CZSJ | Logical Datatype : TIMESTAMP | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000004 | Object Order : 5 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 1 | Created Time : 1543482539 | Description : Created in the model <Model2>. |
Key Group Type : PK | Index Generate : 2 | DB Owner : ODSFDM | Physical Name : XPKSGLR_XDYJC |
Key Group Type : AK1 | Index Generate : 1 | Index Clustered : 2 | DB Owner : PAS | Physical Name : XPKSGLR_XDYJC | Allow Index Reverse Scans : True |
Key Group Member Column : {84BEE7D6-3555-4D66-95EC-6593EA98D2AF}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
Key Group Member Column : {FCD5B3EC-3981-4447-8619-51515D4DD83C}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
Type : 529 | Created Time : 1543482564 | Description : Imported via db level compare from <Model2>. |
Type : 32 | Created Time : 1543481860 | Description : Created via reverse engineering. |



Name : 客户号 | Type : 0 | Datatype : VARCHAR(30) | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 3 | Comment : %AttDef | Physical Name : khh | Logical Datatype : VARCHAR(30) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
Type : 1 | Created Time : 1430102389 |
Type : 2 | Created Time : 1430286305 |
Type : 2 | Created Time : 1430286305 |
Name : 业务类型 | Type : 0 | Datatype : VARCHAR(2) | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 2 | Comment : %AttDef | Physical Name : ywlx | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
Name : 考核对象代号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 1 | Comment : %AttDef | Physical Name : khdxdh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000003 | Object Order : 2 |
Type : 1 | Created Time : 1190362873 | Description : Created in the current model. |
Type : 64 | Created Time : 1251939167 | Description : Imported from a previous version of ERwin. |
Type : 64 | Created Time : 1252034025 | Description : Imported from a previous version of ERwin. |
Type : 64 | Created Time : 1299021923 | Description : Imported from a previous version of ERwin. |
Type : 64 | Created Time : 1299230607 | Description : Imported from a previous version of ERwin. |
Type : 2 | Created Time : 1430102332 |
Type : 2 | Created Time : 1430102334 |
Type : 2 | Created Time : 1430286305 |
Type : 2 | Created Time : 1430286305 |
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
Key Group Member Column : {2C6DABCE-7FA6-4780-92D7-4BE9D383C088}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
Key Group Member Column : {5FAA0B4F-833E-41D3-9A68-D9B65399035F}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
Key Group Member Column : {27CACA2D-B1EA-4741-A1ED-4403DC10CCA7}+00000000 | Key Group Sort Order : ASC | Key Group Position : 3 |
Type : 1 | Created Time : 1190362873 | Description : Created in the current model. |
Type : 64 | Created Time : 1251939166 | Description : Imported from a previous version of ERwin. |
Type : 64 | Created Time : 1252034025 | Description : Imported from a previous version of ERwin. |
Type : 64 | Created Time : 1299021923 | Description : Imported from a previous version of ERwin. |
Type : 64 | Created Time : 1299230607 | Description : Imported from a previous version of ERwin. |
Type : 2 | Created Time : 1430102332 |
Type : 2 | Created Time : 1430102334 |
Type : 2 | Created Time : 1430286305 |
Type : 2 | Created Time : 1430286305 |




{9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 DO Text : 手工导入-存款基数账户-调整基数 | {9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 DO Location : (107, 423, 256, 549) | {9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 DO Reference Object : {066F4B29-421A-4FB6-B249-F0916427A904}+00000000 | {9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 DO Entity Width AutoResizeable : True | {9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 DO Entity Height AutoResizeable : True | {9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 Entity Def Font : {1A46EF46-4CC8-4D79-A4CF-586F5C5C9B89}+00000000 | {9DA71497-9380-4382-9AAC-FE71A0FAF518}+00000000 Entity Fill Color : {A54B4541-336D-40B8-AD97-5D01A500BC48}+00000000 |
-----------------------
{69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 DO Text : 业绩指标-行员考核基数 | {69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 DO Location : (100, 733, 213, 859) | {69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 DO Reference Object : {FF84B92D-41C6-4929-A3B1-A82536CCFF98}+00000000 | {69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 DO Entity Width AutoResizeable : True | {69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 DO Entity Height AutoResizeable : True | {69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 Entity Def Font : {32F21E02-94E9-4859-8A57-F91E237956A7}+00000000 | {69DF8CE1-4CA1-49E3-BB4F-7157D13A27E9}+00000000 Entity Fill Color : {A54B4541-336D-40B8-AD97-5D01A500BC48}+00000000 |
-----------------------
{54933D63-7B30-46FF-B353-C8136966B81B}+00000000 DO Text : 业绩指标-机构考核基数 | {54933D63-7B30-46FF-B353-C8136966B81B}+00000000 DO Location : (96, 577, 221, 703) | {54933D63-7B30-46FF-B353-C8136966B81B}+00000000 DO Reference Object : {EC14494E-214C-4670-9268-A31687C7C852}+00000000 | {54933D63-7B30-46FF-B353-C8136966B81B}+00000000 DO Entity Width AutoResizeable : True | {54933D63-7B30-46FF-B353-C8136966B81B}+00000000 DO Entity Height AutoResizeable : True | {54933D63-7B30-46FF-B353-C8136966B81B}+00000000 Entity Def Font : {32F21E02-94E9-4859-8A57-F91E237956A7}+00000000 | {54933D63-7B30-46FF-B353-C8136966B81B}+00000000 Entity Fill Color : {A54B4541-336D-40B8-AD97-5D01A500BC48}+00000000 |
-----------------------
{98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 DO Text : 基数方案-方案配置 | {98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 DO Location : (214, 121, 351, 241) | {98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 DO Reference Object : {62F78F52-F570-4ED3-900D-862C877B0B1B}+00000000 | {98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 DO Entity Width AutoResizeable : True | {98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 DO Entity Height AutoResizeable : True | {98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 Entity Def Font : {643A447B-3F76-4B9D-850A-E5338AACA1B3}+00000000 | {98575776-B925-4C61-B816-ED8E29CDDA2B}+00000000 Entity Fill Color : {A54B4541-336D-40B8-AD97-5D01A500BC48}+00000000 |