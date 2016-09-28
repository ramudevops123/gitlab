from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import connection
from time import time


# Create your models here.

def get_upload_file_name(instance,filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)

class Users(models.Model):
    FirstName=models.CharField(max_length=30)
    LastName=models.CharField(max_length=30)
    Email=models.EmailField(max_length=75)
    Role=models.CharField(max_length=30)
    Permissions=models.CharField(max_length=300)
    Status=models.CharField(max_length=30)
    CreatedDate=models.DateTimeField(auto_now_add=True)
    ModifiedDate=models.DateTimeField(auto_now=True)


class MsProduct(models.Model):
   ProductID=models.CharField(max_length=30)
   PrincipalID=models.CharField(max_length=20,blank=True)
   PrincipalName=models.CharField(max_length=30)
   ProductType=models.CharField(max_length=30)
   ProductName=models.CharField(max_length=30)
   ProductModel=models.CharField(max_length=30)
   #ProductRequireSN=models.CharField(max_length=30)
   ProductStatus=models.CharField(max_length=30)
   ProductSerialNumber=models.CharField(max_length=30)
   CreatedOn=models.DateTimeField(auto_now_add=True)
   CreatedBy=models.CharField(max_length=30)
   LastUpdateOn=models.DateTimeField(auto_now_add=True)
   LastUpdateBy=models.CharField(max_length=30)


class UserPrivileges(models.Model):
    User=models.CharField(max_length=30)
    PrivilegeType=models.CharField(max_length=30)
    PrivilegeValue=models.CharField(max_length=30)
    my_field = models.BooleanField(default=True)


class ProductType(models.Model):
    ProductType=models.CharField(max_length=30)

class Privilege_Permissions(models.Model):
    User=models.CharField(max_length=30)
    Permissions=models.CharField(max_length=300)
    
class ThirdParty(models.Model):
   ThirdPartyID=models.CharField(max_length=20,blank=True)
   ThirdPartyName=models.CharField(max_length=30)
   ThirdPartyType=models.CharField(max_length=30)
   ThirdPartyAddress=models.CharField(max_length=300)
   ThirdPartyCountry=models.CharField(max_length=30)
   ThirdPartyCiy=models.CharField(max_length=30)
   ThirdPartyWebsite=models.CharField(max_length=30)
   ThirdPartyEmail=models.CharField(max_length=75)
   ThirdPartyPhNo=models.IntegerField(max_length=20)
   ThirdPartyComments=models.CharField(max_length=300)
   ThirdPartyStatus=models.CharField(max_length=30)
   DataExportStatus=models.CharField(max_length=30)
   DataExportQty=models.CharField(max_length=30)
   CreatedOn=models.DateTimeField(auto_now_add=True)
   CreatedBy=models.CharField(max_length=30)
   LastUpdateOn=models.DateTimeField(auto_now_add=True)
   LastUpdateBy=models.CharField(max_length=30)


class WareHouse(models.Model):
    WarehouseID=models.CharField(max_length=30)
    WarehouseName=models.CharField(max_length=30)
    ThirdPartyName=models.CharField(max_length=30)
    WarehouseStatus=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class MsBOMHeader(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductModel=models.CharField(max_length=30)
    ProductStatus=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class MsBOMDetail(models.Model):
    ProductID=models.CharField(max_length=30)
    MaterialCode=models.CharField(max_length=30)
    MaterialName=models.CharField(max_length=30)
    MaterialQty=models.CharField(max_length=30)
	
class TxPurchaseOrderHdr(models.Model):
    PONumber=models.CharField(max_length=20,blank=True)
    PODate=models.DateField(max_length=30)
    PrincipalId=models.CharField(max_length=30)
    PrincipalName=models.CharField(max_length=30)
    POStatus=models.CharField(max_length=30)
    MaterialCount=models.IntegerField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxPurchaseOrderDtl(models.Model):
    PONumber=models.CharField(max_length=20,blank=True)
    ProductId=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    POReceivingQty=models.CharField(max_length=30)
    Quantity=models.CharField(max_length=30)
    EstimatedDeliveryDate=models.DateField(max_length=30)
    POStatus=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)


