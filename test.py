#coding:utf-8
import win32com.client
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

scRootObj.Remove()


sctest = scSession.ModelObjects.Collect('{2BD6BF59-8FE1-4D6C-B891-E996FB3335C8}+00000000')
for i in sctest:
    for j in i.Properties:
        try:md
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

def add_table_head(tablename):
    '''
    只创建表名，没有任何字段
    '''
    scTranId = scSession.BeginTransaction()
    oEntity = scSession.ModelObjects.Add("Entity")  # 创建表至少需要Type属性
    oEntity.Properties("Name").Value = tablename
    oEntity.Properties("Type").Value = 1    # 值为1表示为表
    scSession.CommitTransaction (scTranId)
    return oEntity.ObjectId
    
    
  # 创建字段至少需要Type属性
def add_column()
oEntity.Properties("Physical Only").Value = False   # 是否仅在物理模式下显示
oEntity.Properties("DB2UDB TABLESPACE").Value = "{3CBD15DD-C280-46DA-A7CF-E5FA9DB42D9F}+00000000"   # 表空间
oEntity.Properties("DB2UDB INDEX TABLESPACE").Value = "{9CB8D5C1-DD33-4A33-B6E2-8A8BC817E78D}+00000000"     # 索引表空间
oEntity.Properties("Index Generate").Value = 1
oEntity.Properties("Physical Name").Value = "jxdx_ckzh"
oEntity.Properties("Entity Fill Color").Value = "{73A29D04-3F67-4DD4-9CDE-5BEFFE2EBCD3}+00000000"
oEntity.Properties("DB2UDB PARTITIONING KEY").Value = ""
oEntity.Properties("Definition").Value = ""



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





