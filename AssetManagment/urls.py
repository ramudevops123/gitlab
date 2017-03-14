from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'AssetManagment.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'AssetManagment.views.login'),
    url(r'^accounts/login/$', 'AssetManagment.views.login'),
    url(r'^accounts/auth/$', 'AssetManagment.views.auth_view'),
    url(r'^accounts/invalid/$', 'AssetManagment.views.invalid_login'),
    url(r'^accounts/inactive/$', 'AssetManagment.views.inactive_user'),
    url(r'^accounts/logout/$', 'AssetManagment.views.logout'),
    url(r'^HomePage/ForgotPassword/$', 'AssetManagment.views.Forgot_Password'),
    url(r'^accounts/changepassword/$', 'AssetManagment.views.Change_Password'),
#---------------Product---------------------------------------------------------
    url(r'^accounts/Product/$','AssetManagment.views.Product_View'),
    url(r'^accounts/ViewProduct/$', 'AssetManagment.views.View_Product'),
    url(r'^accounts/EditProduct/(\d+)/$', 'AssetManagment.views.Edit_Product'),
    url(r'^accounts/EditProduct/$', 'AssetManagment.views.Update_Product'),
    url(r'^accounts/Producttype/$', 'AssetManagment.views.ProductType_view'),
#---------------user---------------------------------------------------------
    url(r'^accounts/createuser/$', 'AssetManagment.views.createuser_View'),
    url(r'^accounts/ViewUser/$', 'AssetManagment.views.View_User'),
    url(r'^accounts/Edituser/(\d+)/$', 'AssetManagment.views.Edit_User'),
    url(r'^accounts/EditUser/$', 'AssetManagment.views.Update_User'),
    url(r'^accounts/Privileges/$', 'AssetManagment.views.Privilege_view'),
#---------------ThirdParty---------------------------------------------------------
    url(r'^accounts/ThirdParty/$','AssetManagment.views.ThirdParty_View'),
    url(r'^accounts/ViewThirdParty/$', 'AssetManagment.views.View_ThirdPartyUser'),
    url(r'^accounts/EditThirdParty/(\d+)/$', 'AssetManagment.views.Edit_ThirdPartyUser'),
    url(r'^accounts/EditThirdParty/$', 'AssetManagment.views.Update_ThirdPartyUser'),
	url(r'^ThirdPartyIDtest/$', 'AssetManagment.views.ThirdParty_Error_label'),
#---------------WareHouse---------------------------------------------------------
    url(r'^accounts/WareHouse/$','AssetManagment.views.WareHouse_View'),
    url(r'^accounts/ViewwareHouse/$', 'AssetManagment.views.View_wareHouse'),
    url(r'^accounts/EditwareHouse/(\d+)/$', 'AssetManagment.views.Edit_wareHouse'),
    url(r'^accounts/EditwareHouse/$', 'AssetManagment.views.Update_wareHouse'),
#---------------Bill of Material---------------------------------------------------------
    url(r'^accounts/ADDBOM/$','AssetManagment.views.ADDBOM_View'),
    url(r'^test/$', 'AssetManagment.views.Product_Details'),
    url(r'^materialtest/$', 'AssetManagment.views.Material_Details'),
    url(r'^HomePage/BOMaterial/$', 'AssetManagment.views.Add_BOM_Details'),
    url(r'^accounts/BOMaterial/(\d+)/$', 'AssetManagment.views.Update_BOM'),
    url(r'^accounts/EditBOM/(\d+)/$', 'AssetManagment.views.EditBOM_View'),
    url(r'^accounts/EditBOM/$', 'AssetManagment.views.UpdateBOM_View'),
    url(r'^MaterialInsert/$', 'AssetManagment.views.MaterialInsert_Details'),
    url(r'^MaterialUpdate/$', 'AssetManagment.views.MaterialUpdate_Details'),     
    url(r'^accounts/ViewBOM/$','AssetManagment.views.View_BOM'),
    url(r'^accounts/EditBOMaterial/(\d+)/$','AssetManagment.views.Edit_BOMaterialView'),
    url(r'^accounts/EditBOMaterial/$','AssetManagment.views.Update_BOMaterialView'),

