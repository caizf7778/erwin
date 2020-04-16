using System;
public void GetApplicationFeatures(SCAPI.Application scApp)
{
  Console.WriteLine("show all property:");
  // 取得全部应用环境属性
  SCAPI.PropertyBag scBag = scApp.ApplicationEnvironment.get_PropertyBag(null, null, true);
  PrintPropertyBag(scBag);
  Console.WriteLine("show all property:");
  // 1.获取全部Categories
  scBag = scApp.ApplicationEnvironment.get_PropertyBag(null,"Categories", true);
  if (scBag.get_Value("Categories").GetType().IsArray)
  {
    string[] aCategories =(string[])scBag.get_Value("Categories");
    if (aCategories.Length > 0)
    {
      // 2.将Categories中每个类别的属性打印出来
      foreach (string categoryName in aCategories)
      {
        scBag =scApp.ApplicationEnvironment.get_PropertyBag(categoryName, null, true);
        Console.WriteLine("Values for the " + categoryName + " category:");
        PrintPropertyBag(scBag);
      }
    }
  }
  // 3. 得到Api属性值
  Console.WriteLine("show api version");
  scBag = scApp.ApplicationEnvironment.get_PropertyBag("Application.API", "APIVersion", true);
  PrintPropertyBag(scBag);
}
private void PrintPropertyBag(PropertyBag scBag)
{
  if (scBag != null)
  {
    for (int i = 0; i < scBag.Count; i++)
    {
      if (scBag.get_Value(i).GetType().IsArray)
      {
        string[] values = (string[])scBag.get_Value(i);
        if (values.Length > 0)
        {
          Console.WriteLine(i + ")" + scBag.get_Name(i) + " is an array:");
          foreach (string value in values)
          {
            System.Console.WriteLine("\t" + value);
          }
        }
      }
      else
        Console.WriteLine(i + ")" + scBag.get_Name(i) + " = " + scBag.get_Value(i));
    }
  }
}