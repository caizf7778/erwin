#coding:utf-8
import win32com.client

scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\10.er1", "RDO=Yes")
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
    oEntity = scSession.ModelObjects.Add("Entity")  # 创建表至少需要Type属性
    oEntity.Properties("Name").Value = 'AAAAA'
    oEntity.Properties("Type").Value = 1    # 类型1为表
    
oAttribute = scSession.ModelObjects.Collect(oEntity).Add("Attribute")   # 创建字段至少需要Type属性

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
oAttribute.Properties("Type").Value = 0     # 类型0为字段
oAttribute.Properties("Attribute Required").Value = False
oAttribute.Properties("Order").Value = 2
oAttribute.Properties("Datatype").Value = "DECIMAL(25,4)"
oAttribute1 = scSession.ModelObjects.Collect(oEntity).Add("Attribute")
oAttribute1.Properties("Name").Value = "字段a"
oAttribute1.Properties("Type").Value = 100 # 0是字段的意思
oAttribute1.Properties("Attribute Required").Value = True
oAttribute1.Properties("Physical Name").Value = "qsrq"
oAttribute1.Properties("Order").Value = 1

oIndex = scSession.ModelObjects.Collect(oEntity).Add("Key Group")  
oIndex.Properties("Key Group Type").Value = PK


{'Definition', 'Name', 'Entity Fill Color', 'Type', 'Index Generate', 'Physical Name', 'DB2UDB INDEX TABLESPACE', 'DB2UDB TABLESPACE',
 'DB Owner', 'DB2UDB PARTITIONING KEY', 'Physical Only'}