#---------------Purchase Order---------------------------------------------------------
    url(r'^accounts/ADDPurchaseOrder/$', 'AssetManagment.views.AddPurchaseOrder_View'),
    url(r'^accounts/ADDMaterial/(\d+)/$', 'AssetManagment.views.AddMaterial_OR_Product_View'),
    url(r'^accounts/ADDMaterial/$', 'AssetManagment.views.TestAddMaterial'),
    url(r'^accounts/PurchaseOrder/$', 'AssetManagment.views.PO_view'),
    url(r'^PNameTest/$', 'AssetManagment.views.PO_Product_Details'),
    url(r'^prdctNametest/$', 'AssetManagment.views.Add_PO_Product_Details'),
    url(r'^accounts/ViewPurchaseOrder/$', 'AssetManagment.views.View_PurchaseOrder'),
    url(r'^accounts/EditPurchaseOrder/(\d+)/$', 'AssetManagment.views.EditPurchaseOrder_View'),
    url(r'^accounts/EditPurchaseOrder/$', 'AssetManagment.views.UpdatePurchaseOrder_View'),
    url(r'^poNumbertest/$', 'AssetManagment.views.PO_NO_Error_Label'),
    url(r'^accounts/EditMaterial/(?P<PoNo>[^/]+)/(?P<uid>[^/]+)/$', 'AssetManagment.views.EditMaterial_View'),
    url(r'^accounts/EditMaterial/$', 'AssetManagment.views.UpdateMaterial_View'),
                       
#---------------Shipment From Manufacture---------------------------------------------------------
                       
    url(r'^accounts/ADDSFM/$','AssetManagment.views.ADD_ShipmentFManufacture'),
    url(r'^sfmtest/$', 'AssetManagment.views.ShipmentFManufacture_Details'),
    url(r'^accounts/ViewSFM/$', 'AssetManagment.views.View_SFM'),
    url(r'^accounts/EditSFM/(\d+)/$', 'AssetManagment.views.Edit_SFM'),
    url(r'^accounts/EditSFM/$', 'AssetManagment.views.Update_SFM'),
    url(r'^PIDtest/$', 'AssetManagment.views.SFM_Product_Details'),
    url(r'^SQuantity/$', 'AssetManagment.views.SFM_Quantity_details'),
    url(r'^ProductEDate/$', 'AssetManagment.views.SFM_ProductEDate_details'),
                       
#--------------Custom Clearance---------------------------------------------------------
    url(r'^accounts/ADDCustomClearance/$','AssetManagment.views.ADD_CustomClearance'),
    url(r'^CCTest/$', 'AssetManagment.views.CustomClearance_Details'),
    url(r'^accounts/ViewCustomClearance/$', 'AssetManagment.views.View_CustomClearance'),
    url(r'^accounts/EditCustomClearance/(\d+)/$', 'AssetManagment.views.Edit_CustomClearance'),
    url(r'^accounts/EditCustomClearance/$', 'AssetManagment.views.Update_CustomClearance'),
    url(r'^GetPNameTest/$', 'AssetManagment.views.ProductName_Details'),
    url(r'^GetProductIDTest/$', 'AssetManagment.views.ProductID_Details'),
    url(r'^FillShipData/$', 'AssetManagment.views.ShipProductID_Details'),
    url(r'^FillShipNoDetails/$', 'AssetManagment.views.ShipNo_Details'),
    url(r'^customclearance/$', 'AssetManagment.views.customcleranceErrorLabel'),
    url(r'^customclearancesubmit/$', 'AssetManagment.views.customclerancemessageLabel'),

