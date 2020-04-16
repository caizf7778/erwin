Public Sub Main()
    Sub Main()
        Dim oApi As New SCAPI.Application
        Dim oBag As New SCAPI.PropertyBag
        Dim oPU As SCAPI.PersistenceUnit

        ' Construct a new logical-physical model. Accept the rest as defaults
        oBag.Add("Model_Type", "Combined")
        oPU = oApi.PersistenceUnits.Create(oBag)

        ' Clear the bag for the future reuse
        oBag.ClearAll()

        ' Start a session
        Dim oSession As SCAPI.Session

        oSession = oApi.Sessions.Add
        oSession.Open(oPU)

        ' Prepare a property bag with the transaction properties
        oBag.Add("History_Description", "API History Tracking")

        ' Start a transaction
        Dim nTransId As Object

        nTransId = oSession.BeginNamedTransaction("Create Entity and Attribute", oBag)

        ' Create an entity and an attribute
        Dim oEntity As SCAPI.ModelObject
        Dim oAttribute As SCAPI.ModelObject

        oEntity = oSession.ModelObjects.Add("Entity")
        oAttribute = oSession.ModelObjects.Collect(oEntity).Add("Attribute")
        oAttribute.Properties("Name").Value = "Attr A"

        ' Commit
        oSession.CommitTransaction(nTransId)

    End Sub