class ShipmentFromManufacture(models.Model):
    PONumber=models.CharField(max_length=30)
    PODate=models.DateField(auto_now_add=True)
    ProductID=models.CharField(max_length=30)
    EstimatedDelivery=models.DateField(auto_now_add=True)
    ShipNumber=models.CharField(max_length=30)
    ShipDate=models.DateField(auto_now_add=True)
    ShipAWB=models.CharField(max_length=30)
    ShipFreightName=models.CharField(max_length=30)
    ShipmentQuantity=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class CustomClearance(models.Model):
    PONumber=models.CharField(max_length=30)
    PODate=models.DateField(auto_now_add=True)
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    POQuantity=models.CharField(max_length=30)
    #POStatus=models.CharField(max_length=30)
    PrincipalID=models.CharField(max_length=30)
    PrincipalName=models.CharField(max_length=30)
    EstimatedDeliveryDate=models.DateField(max_length=30)
    ShipNumber=models.CharField(max_length=30)
    ShipDate=models.DateField(auto_now_add=True)
    ShipAWB=models.CharField(max_length=30)
    ShipFreightName=models.CharField(max_length=30)
    ShipmentQuantity=models.CharField(max_length=30)
    HsCode=models.CharField(max_length=30)
    StartDate=models.DateField(max_length=30)
    CustomClearanceStatus=models.CharField(max_length=30)
    FinishDate=models.DateField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)
    
class TxReceivingFG_Material(models.Model):
    ReceivingID=models.CharField(max_length=30)
    PONumber=models.CharField(max_length=30)
    POLineProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ShipmentNo=models.CharField(max_length=30)
    HsCode=models.CharField(max_length=30)
    ShipmentQty=models.CharField(max_length=30)
    ReceivingQty=models.CharField(max_length=30)
    POQuantity=models.CharField(max_length=30)
    ReceivingStatus=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxStockSN(models.Model):
    ProductID=models.CharField(max_length=30)
    ShipmentNo=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductType=models.CharField(max_length=30)
    SerialNumber=models.CharField(max_length=30)
    SNStatus=models.CharField(max_length=30)
    RefNumber=models.CharField(max_length=30)
    AdjustmentStockID=models.CharField(max_length=30)
    InputStockRefNumber=models.CharField(max_length=30)
    SAMRefNumber=models.CharField(max_length=30)
    ReceivingFinishGoodSAMID=models.CharField(max_length=30)
    ShipToCustomerID=models.CharField(max_length=30)
    AdjustmentType=models.CharField(max_length=30)
    CreatedOn=models.DateField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)
    