#------------------------Receiving Finish Goods/Materials-------------------------------------


    url(r'^accounts/ADDReceiving/$','AssetManagment.views.ADD_Receiving'),
    url(r'^ReceivingTest/$', 'AssetManagment.views.Receiving_Details'),
    url(r'^accounts/ViewReceiving/$', 'AssetManagment.views.View_Receiving'),
    url(r'^accounts/EditReceiving/(\d+)/$', 'AssetManagment.views.Edit_Receiving'),
    url(r'^accounts/EditReceiving/$', 'AssetManagment.views.Update_Receiving'),
    url(r'^accounts/EditSN/(?P<SN>[^/]+)/$', 'AssetManagment.views.EditSerialNumber_View'),
    url(r'^SNUpdate/$', 'AssetManagment.views.SNUpdate_Details'),
    url(r'^accounts/DeleteSN/(?P<SN>[^/]+)/$', 'AssetManagment.views.DeleteSerialNumber_View'),
    url(r'^SNDelete/$', 'AssetManagment.views.SNDelete_Details'),
    url(r'^GetALLSNTest/$', 'AssetManagment.views.SNDeleteCheck_Details'),
    url(r'^SNValidation/$', 'AssetManagment.views.SNValidation_Details'),
    url(r'^QuantityCheck/$', 'AssetManagment.views.ReceiveQntyCheck'),
    url(r'^StockInsert/$', 'AssetManagment.views.StockInsert_Details'),
    url(r'^StockInsertSN/$', 'AssetManagment.views.StockInsert_Details'),
    url(r'^SerialNumberCount/$', 'AssetManagment.views.SerialNumberCount_Details'),
    

#---------------Test--------------------------------------------------------------------------------
    url(r'^Productidtest/$', 'AssetManagment.views.ProductID_Details'),
#-------------------------------------StockCard------------------------------------------------------------
	#url(r'^accounts/ADDReceiving/$','AssetManagment.views.ADD_Stock_View'),
        url(r'^accounts/StockCardSummary/$', 'AssetManagment.views.Stock_summary_Card'),
	url(r'^accounts/ViewStockCardSummary/(?P<ProductID>[^/]+)/(?P<Warehouse>[^/]+)/$', 'AssetManagment.views.View_Stock_summary_Card'),
        url(r'^accounts/ViewStockCardSummaryforSearch/(?P<ProductID>[^/]+)/(?P<Warehouse>[^/]+)/$', 'AssetManagment.views.View_Stock_summary_Card_For_Search'),
        url(r'^accounts/ViewStockCardSummaryforSearchWarehouse/(?P<ProductID>[^/]+)/(?P<Warehouse>[^/]+)/$', 'AssetManagment.views.View_Stock_summary_Card_For_SearchWarehouse'),
	#url(r'^accounts/ViewStockCardSummary/(\d+)/$', 'AssetManagment.views.View_Stock_summary_Card'),
	url(r'^accounts/ViewSerialNO/(\d+)/$', 'AssetManagment.views.Serial_No_Details'),
	#url(r'^accounts/ViewStockCardSummary/$', 'AssetManagment.AddStock.View_Stock_summary_Card'),
	url(r'^accounts/CardInquiry/$','AssetManagment.views.Card_Inquiry_View'),
	url(r'^accounts/CardInquirywithwarehouse/$','AssetManagment.views.Card_Inquiry_Using_Warehouseid'),
	url(r'^ProductIdSort/$', 'AssetManagment.views.productId_sorting'),
	url(r'^warehouseIdSort/$', 'AssetManagment.views.warehouseId_sorting'),
    url(r'^warehousecarderrorlabel/$', 'AssetManagment.views.Card_Inquiry_Error_label_With_warehouse'),
    url(r'^SNInsert/$', 'AssetManagment.views.SerialNumber_Details'),
    url(r'^carderrorlabel/$', 'AssetManagment.views.Card_Inquiry_Error_label'),
	url(r'^accounts/Viewresult/$', 'AssetManagment.views.Stock_Result'),