Name : 团队任务-临时任务 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_LSRW | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------
Name : 团队任务-临时任务人员安排 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_LSRWRYAP | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------
Name : 团队任务-任务审批 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_RWSP | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------
Name : 团队任务-任务审批明细 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_RWSPMX | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------
Name : 团队任务-任务状态 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_RWZT | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------
Name : 团队任务-周期任务 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_ZQRW | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------
Name : 团队任务-周期任务明细 | Type : 1 | Definition :  | Index Generate : 1 | DB Owner : PAS | Physical Only : False | Physical Name : TDRW_ZQRWMX | DB2UDB TABLESPACE : {5ABF1825-C6FD-462B-90C9-71BD2994D4BE}+00000000 | DB2UDB INDEX TABLESPACE : {F84A8A27-4B39-4639-B53B-9344E7465876}+00000000 | DB2UDB PARTITIONING KEY :  | Entity Fill Color : {FDEFE491-D90E-4AAF-9C78-5ADF15DF3D15}+00000000 |
-----------------------



Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 2 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 主题编号 | Type : 100 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 3 | Physical Name : ztbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 主题名称 | Type : 100 | Datatype : VARCHAR(200) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 1 | Physical Name : ztmc | Logical Datatype : VARCHAR(200) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 任务内容 | Type : 100 | Datatype : VARCHAR(2000) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 11 | Physical Name : rwnr | Logical Datatype : VARCHAR(2000) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 开始日期 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 4 | Physical Name : ksrq | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 4 |
-----------------------
Name : 截止日期 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 5 | Physical Name : jzrq | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 5 |
-----------------------
Name : 优先级别 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 7 | Physical Order : 6 | Physical Name : yxjb | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 6 |
-----------------------
Name : 标准分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 8 | Physical Order : 7 | Physical Name : bzf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 7 |
-----------------------
Name : 最高分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 9 | Physical Order : 8 | Physical Name : zgf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 8 |
-----------------------
Name : 最低分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 10 | Physical Order : 9 | Physical Name : zdf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 9 |
-----------------------
Name : 默认分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 11 | Physical Order : 10 | Physical Name : mrf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 10 |
-----------------------
Name : 创建人 | Type : 100 | Datatype : VARCHAR(12) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 12 | Physical Order : 13 | Physical Name : cjr | Logical Datatype : VARCHAR(12) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 11 |
-----------------------
Name : 创建时间 | Type : 100 | Datatype : TIMESTAMP | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 13 | Physical Order : 12 | Physical Name : cjsj | Logical Datatype : TIMESTAMP | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 12 |
-----------------------
Name : 修改人 | Type : 100 | Datatype : VARCHAR(12) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 14 | Physical Order : 14 | Physical Name : xgr | Logical Datatype : VARCHAR(12) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 13 |
-----------------------
Name : 修改时间 | Type : 100 | Datatype : TIMESTAMP | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 15 | Physical Order : 15 | Physical Name : xgsj | Logical Datatype : TIMESTAMP | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 14 |
-----------------------
Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 2 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 考核对象代号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 1 | Physical Name : khdxdh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 人员角色 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 4 | Physical Name : ryjs | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 责任比例 | Type : 100 | Datatype : DECIMAL(9,5) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 3 | Physical Name : zrbl | Logical Datatype : DECIMAL(9,5) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 1 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 任务类型 | Type : 0 | Datatype : VARCHAR(2) | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 4 | Physical Name : rwlx | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 任务期数 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 9 | Physical Name : rwqs | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 审批方式 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 8 | Physical Name : spfs | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 审批人 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 2 | Physical Name : spr | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 4 |
-----------------------
Name : 审批日期 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 3 | Physical Name : sprq | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 5 |
-----------------------
Name : 总体评价 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 7 | Physical Order : 6 | Physical Name : ztpj | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 6 |
-----------------------
Name : 评语 | Type : 100 | Datatype : VARCHAR(2000) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 8 | Physical Order : 7 | Physical Name : py | Logical Datatype : VARCHAR(2000) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 7 |
-----------------------
Name : 总分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 9 | Physical Order : 5 | Physical Name : zf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 8 |
-----------------------
Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 1 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 主题编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 2 | Physical Name : ztbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 任务类型 | Type : 0 | Datatype : VARCHAR(2) | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 6 | Physical Name : rwlx | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 任务期数 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 4 | Physical Name : rwqs | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 评价标准 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 3 | Physical Name : pjbz | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 4 |
-----------------------
Name : 评价分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 5 | Physical Name : pjf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 5 |
-----------------------
Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 1 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 主题编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 2 | Physical Name : ztbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 任务类型 | Type : 0 | Datatype : VARCHAR(2) | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 3 | Physical Name : rwlx | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 任务期数 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 4 | Physical Name : rwqs | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 任务状态 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 5 | Physical Name : rwzt | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 4 |
-----------------------
Name : 审批状态 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 6 | Physical Name : spzt | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 5 |
-----------------------
Name : 任务进度 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 7 | Physical Order : 7 | Physical Name : rwjd | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 6 |
-----------------------
Name : 完成日期 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 8 | Physical Order : 8 | Physical Name : wcrq | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 7 |
-----------------------
Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 1 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 责任人 | Type : 100 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 5 | Physical Name : zrr | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 任务年份 | Type : 100 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 2 | Physical Name : rwnf | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 任务周期 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 3 | Physical Name : rwzq | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 任务期数 | Type : 100 | Datatype : VARCHAR(100) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 4 | Physical Name : rwqs | Logical Datatype : VARCHAR(100) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 4 |
-----------------------
Name : 审批人 | Type : 100 | Datatype : INTEGER | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 6 | Physical Name : spr | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 5 |
-----------------------
Name : 总分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 7 | Physical Order : 7 | Physical Name : zf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 6 |
-----------------------
Name : 任务编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 1 | Physical Order : 1 | Physical Name : rwbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 0 |
-----------------------
Name : 主题编号 | Type : 0 | Datatype : INTEGER | Attribute Required : True | Null Option : 1 | Label : %AttName: | Header : %AttName | Order : 2 | Physical Order : 9 | Physical Name : ztbh | Logical Datatype : INTEGER | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 1 |
-----------------------
Name : 主题名称 | Type : 100 | Datatype : VARCHAR(200) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 3 | Physical Order : 2 | Physical Name : ztmc | Logical Datatype : VARCHAR(200) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 2 |
-----------------------
Name : 任务内容 | Type : 100 | Datatype : VARCHAR(2000) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 4 | Physical Order : 4 | Physical Name : rwnr | Logical Datatype : VARCHAR(2000) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 3 |
-----------------------
Name : 优先级别 | Type : 100 | Datatype : VARCHAR(2) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 5 | Physical Order : 3 | Physical Name : yxjb | Logical Datatype : VARCHAR(2) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 4 |
-----------------------
Name : 标准分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 6 | Physical Order : 5 | Physical Name : bzf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 5 |
-----------------------
Name : 最高分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 7 | Physical Order : 6 | Physical Name : zgf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 6 |
-----------------------
Name : 最低分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 8 | Physical Order : 7 | Physical Name : zdf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 7 |
-----------------------
Name : 默认分 | Type : 100 | Datatype : DECIMAL(25,4) | Attribute Required : False | Null Option : 0 | Label : %AttName: | Header : %AttName | Order : 9 | Physical Order : 8 | Physical Name : mrf | Logical Datatype : DECIMAL(25,4) | Parent Domain : {39146A35-A713-4CAA-9FBF-9AA575FA9F44}+00000001 | Object Order : 8 |
-----------------------



Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {9ADA9AB0-6F04-4C21-B9B2-DABC370B29BF}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {D34AE072-2298-4A09-B68D-745644234360}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Member Column : {15954AAB-8BBD-4817-8D02-5CC44B0CE296}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
-----------------------
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {917C2FFF-5CF6-4784-9D9D-5CED1920BB02}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Member Column : {E15026BE-9C6D-42FE-AEEE-928B75D159B7}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
-----------------------
Key Group Member Column : {1E15C216-86EC-4146-9386-AC8BB6DF6E8D}+00000000 | Key Group Sort Order : ASC | Key Group Position : 3 |
-----------------------
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {7AA985E3-8E69-4483-89AD-675606426786}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Member Column : {D12524E1-67B0-4464-9668-E87B62379EEE}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
-----------------------
Key Group Member Column : {5E5F06C2-437D-40FF-B2EB-EA8554945B44}+00000000 | Key Group Sort Order : ASC | Key Group Position : 3 |
-----------------------
Key Group Member Column : {80AE06E0-33CF-4D7B-94C6-3AEA5C388763}+00000000 | Key Group Sort Order : ASC | Key Group Position : 4 |
-----------------------
Key Group Type : AK1 | Index Generate : 1 | Index Clustered : 2 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {D12524E1-67B0-4464-9668-E87B62379EEE}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Member Column : {7AA985E3-8E69-4483-89AD-675606426786}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
-----------------------
Key Group Type : IE1 | Index Generate : 1 | Index Clustered : 2 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {D12524E1-67B0-4464-9668-E87B62379EEE}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {C3E63CAE-CEAE-4F75-92DA-2DE93360C3C3}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Member Column : {E4582CDF-AD8F-4ADD-9EA8-1EBBC4BAEC53}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
-----------------------
Key Group Member Column : {14FBB924-FCE4-48BA-A139-C7F4C3B5BF2D}+00000000 | Key Group Sort Order : ASC | Key Group Position : 3 |
-----------------------
Key Group Member Column : {7A45ECC7-F3EB-47A0-929D-EC19FAAF78D7}+00000000 | Key Group Sort Order : ASC | Key Group Position : 4 |
-----------------------
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {A1A65D91-C306-4DCE-90B9-C5F2411BD6E4}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Type : PK | Index Generate : 1 | DB Owner : ODSFDM | Physical Name : X%KeyType%TableName |
-----------------------
Key Group Member Column : {10F4E7E6-7D09-48D2-AB4E-894794B5B5AA}+00000000 | Key Group Sort Order : ASC | Key Group Position : 1 |
-----------------------
Key Group Member Column : {69F8E1C7-1D06-4ECD-B038-2DA5D858A04D}+00000000 | Key Group Sort Order : ASC | Key Group Position : 2 |
-----------------------

