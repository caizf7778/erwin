#!/usr/bin/python
# -*- coding: cp936 -*-
# robot_lei
import win32com.client
import re
 
 
# 创建COM对象
scapi = win32com.client.Dispatch('AllFusionERwin.SCAPI')
# conn=win32com.client.Dispatch('ADODB.Connection')
# 建立与持久装置中模型的连接
# 源文件
filename = "E:\\3.9.erwin"
# 目标文件
newfilename = "C:\\MGDB_MODEL1.erwin"
scPUnit = scapi.PersistenceUnits.Add(filename, "RDO=yes")
# 建立存取内存中模型数据的连接
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
# 事务控制
scTranId = scSession.BeginTransaction()
# 获取所有Entity模型对象
scMObjects = scSession.ModelObjects.Collect(scSession.ModelObjects.Root, 'Entity', 1)
scSubjectArea = scSession.ModelObjects.Collect(scSession.ModelObjects.Root, 'Subject_Area')
for scObj in scMObjects:
    # 取Definition属性的值
    try:
        scDefineName = scObj.Properties('Definition').Value
    except Exception as ex:
        scDefineName = ''
    try:
        scName = scObj.Properties('Name').Value
    except Exception as ex:
        scName = ''
    # 对象名赋值
    # print "His scName is %s" % scName
    # print "His scDefineName is %s" % scDefineName
    scObj.Properties('Physical_Name').Value = scName
    scObj.Properties('Name').Value = scDefineName
    # 获取该Entity的所有Attribute对象
    scAttrObjects = scSession.ModelObjects.Collect(scObj, 'Attribute', 1)
    for scAttrObj in scAttrObjects:
        try:
            scAttrDefineName = scAttrObj.Properties('Definition').Value
        except Exception as ex:
            scAttrDefineName = ''
        try:
            scAttrName = scAttrObj.Properties('Name').Value
        except Exception as ex:
            scAttrName = ''
        # 对象名赋值
        scAttrObj.Properties('Physical_Name').Value = scAttrName
        # 注释可能带有括号之类的 这边做了特殊处理，不要处理的直接注释掉if代码即可
        if scAttrDefineName != '':
            scAttrDefineName = scAttrDefineName.replace('（', '(')
            is_find = re.findall(r'\(', scAttrDefineName)
            if is_find:
                scAttrDefineName = re.findall(r'(.*?)\(', scAttrDefineName)
                scAttrDefineName = scAttrDefineName[0]
        scAttrObj.Properties('Name').Value = scAttrDefineName
scSession.CommitTransaction(scTranId)
# 另存为一个新的文件
scPUnit.Save(newfilename, 'OVF=yes')