#----------------------------------ReceivingSamCard----------------------------------------------------
    url(r'^accounts/ReceivingSamCard/$', 'AssetManagment.views.Add_ReceivingsamCard'),
    url(r'^accounts/ViewReceivingSamCard/$', 'AssetManagment.views.View_ReceivingsamCard'),
    url(r'^accounts/EditSAMCard/(\d+)/$', 'AssetManagment.views.Edit_ReceivingsamCard'),
    url(r'^accounts/EditSAMDetails/(\d+)/$', 'AssetManagment.views.GetSAM_Details'),
    url(r'^accounts/EditSAMCard/$', 'AssetManagment.views.Update_ReceivingsamCard'),
    url(r'^accounts/EditSAMDetails/$', 'AssetManagment.views.Update_SAMDetails'),
    url(r'^SAMFileClick/$', 'AssetManagment.views.SAMFileClick_Details'),
    url(r'^GetSAMDuplicate/$', 'AssetManagment.views.GetSAMDuplicate_Details'),
    
    url(r'^SAMInsert/$', 'AssetManagment.views.SAMInsert_Details'),
    url(r'^SAMInsertUpdate/$', 'AssetManagment.views.SAMInsertUpdate_Details'),
    #url(r'^SAMDetails/$', 'AssetManagment.samviews.GetSAM_Details'),


#------------------------------------InputStock--------------------------------------------------------------

    url(r'^accounts/InputStock/$', 'AssetManagment.views.AddInputStock_View'),
    url(r'^accounts/ViewInputStock/$', 'AssetManagment.views.View_InputStock'),
    url(r'^accounts/EditInputStock/(\d+)/$', 'AssetManagment.views.Edit_InputStock'),
    url(r'^accounts/EditInputStock/$', 'AssetManagment.views.Update_InputStock'),                       
    url(r'^accounts/EditSerialNumber/(\d+)/$', 'AssetManagment.views.Edit_SerialNumber'),
    url(r'^accounts/EditSerialNumber/$', 'AssetManagment.views.Update_SerialNumber'),
    url(r'^accounts/DeleteSerialNumber/(?P<uid>[^/]+)/(?P<ISID>[^/]+)/(?P<ProductName>[^/]+)/$', 'AssetManagment.views.Delete_SerialNumber'),                           
    url(r'^GetPNameTest/$', 'AssetManagment.views.ProductName_Details'),
    url(r'^SNInputStockInsert/$', 'AssetManagment.views.SNInputStock_Details'),
    url(r'^GetALLInputSNTest/$', 'AssetManagment.views.SNInputDeleteCheck_Details'),
    url(r'^accounts/EditInputSN/(?P<SN>[^/]+)/$', 'AssetManagment.views.EditInputSN_View'),
    url(r'^InputSNUpdate/$', 'AssetManagment.views.InputSNUpdate_Details'),
    url(r'^accounts/DeleteInputSN/(?P<SN>[^/]+)/$', 'AssetManagment.views.DeleteInputSN_View'),
    url(r'^InputSNDelete/$', 'AssetManagment.views.InputSNDelete_Details'),
    #url(r'^SNcountValidation/$', 'AssetManagment.views.SNInputCount_Details'),                  
    #url(r'^accounts/CDReport/$', 'AssetManagment.views.View_CDReport'),
	
                       