Name : <Main Subject Area> | Definition :  | Referenced Entities : {83EF5EF2-8B7D-4FF5-8A7F-AD239649D17E}+00000000 | Author :  | Created Time : 1585213033 | Modified Time : 1585213105 | Is Locked : True | Filter Dangling Rels from Schema Gen : False | Current Stored Display of SA : 0 | Object Order : 0 | Current Subject Area : True | 
-----------------------
Name : H6团队任务 | Definition :  | Referenced Entities : {16D50631-0301-4835-BFE2-9BAC3A88E7CE}+00000000 | Author :  | Created Time : 1585213133 | Modified Time : 1585213156 | Is Locked : True | Filter Dangling Rels from Schema Gen : False | Current Stored Display of SA : 0 | Object Order : 1 | Current Subject Area : False |
-----------------------


Name : <Main Subject Area> | Definition :  | Referenced Entities : {83EF5EF2-8B7D-4FF5-8A7F-AD239649D17E}+00000000 | Author :  | Created Time : 1585213033 | Modified Time : 1585213105 | Is Locked : True | Filter Dangling Rels from Schema Gen : False | Current Stored Display of SA : 0 | Object Order : 0 | Current Subject Area : True | 
-----------------------
Name : H6团队任务 | Definition :  | Referenced Entities : {16D50631-0301-4835-BFE2-9BAC3A88E7CE}+00000000 | Author :  | Created Time : 1585213133 | Modified Time : 1585213156 | Is Locked : True | Filter Dangling Rels from Schema Gen : False | Current Stored Display of SA : 0 | Object Order : 1 | Current Subject Area : False |
-----------------------

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





