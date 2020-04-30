#coding:utf-8
import win32com.client
import sys
from information import tables_not_logicalonly
scapi = win32com.client.Dispatch('ERwin.SCAPI')
erwin_filename = sys.argv[1]
#erwin_filename = '3'
erwin_dir = ("E:\\" + erwin_filename + ".ER1")
scPUnit = scapi.PersistenceUnits.Add(erwin_dir, "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root
scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
scSubArCol = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
scTablespaceCol = scSession.ModelObjects.Collect(scRootObj, 'DB2 UDB Tablespace')
scKeyGroupCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group')
scKeyGroupMemberCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group Member')

class Erwin_Wrongs:
    d_ent_nl = {}    # 所有表表名
    d_ent  = {}    # 表ID对应的表逻辑和物理名称
    same_name = []
    for ent in scEntObjCol:
        try:
            ent_logicalonly = ent.Properties('Logical Only').Value
        except Exception:
            ent_logicalonly = False
        if not ent_logicalonly:
            ent_pn = ent.Properties('Physical Name').Value
            ent_n  = ent.Name
            ent_id = ent.ObjectId
            if ent_pn == '%EntityName()':
                ent_pn = ent.Name
            if ent_pn == ent.Name:
                same_name.append(ent_pn)
            d_ent_nl.setdefault(ent_pn, []).append(ent_id)
            d_ent[ent_id] = (ent_pn, ent_n)
    @classmethod
    def tabs_name_dup(cls):
        '''
        查找重复表名及表重复次数
        '''
        return {key:len(value) for key,value in Erwin_Wrongs.d_ent_nl.items() if len(value) > 1}
    @classmethod
    def tabs_no_english(cls):
        same_name = []
        for i in  Erwin_Wrongs.d_ent.values():
            if i[0] == i[1]:
                same_name.append(i[0])
        return same_name
    def subarea_ent(self):
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
        tables_id = [item for item in mlid if item not in nmlid]
        tables_name = tables_not_logicalonly()
        return [tables_name[tid] for tid in tables_id]



if __name__ == '__main__':
    try:
        if Erwin_Wrongs.tabs_name_dup() == {}:
            print('恭喜你，数据模型中没有重复的表')
        else:
            print("重复的表名及重复次数：", Erwin_Wrongs.tabs_name_dup())
        if Erwin_Wrongs.tabs_no_english() == []:
            print('很好')
        else:
            print('缺失中文的表：', Erwin_Wrongs.tabs_no_english())
    except Exception as e:
        print("Error:" + str(e))
        print("Usage: 3.py erwin_filename (like 'PAS芯_数据模型DnS_V3.9')")
        sys.exit()
    