#-----------------------------------------------HandOverMaterial--------------------------------------------------------------

    url(r'^accounts/ADDHOM/$','AssetManagment.views.ADDHOM_View'),
    url(r'^accounts/ViewHOM/$','AssetManagment.views.View_HOM'),
    url(r'^accounts/EditHOM/(\d+)/$', 'AssetManagment.views.EditHOM_View'),
    url(r'^accounts/EditHOM/$', 'AssetManagment.views.UpdateHOM_View'),
    url(r'^GetMaterialList/$', 'AssetManagment.views.MaterialList_Details'),
    url(r'^SAMSNTest/$', 'AssetManagment.views.SAMSNTest_Details'),
    url(r'^ProductSNTest/$', 'AssetManagment.views.ProductSNTest_Details'),
    url(r'^Androididvalidation/$', 'AssetManagment.views.AndroidValidation_Details'),
    url(r'^SAMHOMFileClick/$', 'AssetManagment.views.SAMHOMFileClick_Details'),
    url(r'^MaterialValidation/$', 'AssetManagment.views.Material_Details_Validation'),
                       
        
#-----------------------------------------------SetWareHouse Production ----------------------------------------

    url(r'^accounts/SetWareHouse/$','AssetManagment.views.SetWareHouse_View'),
    url(r'^WarehouseNametest/$', 'AssetManagment.views.WarehouseName_Details'),
    url(r'^SaveWareHouseClick/$', 'AssetManagment.views.SaveWareHouseClick_Details'),
    url(r'^UpdateWareHouseClick/$', 'AssetManagment.views.UpdateWareHouseClick_Details'),
                       
    

#---------------------------------------------SetSAMCard---------------------------------------------------------------------------------

    url(r'^SetSAMtest/$', 'AssetManagment.views.ProductSAM_Details'),
    url(r'^accounts/SetSamCard/$','AssetManagment.views.SetSamCard_View'),
    url(r'^SaveProductClick/$', 'AssetManagment.views.SaveProductClick_Details'),
    url(r'^UpdateProductClick/$', 'AssetManagment.views.UpdateProductClick_Details'),
                       
#------------------------------------------------FinishGood Receiving----------------------------------------------------------------------

    url(r'^accounts/ViewFGReceiving/$','AssetManagment.views.View_FGReceiving'),
                       
#------------------------------------------------Adjustment Stock ---------------------------------------------------------------------
    url(r'^StockadjustmentserialInsert/$', 'AssetManagment.views.ADjustment_serial_Insertation'),
    #url(r'^StockadjustmentstocklistInsert/$', 'AssetManagment.views.Adjustment_Add_to_Stock_List'),
    #url(r'^StockadjustmentstocklistserialcountInsert/$', 'AssetManagment.views.Adjustment_Add_to_Stock_List_SerialCount'),
    url(r'^accounts/AdjustmentStock/$', 'AssetManagment.views.AdjustmentStock'),
    #url(r'^Stockbalance/$', 'AssetManagment.views.StockbalanceLabel'),
    url(r'^Productnamesorting/$', 'AssetManagment.views.Adjustment_Product_Details'),
    url(r'^accounts/ViewAdjustmentStockList/$', 'AssetManagment.views.view_Adjustment_StockList'),
    url(r'^accounts/EditAdjustmentStock/(\d+)/$', 'AssetManagment.views.Edit_Adjustment_Stock'),
    url(r'^accounts/EditAdjustmentStock/$', 'AssetManagment.views.Update_Adjustment'),
    url(r'^accounts/EditAdjustmentSerialNumber/(\d+)/$', 'AssetManagment.views.Edit_Adjustment_SerialNumber'),
    url(r'^AdjustmentSNUpdate/$', 'AssetManagment.views.Update_Adjustment_SerialNumber'),
    url(r'^accounts/DeleteAdjustmentSerialNumber/(?P<uid>[^/]+)/$', 'AssetManagment.views.Delete_Adjustment_SN_View'),
    url(r'^AdjustmentSNDelete/$', 'AssetManagment.views.Delete_Adjustment_SerialNumber'),
    #url(r'^accounts/EditAdjustmentStockList/(\d+)/$', 'AssetManagment.views.Edit_Adjustment_StockList'),
    #url(r'^UpdateAdjustmentDtl/$', 'AssetManagment.views.Update_Adjustment_StockList'),
    #url(r'^accounts/DeleteAdjustmentStockList/(\d+)/$', 'AssetManagment.views.Delete_Adjustment_StockList_View'),
    #url(r'^UpdateStockList/$', 'AssetManagment.views.Delete_Adjustment_StockList'),
    url(r'^SNStatusValidation/$', 'AssetManagment.views.SNStatus_Validation_Lable'),
    url(r'^GetAdjustmentSNTest/$', 'AssetManagment.views.Adjustment_SNDeleteCheck_Details'),
	