class txStock(models.Model):
    RefNumber=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    ShipmentNo=models.CharField(max_length=30)
    StockQtyIN=models.CharField(max_length=30)
    StockQtyOut=models.CharField(max_length=30)
    StockQtyBalance=models.CharField(max_length=30)
    StockSN=models.CharField(max_length=30)
    PrincipalName=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ADJIOStockStatus=models.CharField(max_length=30)
    InputStockStatus=models.CharField(max_length=30)
    CreatedOn=models.DateField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class MsSerialNumber(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    SerialNumber=models.CharField(max_length=300)
    
class TxReceivingSAM(models.Model):
    ReceivingSAMID=models.CharField(max_length=30)
    ReceivingPersoQty=models.CharField(max_length=30)
    WarehouseName=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxSAM(models.Model):
    ReceivingSAMID=models.CharField(max_length=30)
    SAM_SN=models.CharField(max_length=30)
    SAM_UID=models.CharField(max_length=30)
    #SAM_PCID=models.CharField(max_length=30)
    SAMpinFile=models.FileField(upload_to=get_upload_file_name)
    SAMpinFileDownload=models.CharField(max_length=30)
    SAMPIN=models.CharField(max_length=150)
    WarehouseName=models.CharField(max_length=30)
    Product_SN=models.CharField(max_length=30)
    Product_Model=models.CharField(max_length=30)
    Product_Name=models.CharField(max_length=30)
    CustomerID=models.CharField(max_length=30)
    DistributorID=models.CharField(max_length=30)
    EndCustomerName=models.CharField(max_length=30)
    DistributorName=models.CharField(max_length=30)
    AndriodID=models.CharField(max_length=30)
    DataExportQty=models.CharField(max_length=30)
    DataExportStatus=models.CharField(max_length=30)
    Production_Date=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxSAM_TXStock(models.Model):
    RefNumber=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    StockQtyIN=models.CharField(max_length=30)
    StockQtyOut=models.CharField(max_length=30)
    StockQtyBalance=models.CharField(max_length=30)
    StockSN=models.CharField(max_length=30)

class TxSAM_TxStockSN(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductType=models.CharField(max_length=30)
    SN=models.CharField(max_length=30)
    SNStatus=models.CharField(max_length=30)
    
class TxInputStock(models.Model):
    InputStockID=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    InputStockQty=models.CharField(max_length=30)
    StockSN=models.CharField(max_length=30)
    InputStockStatus=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxInput_TxStock(models.Model):
    RefNumber=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    InputStockStatus=models.CharField(max_length=30)
    StockQtyIN=models.CharField(max_length=30)
    StockQtyOut=models.CharField(max_length=30)
    StockQtyBalance=models.CharField(max_length=30)
    StockSN=models.CharField(max_length=30)

class TxInput_TxStockSN(models.Model):
    ProductID=models.CharField(max_length=30)
    RefNumber=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductType=models.CharField(max_length=30)
    SN=models.CharField(max_length=30)
    SNStatus=models.CharField(max_length=30)

class TxAdjustmentStock_Hdr(models.Model):
    ProductID=models.CharField(max_length=30)
    AdjustmentStockID=models.CharField(max_length=30)
    IOStockStatus=models.CharField(max_length=30)
    IOStockBalance=models.CharField(max_length=30)
    Remark=models.CharField(max_length=300)
    RefTransaction=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=60)
    WarehouseID=models.CharField(max_length=30)
    AdjustmentType=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)


class TxAdjustmentStock_Dtl(models.Model):
    ProductID=models.CharField(max_length=30)
    AdjustmentStockID=models.CharField(max_length=30)
    AdjustmentType=models.CharField(max_length=30)
    InputStockQty=models.CharField(max_length=30)
    OutputStockQty=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    InputOutput=models.CharField(max_length=30)
    SerialStatus=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=60)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxAdjustmentStock_TxStockSN(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductType=models.CharField(max_length=30)
    SerialNumber=models.CharField(max_length=30)
    SNStatus=models.CharField(max_length=30)
    AdjustmentStockID=models.CharField(max_length=30)

class TxAdjustmentStock_TxStock(models.Model):
    RefNumber=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    StockQtyIN=models.CharField(max_length=30)
    StockQtyOut=models.CharField(max_length=30)
    StockQtyBalance=models.CharField(max_length=30)
    IOStockStatus=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=60)
    
class TxHandOverMaterialHdr(models.Model):
    ProductionID=models.CharField(max_length=30)
    RefNumber=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductModel=models.CharField(max_length=30)
    Product_SN=models.CharField(max_length=30)
    SAM_SN=models.CharField(max_length=30)
    AndriodID=models.CharField(max_length=30)
    StartProductionDate=models.CharField(max_length=30)
    EndProductionDate=models.CharField(max_length=30)
    ProductionStatus=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxHandOverMaterialDtl(models.Model):
    ProductionID=models.CharField(max_length=30)
    RefNumber=models.CharField(max_length=30)
    MaterialCode=models.CharField(max_length=100)
    MaterialName=models.CharField(max_length=100)
    MaterialQty=models.CharField(max_length=100)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)
    
