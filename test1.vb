public List<string> IterateObjectProperties(string objName)
{
ModelProperties scObjProperties;
List<string> result = new List<string>();
SCAPI.PersistenceUnit scPUnit;
// new session
SCAPI.Sessions scSessionCol = DmApp.Sessions;
SCAPI.Session scSession = scSessionCol.Add();
scPUnit = OpenModel("E:\\DW-Home\\0400逻辑数据模型\\详细
设计\\SPDB-EDW-LDM.ER1");
scSession.Open(scPUnit, SC_SessionLevel.SCD_SL_M0,
SC_SessionFlags.SCD_SF_NONE);
ModelObject scObj;
if (scSession.IsOpen())
{
if (null==objName )
scObj = scSession.ModelObjects.Root;
else
scObj = GetModelObject(scSession, objName);
if (scObj != null){
scObjProperties = scObj.Properties;
result.Add(scObj.Name + ":" + scObj.ClassName);
foreach (ModelProperty scObjProperty in
scObjProperties)
{
if (scObjProperty.Count <= 1)
{
result.Add("-->" +
scObjProperty.ClassName + "(" + scObjProperty.FormatAsString() + ")");
}
else
{
result.Add("-->" +
scObjProperty.ClassName + "[" + scObjProperty.Count + "]");
for (int i = 0; i < scObjProperty.Count;
i++)
{
result.Add("---->" +
scObjProperty.get_Value(i, SCAPI.SC_ValueTypes.SCVT_BSTR));
}
}
}
}
}
return result;
}