#--------------------------------------------------ShipmentToCustomer-----------------------------------------------------------------------

    url(r'^accounts/ShipmentTOCustomer/$','AssetManagment.views.Add_ShipmentToCustomer'),
    url(r'^GetDistributorDetails/$', 'AssetManagment.views.GetDistributor_Details'),
    url(r'^GetCustomerDetails/$', 'AssetManagment.views.GetCustomer_Details'),
    url(r'^DeviceSNtest/$', 'AssetManagment.views.GetDeviceSN_Details'),
    url(r'^DeviceSNListView/$', 'AssetManagment.views.GetDeviceSNList_Details'),
    url(r'^accounts/ViewShipmentToCustomer/$', 'AssetManagment.views.View_ShipmentToCustomer'),
    url(r'^accounts/EditShipmentToCustomer/(\d+)/$', 'AssetManagment.views.Edit_ShipmentToCustomer'),
    url(r'^accounts/EditShipmentToCustomer/$', 'AssetManagment.views.Update_ShipmentToCustomer'),
    url(r'^SaveStockInsert/$', 'AssetManagment.views.SaveStockInsert_Details'),
    url(r'^DetailCount/$', 'AssetManagment.views.DetailCount_Details'),

#------------------------------------------------Reports--------------------------------------------------------------------------------------------

    #url(r'^accounts/CDReport/$', 'AssetManagment.views.View_CDReport'),
    url(r'^accounts/CustomerDataReport/$', 'AssetManagment.views.CustomerReport_DataView'),
    url(r'^CustomerExportID/$', 'AssetManagment.views.CustomerReport_Details'),
    url(r'^accounts/DistributorDataReport/$', 'AssetManagment.views.DistributorReport_DataView'),
    url(r'^DistributorExportID/$', 'AssetManagment.views.DistributorReport_Details'),
    url(r'^accounts/DeviceDataReport/$', 'AssetManagment.views.DeviceReport_DataView'),
    url(r'^DeviceExportID/$', 'AssetManagment.views.DeviceReport_Details'),
    
    url(r'^accounts/ProductionDataReport/$', 'AssetManagment.views.ProductionReport_DataView'),

#-------------------------------------------Transfer Stock Location--------------------------------------
    url(r'^accounts/TransferStockLocation/$', 'AssetManagment.views.Transfer_Stock_Location_View'),
    url(r'^TransferlocationProductidsorting/$', 'AssetManagment.views.Transfer_Stock_ProductID_Sorting'),
    url(r'^ExistingQtyValidation/$', 'AssetManagment.views.Transfer_Stock_Existing_Stock_Validation'),
    url(r'^TransferlocationSerialNumbers/$', 'AssetManagment.views.Transfer_Stock_SerialNumber_Details'),
    url(r'^CheckedSerialNumbers/$', 'AssetManagment.views.Checked_SerialNumber_Details'),
    url(r'^accounts/ViewTransferLocation/$', 'AssetManagment.views.Transfer_StocK_Location_List'),
    url(r'^TransferlocationWarehouseValidation/$', 'AssetManagment.views.Transfer_Location_Warehouse_Validation'),

#--------------------------------------Search------------------------------------------------------
    url(r'^accounts/SAMDeviceID/$', 'AssetManagment.views.SAMDeviceID'),
    
)