class TxWarehouseForProduction(models.Model):
    ProdWarehouseNo=models.CharField(max_length=30)
    InputWarehouseID=models.CharField(max_length=30)
    InputWarehouseName=models.CharField(max_length=30)
    OutputWarehouseID=models.CharField(max_length=30)
    OutputWarehouseName=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxSetSAMCard(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductType=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ProductModel=models.CharField(max_length=30)
    ProductStatus=models.CharField(max_length=30)
    


class TxProductionFG_TxStock(models.Model):
    RefNumber=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    StockQtyIN=models.CharField(max_length=30)
    StockQtyOut=models.CharField(max_length=30)
    StockQtyBalance=models.CharField(max_length=30)

class TxProductionMaterial_TxStock(models.Model):
    RefNumber=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    StockQtyIN=models.CharField(max_length=30)
    StockQtyOut=models.CharField(max_length=30)
    StockQtyBalance=models.CharField(max_length=30)

class TxProductionFG_TxStockSN(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    SN=models.CharField(max_length=30)
    SNStatus=models.CharField(max_length=30)

class TxProductionMaterial_TxStockSN(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    SN=models.CharField(max_length=30)
    SNStatus=models.CharField(max_length=30)

class TxProduction_TxSAM(models.Model):
    ReceivingSAMID=models.CharField(max_length=30)
    SAM_SN=models.CharField(max_length=30)
    SAM_UID=models.CharField(max_length=30)
    SAM_PCID=models.CharField(max_length=30)
    Product_SN=models.CharField(max_length=30)
    Product_Model=models.CharField(max_length=30)
    Product_Name=models.CharField(max_length=30)
    Production_Date=models.CharField(max_length=30)
    EndCustomerName=models.CharField(max_length=30)
    DistributorName=models.CharField(max_length=30)

class TxShipmentToCustomer_Hdr(models.Model):
    ShipToCustomerID=models.CharField(max_length=30)
    RefTransaction=models.CharField(max_length=30)
    DistributorID=models.CharField(max_length=30)
    CustomerID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    DistributorName=models.CharField(max_length=30)
    CustomerName=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    ShipDate=models.DateField(auto_now_add=True)
    ShipQty=models.CharField(max_length=30)
    Status=models.CharField(max_length=30)
    Remarks=models.CharField(max_length=300)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class TxShipmentToCustomer_Dtl(models.Model):
    ShipToCustomerID=models.CharField(max_length=30)
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    Product_SN=models.CharField(max_length=30)
    CreatedOn=models.DateTimeField(auto_now_add=True)
    CreatedBy=models.CharField(max_length=30)
    LastUpdateOn=models.DateTimeField(auto_now_add=True)
    LastUpdateBy=models.CharField(max_length=30)

class Txtransfer_location(models.Model):		
    RefNumber=models.CharField(max_length=30)		
    WarehouseFrom=models.CharField(max_length=30)		
    ProductID=models.CharField(max_length=30)		
    ProductName=models.CharField(max_length=30)		
    ProductModel=models.CharField(max_length=30)		
    ProductType=models.CharField(max_length=30)		
    ExistingQuantity=models.CharField(max_length=30)		
    WarehouseTo=models.CharField(max_length=30)		
    TransferQuantity=models.CharField(max_length=30)		
    CreatedOn=models.DateTimeField(auto_now_add=True)		
    CreatedBy=models.CharField(max_length=30)		
    LastUpdateOn=models.DateTimeField(auto_now_add=True)		
    LastUpdateBy=models.CharField(max_length=30)		
    

class StockCard_result(models.Model):
    ProductID=models.CharField(max_length=30)
    ProductName=models.CharField(max_length=30)
    WarehouseID=models.CharField(max_length=30)
    Balance=models.CharField(max_length=30)
    StockSN=models.CharField(max_length=30)