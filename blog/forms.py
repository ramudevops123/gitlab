from django import forms
from models import TxSAM

class TxSAMForm(forms.ModelForm):
	
	class Meta:
		model=TxSAM
		fields= ('ReceivingSAMID','SAM_SN','SAM_UID','SAMpinFile','SAMpinFileDownload','WarehouseName','DataExportQty','DataExportStatus')
		

