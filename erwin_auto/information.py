# coding:utf-8
import win32com.client
from collections import defaultdict
from pywintypes import com_error
scapi = win32com.client.Dispatch('ERwin.SCAPI')
scPUnit = scapi.PersistenceUnits.Add(r"E:\HZPAS.er1", "RDO=Yes")
scSession = scapi.Sessions.Add()
scSession.Open(scPUnit, 0, 0)
scRootObj = scSession.ModelObjects.Root

scKeyGroupCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group')
scKeyGroupMemberCol = scSession.ModelObjects.Collect(scRootObj, 'Key Group Member')

class Tables:
    scEntObjCol = scSession.ModelObjects.Collect(scRootObj, 'Entity')
    @classmethod
    def tab_check(cls, id=None, tabname=None, physical_name=None):
        tabs = []
        lst = []
        for ent in Tables.scEntObjCol:
            tab_id = ent.ObjectId
            name = ent.Name.upper()
            name2 = ent.Properties('Physical Name').Value.upper()
            if name2 == '%ENTITYNAME()':
                name2 = name
            try:
                ent_logicalonly = ent.Properties('Logical Only').Value
            except Exception as e:
                ent_logicalonly = False
            if not ent_logicalonly:
                tabs.append((tab_id,name,name2))
        if (id or tabname or physical_name) !=None:
            for tab in tabs:
                if tab[0] == id and tabname == physical_name == None:
                    lst.append((tab[1],tab[2]))
                if tab[1] == tabname and id == physical_name == None:
                    lst.append((tab[0],tab[2]))
                if tab[2] == physical_name and id == tabname == None:
                    lst.append((tab[0],tab[1]))
            if lst == []:
                raise KeyError
            return lst
        if (id or tabname or physical_name) == None:
            return tabs
    @classmethod
    def not_logicalonly(cls):
        '''
        返回表名和ID(删减LogicalOnly)
        '''
        ent_nlo = {}
        for ent in Tables.scEntObjCol:
            try:
                ent_logicalonly = ent.Properties('Logical Only').Value
            except Exception as e:
                ent_logicalonly = False
            if not ent_logicalonly:
                ent_nlo[ent.ObjectId] = ent.Name.upper()
        return ent_nlo
    class Check:
        def __init__(self, tablename):
            self.tablename = tablename
        def get_tablename(self):
            return self.tablename
        def get_tableid(self):
            try:
                id = Tables.tab_check(tabname=self.tablename)
            except KeyError as e:
                return False
            else:
                if len(id)>=2:
                    return list(zip(*id))[0]
                else:
                    return id[0][0]
        def get_physicalname(self):
            try:
                physicalname = Tables.tab_check(tabname=self.tablename)
            except KeyError as e:
                return False
            else:
                if len(physicalname)>=2:
                    return list(zip(*physicalname))[1]
                return physicalname[0][1]
        @classmethod
        def by_physicalname(cls, physical_name):
            try:
                tablename = Tables.tab_check(physical_name=physical_name)[0][1]
            except KeyError as e:
                return False
            else:
                return cls(tablename)
        @classmethod
        def by_tableid(cls, tableid):
            try:
                tablename = Tables.tab_check(id=tableid)[0][0]
            except KeyError as e:
                return False
            else:
                return cls(tablename)
        def structure(self):
            '''
            以字典形式返回所查表的表结构（字段名,字段类型和字段空值设置）
            '''
            l_cols = []
            id_num = Tables.Check(self.tablename).get_tableid()
            tab_col = scSession.ModelObjects.Collect(self.get_tableid())
            if len(id_num)==1:
                for att in tab_col:
                    try:
                        type = att.Properties("Type").Value
                    except Exception as e:
                        type = False
                    else:
                        if type in[0, 100]:
                            apn = att.Properties('Physical Name').Value # 字段物理名称(英文)
                            an = att.Properties('Name').Value # 字段名称(中文)
                            adt = att.Properties('Datatype').Value # 字段数据类型
                            ano = att.Properties('Null Option').Value # 字段空值设置
                            if apn == '%AttName':
                                apn = att.Name
                            if ano == 1:
                                ano = 'Not Null'
                            if ano == 0:
                                    ano = 'Null'
                            d_att = {}
                            d_att[apn] = (adt, ano, an)
                            l_cols.append(d_att)
                return l_cols
            else:
                print('存在多张相同的表，无法查询表结构,请通过get_tableid()方法获得表ID，然后进行比较！')
                return False
    class Differents:
        def __init__(self, tab1 , tab2=None):
            self.tab1 = tab1
            if tab2 == None:
                self.tab2 = tab1
            else:    
                self.tab2 = tab2
        def compare(self):
            tc = Tables.Check(tablename=self.tab1)
            if tab2 == None:
                tab_id = tc.get_tableid()
                if len(tab_id) == 1:
                    print('单表无法比对，请添加tab2')
                    return False
                if len(tab_id) ==2:
                    tab1_id = tab_id[0]
                    tab2_id = tab_id[1]
                    tc.
            tab1_col_nums = Tables.Check.by_tableid(tab1_id).get_tablename()
            
    class Columns:
        scAttCol = scSession.ModelObjects.Collect(scRootObj, 'Attribute')
        @classmethod
        def name(cls):
            '''
            返回字段ID及字段名(删减LogicalOnly)
            '''
            att_nlo = {}
            for att in Tables.Columns.scAttCol:
                try:
                    att_logicalonly = att.Properties('Logical Only').Value
                except Exception:
                    att_logicalonly = False
                if not att_logicalonly:
                    att_nlo[att.ObjectId] = att.Name
            return att_nlo
        @classmethod
        def dictionary1(cls):
            '''
            返回字典类型的字段词典
            '''
            allcolumn = []
            for scAtt in Tables.Columns.scAttCol:
                sn = scAtt.Name
                spn = scAtt.Properties('Physical Name').Value
                if sn != spn and spn !='%AttName':
                    allcolumn.append((spn.upper(), sn))
            removal = set(allcolumn)
            d = {}
            for en,zh in removal:
                d.setdefault(en, []).append(zh)
            return d
        @classmethod
        def dictionary2(cls):
            '''
            返回defaultdict(<class 'list'>类型的字段词典，可通过append()方法添加键值对
            '''
            allcolumn = []
            for scAtt in Tables.Columns.scAttCol:
                sn = scAtt.Name
                spn = scAtt.Properties('Physical Name').Value
                if sn != spn and spn !='%AttName':
                    allcolumn.append((spn.upper(), sn))
            removal = set(allcolumn)
            d = defaultdict(list)
            for en,zh in removal:
                d[en].append(zh)
            return d



# a = Tables()
# a.tab_check()
# a.tab_check(id='{2CBC06BF-CB81-4474-A193-B4CE5D13B61E}+00000000')
# a.tab_check(tabname='临时表-指标链接明细')
# a.tab_check(physical_name='JXBG_MBZT')
# a.tab_check(id='{2CBC06BF-CB81-4474-A193-B4CE5D13B61E}+0000test')
# a.tab_check(tabname='test')
# a.tab_check(physical_name='test')
# a.not_logicalonly()
# b = a.Check.by_physicalname('XTB_ZDYSQL')
# b.get_tablename()
# b.get_tableid()
# b.get_physicalname()
# b.structure()
# b1 = a.Check(tablename='SGLR_DKZHJGGS')
# b1.get_tableid()
# b1.structure()
# c = a.Check.by_tableid('{408FF321-E61E-4909-A8C3-1602EB6B1AD9}+00000000')
# c.get_tableid()
# c.get_physicalname()
# c.get_tablename()
# c.structure()
# d = Tables.Columns.name()
# e = Tables.Columns.dictionary1()
# f = Tables.Columns.dictionary2()


class SubjectArea:
    subarea_col = scSession.ModelObjects.Collect(scRootObj, 'Subject Area')
    @classmethod
    def areas(cls):
        return {area.Name:area.ObjectId for area in SubjectArea.subarea_col}
    class Check:
        def __init__(self, areaname):
            self.areaname = areaname
        def get_areaname(self):
            return self.areaname
        def get_areaid(self):
            try:
                id = SubjectArea.areas()[self.areaname]
            except KeyError as e:
                print('该域名不存在！')
                return False
            else:
                return id
        def is_exist(self):
            if self.areaname in SubjectArea.areas().keys():
                return True
            if self.areaname not in SubjectArea.areas().keys():
                return False
        def get_tables(self):
            if self.is_exist():
                d_sub = {}
                l_tab = []
                for sub in SubjectArea.subarea_col:
                    if sub.Name == self.areaname:
                        draw_tab_col =  scSession.ModelObjects.Collect(sub, 'Drawing Object Entity')
                        for tabs in draw_tab_col:
                            l_tab.append(tabs.Properties('DO Text').Value)
                        d_sub[sub.name] = l_tab
                return d_sub
            else:
                print('no space,no tables!')
                return False
    class Add:
        def __init__(self, areaname):
            self.areaname = areaname
        def new_area(self):
            if SubjectArea.Check(self.areaname).is_exist():
                print('该域名已存在！')
                return False
            else:
                scTranId = scSession.BeginTransaction()
                oarea = scSession.ModelObjects.Add("Subject Area")
                oarea.Properties("Name").Value = self.areaname
                try:
                    scSession.CommitTransaction (scTranId)
                except com_error as e:
                    scSession.RollbackTransaction(scTranId)
                    print('域创建失败！')
                    return False
                else:
                    print('域创建成功！')
                    return True

# b = SubjectArea()
# b.areas()
# c = b.Check('手工录入数据')
# c.get_areaid()
# c.get_areaname()
# c.get_tables()
# c.is_exist()
# d = b.Check('tset')
# d.is_exist()
# e = b.Add('手工录入数据')
# e.new_area()
# f = b.Add('手工录入数据')
# f.new_area() 

class Tablespace:
    tablespace_col = scSession.ModelObjects.Collect(scRootObj, 'DB2 UDB Tablespace')
    @classmethod
    def spaces(cls):
        return {space.Name:space.ObjectID for space in Tablespace.tablespace_col}
    class Check:
        def __init__(self, spacename):
            self.spacename = spacename
        def get_spacename(self):
            return self.spacename
        def get_spaceid(self):
            try:
                id = Tablespace.spaces()[self.spacename]
            except KeyError as e:
                return False
            else:
                return id
        def is_exist(self):
            if self.spacename in Tablespace.spaces().keys():
                return True
            if self.spacename not in Tablespace.spaces().keys():
                return False
    class Add:
        def __init__(self, spacename):
            self.spacename = spacename
        def new_space(self):
            if Tablespace.Check(self.spacename).is_exist():
                print('该表空间已存在！')
                return False
            else:
                scTranId = scSession.BeginTransaction()
                otabspace = scSession.ModelObjects.Add("DB2 UDB Tablespace")
                otabspace.Properties("Name").Value = self.spacename
                try:
                    scSession.CommitTransaction (scTranId)
                except com_error as e:
                    scSession.RollbackTransaction(scTranId)
                    print('表空间创建失败！')
                    return False
                else:
                    print('表空间创建成功！')
                    return True

# t = Tablespace()
# t.spaces()
# k = t.Check('TBS_IDX')
# k.get_spaceid()
# k.get_spacename()
# k.is_exist()
# l = t.Add('TBS_IDX')
# l.new_space()
# m = t.Add('ABC')
# m.new_space()

# 事务控制-开始
# scTranId = scSession.BeginTransaction()
# 事务控制-结束（提交）
# scSession.CommitTransaction (scTranId)
# 事务控制-回滚
# scSession.RollbackTransaction(scTranId)
# 关闭scSession
# scSession.Close()
# scapi.Sessions.Remove(scSession)
# 模型另存为（newfilename为新模型的路径）
# scPUnit.Save(newfilename)
# 断开内存中模型的连接
# scapi.PersistenceUnits.clear()
# scPUnit = None
# scSession = None