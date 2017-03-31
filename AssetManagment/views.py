from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User,check_password
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from blog.models import Users,UserPrivileges,MsProduct,ProductType,ThirdParty,WareHouse,MsBOMHeader,MsBOMDetail,TxPurchaseOrderHdr,TxPurchaseOrderDtl,ShipmentFromManufacture,CustomClearance,MsSerialNumber,TxReceivingFG_Material,txStock,TxStockSN,TxSAM,TxReceivingSAM,TxInput_TxStockSN,TxInput_TxStock,TxInputStock,TxHandOverMaterialHdr,TxHandOverMaterialDtl,TxAdjustmentStock_Hdr,TxAdjustmentStock_Dtl,TxAdjustmentStock_TxStockSN,TxAdjustmentStock_TxStock,TxShipmentToCustomer_Hdr,MsBOMHeader,TxWarehouseForProduction,TxSetSAMCard,TxShipmentToCustomer_Dtl,Txtransfer_location,StockCard_result
from blog.forms import TxSAMForm
import os
import logging
import datetime
import random
import time
from random import randint
import string
from datetime import datetime,timedelta,time,date
logger=logging.getLogger(__name__)
from django.db import connection
from django.core import mail
import json
from django.core import serializers
from django.core.files import File
from time import time
from django.template.loader import render_to_string

os.environ['TZ'] = 'Asia/Calcutta'

def login(request):
    BootStrap_Admin()
    csrftoken={}
    csrftoken.update(csrf(request))
    return render_to_response('login.html',csrftoken)

def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def get_role(email):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT role from blog_users where email =('%s')" % (email))
        data =  cursor.fetchone()[0]
        logger.info(data)
        return data
    except:
        return None

def get_status(email):
    cursor=connection.cursor()
    cursor.execute("SELECT Status from blog_users where email =('%s')" % (email))
    data =  cursor.fetchone()[0]
    logger.info(data)
    return data 
    
def get_username(userid):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Email from blog_users where id =('%s')" % (userid))
        data =  cursor.fetchone()[0]
        logger.info(data)
        return data
    except User.DoesNotExist:
        return None
	
def auth_view(request):
    email=request.POST.get('email', '')
    password=request.POST.get('password', '')
    username = get_user(email)
    logger.info(username)
    user = auth.authenticate(username=username, password=password)
    if user is not None:
	userstatus=get_status(email)
	if userstatus == 'InActive':
            return HttpResponseRedirect('/accounts/inactive/')
	auth.login(request,user)
	userrole=get_role(email)
	if userrole == 'Admin':
            return render(request,'DashBoard.html',{'full_name':request.user.first_name,'UserRole':userrole})
            #return HttpResponseRedirect('/accounts/DashBoard/')
        elif userrole == 'Logistic staff/user':
            return render(request,'DashBoard.html',{'full_name':request.user.first_name,'UserRole':userrole})
        elif userrole == 'Production':
            return render(request,'DashBoard.html',{'full_name':request.user.first_name,'UserRole':userrole})
        elif userrole == 'Local Manufacture':
            return render(request,'DashBoard.html',{'full_name':request.user.first_name,'UserRole':userrole})
           # cursor = connection.cursor()
            #cursor.execute("SELECT Permissions from blog_users where Email =('%s')" % (email))
            #data =  cursor.fetchone()[0]
            #logger.info(data)
            #a=data.replace("('","")
           # m=a.replace("','"," ")
          #  Permissions=m.replace("')","")
           # logger.info(Permissions)
           # return render(request,'Product.html',{'full_name':request.user.first_name,'UserRole':userrole,'obj':Permissions,'producttype':ProductType.objects.all() })
        #if userrole == 'Logistic staff/user':
           # return render(request,'Product.html',{'full_name':request.user.first_name,'UserRole':userrole,'obj':UserPrivileges.objects.filter(User='LogisticStaff').filter(my_field=1)})
        
    else:
	return render_to_response('invalid_login.html')
    return render_to_response('login.html')
	
def inactive_user(request):
    return render_to_response('inactive_user.html')

def BootStrap_Admin():
                if User.objects.count() == 0 and Users.objects.count() == 0:
                    psswd=make_password("admin123")
                    now=datetime.now()
                    createddate=str(now)[:10]
                    modifieddate=str(now)[:10]
                    is_superuser='1'
                    is_staff='1'		
                    is_active='1'
                    role='Admin'
                    status='Active'
                    cursor = connection.cursor()
                    cursor.execute("""INSERT INTO auth_user (password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(psswd,modifieddate,is_superuser,"Admin","Admin","Admin","admin@lst.com",is_staff,is_active,createddate))
                    cursor.execute("""INSERT INTO blog_users (FirstName,LastName,Email,Role,Status,CreatedDate,ModifiedDate) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s)""",("Admin","Admin","admin@lst.com",role,status,createddate,modifieddate))
                else:
                    return render_to_response('login.html')
def invalid_login(request):
    return render_to_response('invalid_login.html')


#---------------------------------------------User Management-----------------------------------------------------

def createuser_View(request):
        #import_csv("C:\\Users\\admin\\Desktop\\import.csv")
	cursor = connection.cursor()
	firstname=request.POST.get('firstname')
	lastname=request.POST.get('lastname')
	email=request.POST.get('email')
	password='pbkdf2_sha256$12000$zeQk9D3wBGlA$XOsUm8nm/UIrThkpvW/krtN3qZoWwQZijsMQxXY4Yw0='
	role=request.POST.get('myrole')	
	status=request.POST.get('status')
	now=datetime.now()
        createddate=str(now)[:10]
        modifieddate=str(now)[:10]
        is_superuser='1'
        is_staff='1'
        is_active='1'
        PO=request.POST.getlist('user')
	logger.info(PO)
	if User.objects.filter(email=email).count() > 0: 
	    return render(request,'createuser.html',{'full_name':request.user.first_name,'Error':'User Already Exists'})
	#elif User.objects.filter(username=firstname).count() > 0:
		#return render(request,'createuser.html',{'deptlist':Add_New_Group.objects.all(),'full_name':request.user.first_name,'Error':'UserName Already Exists'})
	
	elif firstname != None:
	    cursor.execute("""INSERT INTO blog_users(FirstName,LastName,Email,Role,Permissions,Status,CreatedDate,ModifiedDate) 
	    VALUES (%s,%s,%s,%s,%r,%s,%s,%s)""",(firstname,lastname,email,role,tuple(PO),status,createddate,modifieddate))
	    cursor.execute("""INSERT INTO auth_user (password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) 
	    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(password,modifieddate,is_superuser,email,firstname ,lastname,email,is_staff,is_active,createddate))
	    from_email = settings.EMAIL_HOST_USER
	    to_list=[email]
	    subject='User created successfully'
	    messages =  """
-- Please Do Not Reply --
	Hello,
		
	    Welcome to Logistic Mointoring. Your account has been successfully created.
		Please find below login details:
		Login Url : http://192.168.7.120:8080
                Email: """ + email + """
		Password : Password123!?
		Role : """ + role + """
		
Note:
	This is a system generated mail. Please do not reply to this email ID. 
	If you have a query or need any clarification you may:
	Email Us : itsupport@lone-soft.com 
	
Best regards,
Admin Team
Biomorf Inventory Management System  (BIMS) """

	    send_mail(subject,messages,from_email,to_list,fail_silently=True)
	    return HttpResponseRedirect('/accounts/ViewUser/')
	else:
	    return render(request,'createuser.html',{'full_name':request.user.first_name,'userPrivileges':UserPrivileges.objects.filter(User='LogisticStaff'),'ProPrivileges':UserPrivileges.objects.filter(User='Production')})
        return render(request,'createuser.html',{'full_name':request.user.first_name,'userPrivileges':UserPrivileges.objects.filter(User='LogisticStaff'),'ProPrivileges':UserPrivileges.objects.filter(User='Production')})

def View_User(request):
	if request.user.username == '':
		return HttpResponseRedirect('/accounts/login/')
	else:
		return render_to_response('Viewuser.html',{'obj':Users.objects.exclude(Role='EndUser'),
											  'full_name':request.user.first_name})
											  
def Edit_User(request,u_id):
    UserList = Users.objects.raw('SELECT * FROM blog_users where id =%s',[u_id])
    for p in UserList:
		if request.user.username == '':
			return HttpResponseRedirect('/accounts/login/')
		else:
			return render(request, 'Edituser.html',{'firstname':p.FirstName,
								'lastname':p.LastName,
								'email':p.Email,
								'role':p.Role,												
								'status':p.Status,
								'uid':u_id,
                                                                'full_name':request.user.first_name,
                                                                'userPrivileges':UserPrivileges.objects.filter(User='LogisticStaff'),
                                                                'ProPrivileges':UserPrivileges.objects.filter(User='Production')
                                                   })


												   
def Update_User(request):
	userid=request.POST.get('uid')
	logger.info(userid)
	#dept=request.POST.get('dept')
	role=request.POST.get('role')
	emptype=request.POST.get('emptype')
	status=request.POST.get('status')
	assts=request.POST.get('assts')
	repo=request.POST.get('repo')
	level=request.POST.get('level')
	username=get_username(userid)
	now=datetime.now()
        modifieddate=str(now)[:10]
	cursor = connection.cursor()
	cursor.execute("""UPDATE blog_users SET Role=%s,Status=%s,ModifiedDate=%s WHERE id=%s""",
	(role,status,modifieddate,userid))
	PO=request.POST.getlist('userlist')
	logger.info(PO)
	if len(PO) != 0:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO blog_privilege_permissions(User,Permissions) 
	    VALUES (%s,%r)""",(username,tuple(PO)))
            logger.info("test")
	return HttpResponseRedirect('/accounts/ViewUser/',{'full_name':request.user.first_name})

#------------------------------Logout,ChangePassword,ForgotPassword-----------------------------------------
		
def logout(request):
	auth.logout(request)
	return render(request,'login.html')

def Forgot_Password(request):
	cursor = connection.cursor()
	namemail=request.POST.get('namemail')
	if namemail !=None:
		if User.objects.filter(email=namemail).count() > 0:
			Token=''.join(random.choice(string.ascii_uppercase) for i in range(18))
			logger.info(Token)
			from_email = settings.EMAIL_HOST_USER
			to_list=[namemail]
			subject='Forgot Password request'
			messages = """
-- Please Do Not Reply --
Hello """ + namemail + """,

	Welcome to Logistic Mointoring. You have been requested for Forgot Password.
	

	    Email: """ + namemail + """
		Token: """ + Token + """
		Login Url: http://192.168.7.120:8080/HomePage/Token/"""+Token+"""/"""+namemail+"""/
Note:
	This is a system generated mail. Please do not reply to this email ID. 
	If you have a query or need any clarification you may:
	Email Us : itsupport@lone-soft.com 
	
Best regards,
Admin Team
IT Ticketing System (ITTS) """

                        send_mail(subject,messages,from_email,to_list,fail_silently=True)
		
                        return render(request,'login.html')
		else:
		    return render(request,'ForgotPassword.html',{'Error':'InValid Email Address'})
	else:
		return render(request,'ForgotPassword.html')

def Change_Password(request):
        userrole=get_role(request.user.email)
	opwd=request.POST.get('oldpwd')
	user = auth.authenticate(username=request.user.username, password=opwd)
	if opwd !=None:
                npwd=request.POST.get('pwd')
		cpwd=request.POST.get('cnfpwd')
		u = User.objects.get(username__exact=request.user.username)
		u.set_password(npwd)
		u.save()
		return HttpResponseRedirect('/accounts/login/',{'full_name':request.user.first_name,'UserRole':userrole})
	else:
		return render(request,'ChangePassword.html',{'full_name':request.user.first_name,'UserRole':userrole})
	    
#-------------------------------------------------Product---------------------------------------

def Product_View(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('ProID')
    PrincipalID=request.POST.get('PriID')
    PrincipalName=request.POST.get('PrincipalName')
    Producttype=request.POST.get('PType')
    ProductName=request.POST.get('PName')
    ProductModel=request.POST.get('PModel')
    ProductStatus=request.POST.get('PStatus')
    PSerialNumber=request.POST.get('PSerialNumber')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    if MsProduct.objects.filter(ProductID=ProductID):
        return render(request,'Product.html',{'full_name':request.user.first_name,'PID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'UserRole':userrole,'producttype':ProductType.objects.all(),'Error':'ProductID already exists'})
        
    if ProductID != None:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_msproduct(ProductID,PrincipalID,PrincipalName,ProductType,ProductName,ProductModel,ProductStatus,ProductSerialNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) 
	    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,PrincipalID,PrincipalName,Producttype,ProductName,ProductModel,ProductStatus,PSerialNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return HttpResponseRedirect('/accounts/ViewProduct/',{'full_name':request.user.first_name,'UserRole':userrole})
    else:
        return render(request,'Product.html',{'full_name':request.user.first_name,'PID':ThirdParty.objects.filter(ThirdPartyType='Principal').filter(ThirdPartyStatus='Active'),'UserRole':userrole,'producttype':ProductType.objects.all()})
    
def View_Product(request):
	if request.user.username == '':
		return HttpResponseRedirect('/accounts/login/')
	else:
		return render_to_response('ViewProduct.html',{'obj':MsProduct.objects.all(),'full_name':request.user.first_name})


def Edit_Product(request,u_id):
    product = MsProduct.objects.get(id=u_id)
    ProductList = MsProduct.objects.raw('SELECT * FROM blog_msproduct where id =%s',[u_id])
    for p in ProductList:
		if request.user.username == '':
			return HttpResponseRedirect('/accounts/login/')
		else:
			return render(request, 'Editproduct.html',{'ProductID':p.ProductID,
								'ProductType':p.ProductType,
								'ProductName':p.ProductName,
								'ProductModel':p.ProductModel,												
								'ProductStatus':p.ProductStatus,
                                                                'PSerialNumber':p.ProductSerialNumber,
                                                                'PrincipalID':p.PrincipalID,
                                                                'PrincipalName':p.PrincipalName,
                                                                'CreatedOn':p.CreatedOn,
                                                                'CreatedBy':p.CreatedBy,
                                                                'LastUpdateOn':p.LastUpdateOn,
                                                                'LastUpdateBy':p.LastUpdateBy,
								'uid':u_id,
                                                                'full_name':request.user.first_name
                                                   })
												   
def Update_Product(request):
	productid=request.POST.get('uid')
	logger.info(productid)
	ProductName=request.POST.get('ProductName')
	ProductStatus=request.POST.get('ProductStatus')
	now=datetime.now()
        LastUpdateOn=str(now)[:19]
        LastUpdateBy=request.user.first_name
	cursor = connection.cursor()
	cursor.execute("""UPDATE blog_msproduct SET ProductName=%s,ProductStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(ProductName,ProductStatus,LastUpdateOn,LastUpdateBy,productid))
	return HttpResponseRedirect('/accounts/ViewProduct/',{'full_name':request.user.first_name})




def PO_view(request):
    return render(request,'purchaseorder.html',{'full_name':request.user.first_name,'obj':UserPrivileges.objects.filter(User='LogisticStaff').filter(my_field=1)})

def ProductType_view(request):
    userrole=get_role(request.user.email)
    ProductType=request.POST.get('ProductType')
    if ProductType != None:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_producttype(ProductType) VALUES ('%s') """ %(ProductType))
        return render(request,'ProductType.html',{'full_name':request.user.first_name,'UserRole':userrole,'Success':'Product Type added successfully'})
    else:
        return render(request,'ProductType.html',{'full_name':request.user.first_name,'UserRole':userrole})
    
#------------------------------------Privileges ----------------------------------------------------------

def Privilege_view(request):
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(PrivilegeType) FROM blog_userprivileges WHERE User= 'LogisticStaff' and my_field=1")
    privilegeuserlist=cursor.fetchone()[0]
    if privilegeuserlist!= None:
        userlist=privilegeuserlist.split(",")
        userprvi="['"+"'"u",'".join(userlist)+"']"
        logger.info(userprvi)
    PO=request.POST.getlist('user')
    logger.info(PO)
    for u in PO:
        logger.info(u)
        cursor.execute("""UPDATE blog_userprivileges set my_field=%s where PrivilegeType=%s""",('1',u))
    return render(request,'Privileges.html',{'userPrivileges':UserPrivileges.objects.filter(User='LogisticStaff'),'ProPrivileges':UserPrivileges.objects.filter(User='Production')})
    
#----------------------------------------------------------ThirdParty---------------------------------------------------
		
def ThirdParty_View(request):
    userrole=get_role(request.user.email)
    partyId=request.POST.get('thrdID')
    logger.info(partyId)
    partyName=request.POST.get('thrdName')
    partyType=request.POST.get('thrdType')
    partyAddress=request.POST.get('thrdaddrs')
    partyCountry=request.POST.get('thrdcntry')
    partyCity=request.POST.get('thrdcity')
    partyWebsite=request.POST.get('thrdweb')
    partyEmail=request.POST.get('thrdemail')
    partyPhNo=request.POST.get('thrdphone')
    partyNotes=request.POST.get('thrdNote')
    partyStatus=request.POST.get('thrdStatus')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    if ThirdParty.objects.filter(ThirdPartyID=partyId).count()>0:
        return render(request,'ThirdPartyUser.html',{'full_name':request.user.first_name,'UserRole':userrole,'Error':'ThirdParty already exists'})
    if partyId != None:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_thirdparty(ThirdPartyID,ThirdPartyName,ThirdPartyType,ThirdPartyAddress,ThirdPartyCountry,ThirdPartyCiy,ThirdPartyWebsite,ThirdPartyEmail,ThirdPartyPhNo,ThirdPartyComments,ThirdPartyStatus,DataExportStatus,DataExportQty,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) 
	    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(partyId,partyName,partyType,partyAddress,partyCountry,partyCity,partyWebsite,partyEmail,partyPhNo,partyNotes,partyStatus,'Open','0',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return HttpResponseRedirect('/accounts/ViewThirdParty/',{'full_name':request.user.first_name,'UserRole':userrole})
    else:
        return render(request,'ThirdPartyUser.html',{'full_name':request.user.first_name,'UserRole':userrole})

def View_ThirdPartyUser(request):
	if request.user.username == '':
		return HttpResponseRedirect('/accounts/login/')
	else:
		return render_to_response('ViewThirdParty.html',{'obj':ThirdParty.objects.all(),'full_name':request.user.first_name})


def Edit_ThirdPartyUser(request,u_id):
    Tpartyuser = ThirdParty.objects.get(id=u_id)
    ThirdPartyList = ThirdParty.objects.raw('SELECT * FROM blog_thirdparty where id =%s',[u_id])
    for t in ThirdPartyList:
		if request.user.username == '':
			return HttpResponseRedirect('/accounts/login/')
		else:
			return render(request, 'EditThirdParty.html',{'ThirdPartyID':t.ThirdPartyID,
								'ThirdPartyName':t.ThirdPartyName,
								'ThirdPartyType':t.ThirdPartyType,
								'ThirdPartyAddress':t.ThirdPartyAddress,												
								'ThirdPartyCountry':t.ThirdPartyCountry,
                                                                'ThirdPartyCity':t.ThirdPartyCiy,
                                                                'ThirdPartyWebsite':t.ThirdPartyWebsite,
                                                                'ThirdPartyEmail':t.ThirdPartyEmail,
								'ThirdPartyPhNo':t.ThirdPartyPhNo,
								'ThirdPartyNotes':t.ThirdPartyComments,												
								'ThirdPartyStatus':t.ThirdPartyStatus,
                                                                'CreatedOn':t.CreatedOn,
                                                                'CreatedBy':t.CreatedBy,
                                                                'LastUpdateOn':t.LastUpdateOn,
                                                                'LastUpdateBy':t.LastUpdateBy,
								'uid':u_id,
                                                                'full_name':request.user.first_name
                                                   })
												   
def Update_ThirdPartyUser(request):
	Tpartyid=request.POST.get('uid')
	logger.info(Tpartyid)
	ThirdPartyName=request.POST.get('ThirdPartyName')
	ThirdPartyType=request.POST.get('ThirdPartyType')
	ThirdPartyAddress=request.POST.get('ThirdPartyAddress')
	ThirdPartyCountry=request.POST.get('ThirdPartyCountry')
	ThirdPartyCity=request.POST.get('ThirdPartyCity')
        ThirdPartyWebsite=request.POST.get('ThirdPartyWebsite')
        ThirdPartyEmail=request.POST.get('ThirdPartyEmail')
        ThirdPartyPhNo=request.POST.get('ThirdPartyPhNo')
        ThirdPartyNotes=request.POST.get('ThirdPartyNotes')
	ThirdPartyStatus=request.POST.get('ThirdPartyStatus')
	now=datetime.now()
        LastUpdateOn=str(now)[:19]
        LastUpdateBy=request.user.first_name
	cursor = connection.cursor()
	cursor.execute("""UPDATE blog_thirdparty SET ThirdPartyName=%s,ThirdPartyType=%s,ThirdPartyAddress=%s,ThirdPartyCountry=%s,ThirdPartyCiy=%s,
        ThirdPartyWebsite=%s,ThirdPartyEmail=%s,ThirdPartyPhNo=%s,ThirdPartyComments=%s,ThirdPartyStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(ThirdPartyName,ThirdPartyType,ThirdPartyAddress,ThirdPartyCountry,ThirdPartyCity,ThirdPartyWebsite,ThirdPartyEmail,ThirdPartyPhNo,ThirdPartyNotes,
         ThirdPartyStatus,LastUpdateOn,LastUpdateBy,Tpartyid))
	return HttpResponseRedirect('/accounts/ViewThirdParty/',{'full_name':request.user.first_name})


def ThirdParty_Error_label(request):
    ThirdPartyIDFromPage=request.GET.get('val')
    logger.info(ThirdPartyIDFromPage)
    if ThirdParty.objects.filter(ThirdPartyID=ThirdPartyIDFromPage).count()>0:
        Data="Third Party ID already exists"
    else:
        Data=None
    if ThirdPartyIDFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        ThirdPartyIDFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

#------------------------------------------WareHouse------------------------------------------------------------

def WareHouse_View(request):
    userrole=get_role(request.user.email)
    wareHouseID=request.POST.get('wareHouseID')
    wareHouseName=request.POST.get('wareHouseName')
    ThirdPartyName=request.POST.get('ThirdPartyName')
    wareHouseStatus=request.POST.get('wareHouseStatus')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    if WareHouse.objects.filter(WarehouseID=wareHouseID).count()>0:
        return render(request,'wareHouse.html',{'full_name':request.user.first_name,'UserRole':userrole,'TPName':ThirdParty.objects.all(),'Error':'WareHouse already exists'})
    if wareHouseID != None:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_warehouse(WarehouseID,WarehouseName,ThirdPartyName,WarehouseStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) 
	    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(wareHouseID,wareHouseName,ThirdPartyName,wareHouseStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return HttpResponseRedirect('/accounts/ViewwareHouse/',{'full_name':request.user.first_name,'UserRole':userrole,'Success':'WareHouse added successfully'})
    else:
        return render(request,'wareHouse.html',{'full_name':request.user.first_name,'UserRole':userrole,'TPName':ThirdParty.objects.filter(ThirdPartyStatus="Active")})
    
    
def View_wareHouse(request):
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewwareHouse.html',{'obj':WareHouse.objects.all(),'full_name':request.user.first_name})


def Edit_wareHouse(request,u_id):
    wareHouse = WareHouse.objects.get(id=u_id)
    wareHouseList = WareHouse.objects.raw('SELECT * FROM blog_warehouse where id =%s',[u_id])
    for w in wareHouseList:
		if request.user.username == '':
			return HttpResponseRedirect('/accounts/login/')
		else:
			return render(request, 'EditwareHouse.html',{'WareHouseID':w.WarehouseID,
								'wareHouseName':w.WarehouseName,
								'ThirdPartyName':w.ThirdPartyName,
								'wareHouseStatus':w.WarehouseStatus,
                                                                'CreatedOn':w.CreatedOn,
                                                                'CreatedBy':w.CreatedBy,
                                                                'LastUpdateOn':w.LastUpdateOn,
                                                                'LastUpdateBy':w.LastUpdateBy,
                                                                'TPName':ThirdParty.objects.all(),
								'uid':u_id,
                                                                'full_name':request.user.first_name
                                                   })
												   
def Update_wareHouse(request):
	warehouseid=request.POST.get('uid')
	logger.info(warehouseid)
	wareHouseName=request.POST.get('wareHouseName')
	ThirdPartyName=request.POST.get('ThirdPartyName')
	wareHouseStatus=request.POST.get('wareHouseStatus')
	now=datetime.now()
        LastUpdateOn=str(now)[:19]
        LastUpdateBy=request.user.first_name
	cursor = connection.cursor()
	cursor.execute("""UPDATE blog_warehouse SET WarehouseName=%s,ThirdPartyName=%s,WarehouseStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(wareHouseName,ThirdPartyName,wareHouseStatus,LastUpdateOn,LastUpdateBy,warehouseid))
	return HttpResponseRedirect('/accounts/ViewwareHouse/',{'full_name':request.user.first_name})

#----------------------------------------------Bill of Material-------------------------------------

def MaterialInsert_Details(request):
    ProductID=request.GET.get('ProductID')
    Materialcode=request.GET.get('Mcode')
    Materialname=request.GET.get('Mname')
    Qty=request.GET.get('Qty')
    cursor = connection.cursor()
    ValidationData=''
    getdata=''
    if ProductID =='':
        ValidationData='Please Select ProductID'
    elif Materialcode =='':
        ValidationData='Please Select Material Code'
    elif Qty =='':
        ValidationData='Please Enter Quantity'
    elif MsBOMDetail.objects.filter(ProductID=ProductID).filter(MaterialCode=Materialcode).count()>0:
        ValidationData='Data already exists please check and try again'
    else:
        cursor.execute("""INSERT INTO blog_msbomdetail(ProductID,MaterialCode,MaterialName,MaterialQty) 
        VALUES (%s,%s,%s,%s)""",(ProductID,Materialcode,Materialname,Qty))
        obj = MsBOMDetail.objects.filter(ProductID=ProductID).values_list('MaterialCode', 'MaterialName', 'MaterialQty','id')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)

def MaterialUpdate_Details(request):
    ProductID=request.GET.get('ProductID')
    Materialcode=request.GET.get('Mcode')
    Materialname=request.GET.get('Mname')
    Qty=request.GET.get('Qty')
    mid=request.GET.get('uid')
    cursor = connection.cursor()
    ValidationData=''
    if Qty =='':
        ValidationData='Please Enter Quantity'
    else:
        cursor.execute("""UPDATE blog_msbomdetail SET MaterialCode=%s,MaterialName=%s,MaterialQty=%s WHERE id=%s and ProductID=%s""",
        (Materialcode,Materialname,Qty,mid,ProductID))
    obj = MsBOMDetail.objects.filter(ProductID=ProductID).values_list('MaterialCode', 'MaterialName', 'MaterialQty','id')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)


def ADDBOM_View(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('PID')
    logger.info(ProductID)
    ProductName=request.POST.get('PName')
    logger.info(ProductName)
    ProductModel=request.POST.get('PModel')
    logger.info(ProductModel)
    ProductStatus=request.POST.get('PStatus')
    logger.info(ProductStatus)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if ProductID != None:
        if MsBOMHeader.objects.filter(ProductID=ProductID).count() >0:
            return render(request, 'AddBillOfMaterial.html',{'UserRole':userrole,'PType':MsProduct.objects.filter(ProductType='Finish Good'),'Mtype':MsProduct.objects.filter(ProductType='Material'),'Error':'Product Already Exists'}) 
        else:
            cursor.execute("""INSERT INTO blog_msbomheader(ProductID,ProductName,ProductModel,ProductStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,ProductName,ProductModel,ProductStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return render_to_response('ViewBOM.html',{'UserRole':userrole,'obj':MsBOMHeader.objects.all(),'full_name':request.user.first_name})
    else:
	return render(request, 'AddBillOfMaterial.html',{'UserRole':userrole,'PType':MsProduct.objects.filter(ProductType='Finish Good'),'Mtype':MsProduct.objects.filter(ProductType='Material')})

def View_BOM(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewBOM.html',{'UserRole':userrole,'obj':MsBOMHeader.objects.all(),'full_name':request.user.first_name})


def EditBOM_View(request,u_id):
    userrole=get_role(request.user.email)
    results = MsBOMDetail.objects.raw("SELECT * FROM blog_msbomheader WHERE id=('%s')"%(u_id))
    for b in results:
        return render(request, 'EditBillOfMaterial.html',{'PType':MsProduct.objects.filter(ProductType='Finish Good'),
                                                         'Mtype':MsProduct.objects.filter(ProductType='Material'),
                                                         'obj':MsBOMDetail.objects.filter(ProductID=b.ProductID),
                                                         'ProductID':b.ProductID,
                                                         'ProductName':b.ProductName,
                                                         'ProductModel':b.ProductModel,
                                                         'PStatus':b.ProductStatus,
                                                         'uid':u_id,
                                                         'UserRole':userrole,
                                                         'full_name':request.user.first_name
                                                         })

def Edit_BOMaterialView(request,u_id):
    userrole=get_role(request.user.email)
    results = MsBOMDetail.objects.raw("SELECT * FROM blog_msbomdetail  WHERE id=('%s')"%(u_id))
    cursor = connection.cursor()
    for b in results:
        #cursor.execute("SELECT id FROM blog_msbomheader where ProductID=('%s')" % (b.ProductID))
        #Mhid=cursor.fetchone()[0]
        #logger.info(Mhid)
        #'Pid':Mhid,
        return render(request, 'BillOfMaterial.html',{'Mtype':MsProduct.objects.filter(ProductType='Material'),
                                                    'Materialcode':b.MaterialCode,
                                                    'Materialname':b.MaterialName,
                                                    'MQty':b.MaterialQty,
                                                    'uid':u_id,
                                                    'UserRole':userrole,
                                                    'full_name':request.user.first_name
                                                         })
def Update_BOMaterialView(request):
    userrole=get_role(request.user.email)
    mid=request.POST.get('uid')
    Materialcode=request.POST.get('Materialcode')
    Materialname=request.POST.get('Materialname')
    Qty=request.POST.get('Qty')
    Pid=request.POST.get('Pid')
    cursor = connection.cursor()
    cursor.execute("""UPDATE blog_msbomdetail SET MaterialCode=%s,MaterialName=%s,MaterialQty=%s WHERE id=%s""",
    (Materialcode,Materialname,Qty,mid))
    return HttpResponseRedirect('/accounts/EditBOM/'+ str(Pid),{'UserRole':userrole,'PType':MsProduct.objects.filter(ProductType='Finish Good'),'Mtype':MsProduct.objects.filter(ProductType='Material'),'full_name':request.user.first_name})
    
def UpdateBOM_View(request):
    userrole=get_role(request.user.email)
    billid=request.POST.get('uid')
    ProductId=request.POST.get('PID')
    PStatus=request.POST.get('PStatus')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("""UPDATE blog_msbomheader SET ProductStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
                   (PStatus,LastUpdateOn,LastUpdateBy,billid))
    return HttpResponseRedirect('/accounts/ViewBOM/',{'UserRole':userrole,'obj':MsBOMDetail.objects.all(),'PType':MsProduct.objects.filter(ProductType='Finish Good'),'Mtype':MsProduct.objects.filter(ProductType='Material'),'full_name':request.user.first_name})
    

def Product_Details(request):
    DataFromPage=request.GET.get('ProductID')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName  FROM blog_msproduct where ProductID=('%s')" % (DataFromPage))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    cursor.execute("SELECT ProductModel  FROM blog_msproduct where ProductID=('%s')" % (DataFromPage))
    ProductModel=cursor.fetchone()[0]
    logger.info(ProductModel)
    ValidationData=''
    if MsBOMHeader.objects.filter(ProductID=DataFromPage).count()>0:
        ValidationData='Data already exists Please Select another Product'
    Data=ProductName + ',' + ProductModel + ',' + ValidationData
    logger.info(Data)
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

def Material_Details(request):
    DataFromPage=request.GET.get('Mcode')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName  FROM blog_msproduct where ProductID=('%s')" % (DataFromPage))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    
    if DataFromPage:
        c = {
         'Materialdata':ProductName,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Materialdata':ProductName,
             }
        logger.info(c)
    return HttpResponse(ProductName)

#-----------------------------------------------------------------Purchase Order---------------------------------------------

def AddPurchaseOrder_View(request):
    userrole=get_role(request.user.email)
    PONumber=request.POST.get('PONO')
    logger.info(PONumber)
    PODate=request.POST.get('PODate')
    logger.info(PODate)
    PrincipalID=request.POST.get('PrncID')
    logger.info(PrincipalID)
    PrincipalName=request.POST.get('PrncplName')
    logger.info(PrincipalName)
    PrincipalStatus=request.POST.get('PrncStatus')
    logger.info(PrincipalStatus)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if PONumber is not None and PODate is not None:
        if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).count()>0:
            cursor.execute("SELECT PONumber  FROM blog_txpurchaseorderhdr where PrincipalId=('%s')" % (PrincipalID))
            PrincipalId=cursor.fetchone()[0]
            logger.info(PrincipalId)
            if PrincipalId is None:
                return render(request, 'AddPurchseOrder.html',{'UserRole':userrole,'Error':'Principal ID and PO NUmber does not match'})
            else:
                if PONumber==PrincipalId:
                    cursor.execute("""INSERT INTO blog_txpurchaseorderhdr(PONumber,PODate,PrincipalId,PrincipalName,POStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(PONumber,PODate,PrincipalID,PrincipalName,PrincipalStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
                    return HttpResponseRedirect('/accounts/ViewPurchaseOrder/',{'UserRole':userrole,'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal').filter(ThirdPartyStatus='Active'),'obj':TxPurchaseOrderDtl.objects.all(),'full_name':request.user.first_name})
                else:
                    return render(request, 'AddPurchseOrder.html',{'UserRole':userrole,'full_name':request.user.first_name,'Error':'Principal ID and PO NUmber does not match'})
        else:
            cursor.execute("""INSERT INTO blog_txpurchaseorderhdr(PONumber,PODate,PrincipalId,PrincipalName,POStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(PONumber,PODate,PrincipalID,PrincipalName,PrincipalStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            return HttpResponseRedirect('/accounts/ViewPurchaseOrder/',{'UserRole':userrole,'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal').filter(ThirdPartyStatus='Active'),'obj':TxPurchaseOrderDtl.objects.all(),'full_name':request.user.first_name})
    else:
        return render(request, 'AddPurchseOrder.html',{'UserRole':userrole,'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal').filter(ThirdPartyStatus='Active'),'obj':TxPurchaseOrderDtl.objects.all(),'full_name':request.user.first_name})

def AddMaterial_OR_Product_View(request,u_id):
    logger.info(u_id)
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT PrincipalID FROM blog_txpurchaseorderhdr where id=('%s')" % (u_id))
    prncplID=cursor.fetchone()[0]
    logger.info(prncplID)
    cursor.execute("SELECT PONumber FROM blog_txpurchaseorderhdr where id=('%s')" %(u_id))
    PONumber=cursor.fetchone()[0]
    logger.info(PONumber)
    return render(request, 'AddMaterial.html',{'UserRole':userrole,'uid':u_id,'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'obj':TxPurchaseOrderDtl.objects.filter(PONumber=PONumber),'PrdctID':MsProduct.objects.filter(PrincipalID=prncplID).filter(ProductStatus='Active'),'full_name':request.user.first_name})
    
def TestAddMaterial(request):
    userrole=get_role(request.user.email)
    uid=request.POST.get('uid')
    logger.info(uid)
    ProductCode=request.POST.get('prdctcode')
    logger.info(ProductCode)
    ProductName=request.POST.get('Prdctname')
    logger.info(ProductName)
    Quantity=request.POST.get('Qnty')
    logger.info(Quantity)
    EstimatedDeliveryDate=request.POST.get('DlvryDate')
    logger.info(EstimatedDeliveryDate)
    POStatus=request.POST.get('POStatus')
    logger.info(POStatus)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("SELECT PONumber FROM blog_txpurchaseorderhdr where id=('%s')" %(uid))
    PONumber=cursor.fetchone()[0]
    logger.info(PONumber)
    if ProductCode != None:
        cursor.execute("""INSERT INTO blog_txpurchaseorderdtl(PONumber,ProductId,ProductName,POReceivingQty,Quantity,EstimatedDeliveryDate,POStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(PONumber,ProductCode,ProductName,'0',Quantity,EstimatedDeliveryDate,POStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        MaterialCount=TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).count()
        cursor.execute("""UPDATE blog_txpurchaseorderhdr SET MaterialCount=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE PONumber=%s""",(MaterialCount,LastUpdateOn,LastUpdateBy,PONumber))
        return render(request, 'Viewpurchaseorder.html',{'UserRole':userrole,'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'obj':TxPurchaseOrderHdr.objects.all(),'full_name':request.user.first_name})
    else:
        return render(request, 'AddMaterial.html',{'UserRole':userrole,'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'obj':TxPurchaseOrderDtl.objects.filter(PONumber=PONumber),'full_name':request.user.first_name})

def PO_Product_Details(request):
    DataFromPage=request.GET.get('Productcode')
    logger.info(DataFromPage)
    uid=request.GET.get('Productid')
    logger.info(uid)
    cursor = connection.cursor()
    cursor.execute("SELECT PONumber FROM blog_txpurchaseorderhdr where id=('%s')" %(uid))
    PONumber=cursor.fetchone()[0]
    logger.info(PONumber)
    cursor.execute("SELECT ProductName  FROM blog_msproduct where ProductID=('%s')" % (DataFromPage))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    ValidationData=""
    if TxPurchaseOrderDtl.objects.filter(ProductId=DataFromPage).filter(PONumber=PONumber).count()>0:
        ValidationData="ProductID for this PONumber already exists"
    Data=ProductName + ',' + ValidationData
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

def Add_PO_Product_Details(request):
    DataFromPage=request.GET.get('principalid')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT ThirdPartyName  FROM blog_thirdparty where ThirdPartyID=('%s')" % (DataFromPage))
    ProductName=cursor.fetchone()[0]
    Productvalidation=''
    if MsProduct.objects.filter(PrincipalID=DataFromPage).filter(ProductStatus='Active').count()==0:
        Productvalidation="Selected Principal does not contain Products.Please add Products for this Principal"
    Data=ProductName + ',' + Productvalidation
    
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)


def EditPurchaseOrder_View(request,u_id):
    logger.info(u_id)
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT PONumber FROM blog_txpurchaseorderhdr where id=('%s')" %(u_id))
    PONumber=cursor.fetchone()[0]
    results = TxPurchaseOrderDtl.objects.raw('SELECT * FROM blog_txpurchaseorderhdr where  id=%s',[u_id])
    for b in results:
        return render(request, 'EditPurchseOrder.html',{'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),
                                                        'PONumber':b.PONumber,
                                                        'PODate':b.PODate,
                                                        'PrincipalID':b.PrincipalId,
                                                        'principalName':b.PrincipalName,
                                                        'POStatus':b.POStatus,
                                                        'uid':u_id,
                                                        'obj':TxPurchaseOrderDtl.objects.filter(PONumber=PONumber),
                                                        'UserRole':userrole,
                                                        'full_name':request.user.first_name
                                                         })

def EditMaterial_View(request,PoNo,uid):
    logger.info(PoNo)
    logger.info(uid)
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT PrincipalID FROM blog_txpurchaseorderhdr where PONumber=('%s')" % (PoNo))
    prncplID=cursor.fetchone()[0]
    logger.info(prncplID)
    cursor.execute("SELECT id FROM blog_txpurchaseorderhdr where PONumber=('%s')" % (PoNo))
    POid=cursor.fetchone()[0]
    logger.info(POid)
    
    results = TxPurchaseOrderDtl.objects.raw('SELECT * FROM blog_txpurchaseorderdtl where  id=%s',[uid])
    for b in results:
        return render(request, 'EditMaterial.html',{'uid':PoNo,
                                                    'mid':uid,
                                                    'POid':POid,
                                                    'ProductId':b.ProductId,
                                                    'ProductName':b.ProductName,
                                                    'Quantity':b.Quantity,
                                                    'DeliveryDate':b.EstimatedDeliveryDate,
                                                    'POStatus':b.POStatus,
                                                    'PrdctID':MsProduct.objects.filter(PrincipalID=prncplID).filter(ProductStatus='Active'),
                                                    'UserRole':userrole,
                                                    'full_name':request.user.first_name
                                                    })
def UpdateMaterial_View(request):
    userrole=get_role(request.user.email)
    mid=request.POST.get('mid')
    PoNO=request.POST.get('uid')
    ProductId=request.POST.get('prdctcode')
    ProductName=request.POST.get('Prdctname')
    Quantity=request.POST.get('Qnty')
    EstimatedDeliveryDate=request.POST.get('DlvryDate')
    POid=request.POST.get('POid')
    cursor = connection.cursor()
    cursor.execute("""UPDATE blog_txpurchaseorderdtl SET Quantity=%s,EstimatedDeliveryDate=%s WHERE id=%s""",
    (Quantity,EstimatedDeliveryDate,mid))
    #cursor.execute("SELECT id FROM blog_txpurchaseorderhdr where PONumber=('%s')" % (PoNO))
    #POid=cursor.fetchone()[0]
    #logger.info(POid)
    return HttpResponseRedirect('/accounts/EditPurchaseOrder/' + str(POid) ,{'UserRole':userrole,'obj':TxPurchaseOrderDtl.objects.all(),'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'PrdctID':MsProduct.objects.filter(ProductType='Material'),'full_name':request.user.first_name})


    
def UpdatePurchaseOrder_View(request):
    userrole=get_role(request.user.email)
    billid=request.POST.get('uid')
    logger.info(billid)
    if request.POST.get('_delete'):
        test=request.POST.getlist('PurchaseCheck')
        logger.info(test)
        TxPurchaseOrderDtl.objects.filter(id__in=request.POST.getlist('PurchaseCheck')).delete()
        logger.info("mbdcfhjhjh")
        return HttpResponseRedirect('/accounts/EditPurchaseOrder/' + str(billid) ,{'UserRole':userrole,'obj':TxPurchaseOrderDtl.objects.all(),'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'PrdctID':MsProduct.objects.filter(ProductType='Material'),'full_name':request.user.first_name})
    PONumber=request.POST.get('PONO')
    PODate=request.POST.get('PODate')
    PrincipalID=request.POST.get('PrncID')
    logger.info(PrincipalID)
    PrincipalName=request.POST.get('PrncplName')
    PrincipalStatus=request.POST.get('PrncStatus')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("""UPDATE blog_txpurchaseorderhdr SET PODate=%s,POStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
                   (PODate,PrincipalStatus,LastUpdateOn,LastUpdateBy,billid))
    return HttpResponseRedirect('/accounts/ViewPurchaseOrder/',{'UserRole':userrole,'obj':TxPurchaseOrderDtl.objects.all(),'PrncID':ThirdParty.objects.filter(ThirdPartyType='Principal'),'PrdctID':MsProduct.objects.filter(ProductType='Material'),'full_name':request.user.first_name})


def View_PurchaseOrder(request):
	if request.user.username == '':
		return HttpResponseRedirect('/accounts/login/')
	else:
		return render_to_response('Viewpurchaseorder.html',{'obj':TxPurchaseOrderHdr.objects.all(),'full_name':request.user.first_name})

def PO_NO_Error_Label(request):
    PONumberfrompage=request.GET.get('val')
    logger.info(PONumberfrompage)
    if TxPurchaseOrderHdr.objects.filter(PONumber=PONumberfrompage).count()>0:
        Data="PO Number already exists"
    else:
        Data=None
    if PONumberfrompage:
        c = {
         'Pagedata':Data,
         }
    else:
        PONumberfrompage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

#-----------------------------------------------------Shipment From Manufacture------------------------------------------

def ShipmentFManufacture_Details(request):
    DataFromPage=request.GET.get('PONumber')
    logger.info(DataFromPage)
    Validationmessage=''
    PODate=''
    EDate=''
    ShipNO=''
    if TxPurchaseOrderDtl.objects.filter(PONumber=DataFromPage).count()==0:
        Validationmessage="Please add Products for this PO Number"
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT PODate  FROM blog_txpurchaseorderhdr where PONumber=('%s')" % (DataFromPage))
        PODate=cursor.fetchone()[0]
        logger.info(PODate)
    Data=str(PODate) + ',' +  Validationmessage
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

def SFM_Product_Details(request):
    DataFromPage=request.GET.get('PONumber')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(ProductId)  FROM blog_txpurchaseorderdtl where PONumber=('%s')" % (DataFromPage))
    ProductId=cursor.fetchone()[0]
    logger.info(ProductId)
    if DataFromPage:
        c = {
         'Pagedata':ProductId,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':ProductId,
             }
        logger.info(c)
    return HttpResponse(ProductId)

def SFM_ProductEDate_details(request):
    DataFromPage=request.GET.get('ProductID')
    logger.info(DataFromPage)
    PONumber=request.GET.get('PONumber')
    logger.info(PONumber)
    cursor = connection.cursor()
    cursor.execute("SELECT  EstimatedDeliveryDate FROM blog_txpurchaseorderdtl where ProductId=('%s') and PONumber=('%s')" % (DataFromPage,PONumber))
    EstimatedDeliveryDate=cursor.fetchone()[0]
    logger.info(EstimatedDeliveryDate)
    SNO=randint(100000, 999999)
    ShipNO='SHIP' + str(SNO)
    cursor.execute("SELECT Quantity-POReceivingQty AS Diff FROM blog_txpurchaseorderdtl where ProductId=('%s') and PONumber=('%s')" % (DataFromPage,PONumber))
    QtyDiff=cursor.fetchone()[0]
    logger.info(QtyDiff)
    Qtyvalue=int(QtyDiff)
    Data=str(EstimatedDeliveryDate) + ',' + ShipNO + ',' + str(Qtyvalue)
    return HttpResponse(Data)

def ADD_ShipmentFManufacture(request):
    userrole=get_role(request.user.email)
    PONO=request.POST.get('PONumber')
    PODate=request.POST.get('PODate')
    PID=request.POST.get('PID')
    DeliveryDate=request.POST.get('DeliveryDate')
    ShipNo=request.POST.get('ShipNo')
    ShipDate=request.POST.get('ShipDate')
    ShipAWB=request.POST.get('ShipAWB')
    SFreight=request.POST.get('SFreight')
    SQuantity=request.POST.get('SQuantity')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    if PONO != None:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_shipmentfrommanufacture(PONumber,PODate,ProductID,EstimatedDelivery,ShipNumber,ShipDate,ShipAWB,ShipFreightName,ShipmentQuantity,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(PONO,PODate,PID,DeliveryDate,ShipNo,ShipDate,ShipAWB,SFreight,SQuantity,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return render_to_response('ViewShipmentFromManufacture.html',{'UserRole':userrole,'obj':ShipmentFromManufacture.objects.all(),'full_name':request.user.first_name})
    else:
        return render(request, 'ShipmentFromManufacture.html',{'full_name':request.user.first_name,'UserRole':userrole,'PONO':TxPurchaseOrderHdr.objects.filter(POStatus='Open'),'FName':ThirdParty.objects.filter(ThirdPartyType='Freight').filter(ThirdPartyStatus='Active')})


def View_SFM(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewShipmentFromManufacture.html',{'full_name':request.user.first_name,'UserRole':userrole,'obj':ShipmentFromManufacture.objects.all(),'full_name':request.user.first_name})


def Edit_SFM(request,u_id):
    userrole=get_role(request.user.email)
    SFMList = ShipmentFromManufacture.objects.raw('SELECT * FROM blog_shipmentfrommanufacture where id =%s',[u_id])
    for s in SFMList:
		if request.user.username == '':
			return HttpResponseRedirect('/accounts/login/')
		else:                       
			return render(request, 'EditShipmentFromManufacture.html',{'PONumber':s.PONumber,
                                                                'PODate':s.PODate,
                                                                'DeliveryDate':s.EstimatedDelivery,
                                                                'ShipNo':s.ShipNumber,
                                                                'ShipDate':s.ShipDate,
                                                                'ShipAWB':s.ShipAWB,
                                                                'SFreight':s.ShipFreightName,
                                                                'SQuantity':s.ShipmentQuantity,
                                                                'CreatedOn':s.CreatedOn,
                                                                'CreatedBy':s.CreatedBy,
                                                                'LastUpdateOn':s.LastUpdateOn,
                                                                'LastUpdateBy':s.LastUpdateBy,
                                                                'PID':TxPurchaseOrderDtl.objects.filter(PONumber=s.PONumber),
                                                                'FName':ThirdParty.objects.filter(ThirdPartyType='Freight').filter(ThirdPartyStatus='Active'),
                                                                'ProductID':s.ProductID,
                                                                'UserRole':userrole,
								'uid':u_id,
                                                                'full_name':request.user.first_name
                                                   })
												   
def Update_SFM(request):
        userrole=get_role(request.user.email)
	SFMid=request.POST.get('uid')
	logger.info(SFMid)
	PONO=request.POST.get('PONumber')
        PODate=request.POST.get('PODate')
        PID=request.POST.get('PID')
        DeliveryDate=request.POST.get('DeliveryDate')
        ShipNo=request.POST.get('ShipNo')
        ShipDate=request.POST.get('ShipDate')
        ShipAWB=request.POST.get('ShipAWB')
        SFreight=request.POST.get('SFreight')
        SQuantity=request.POST.get('SQuantity')
	now=datetime.now()
        LastUpdateOn=str(now)[:19]
        LastUpdateBy=request.user.first_name
	cursor = connection.cursor()
	cursor.execute("""UPDATE blog_shipmentfrommanufacture SET ProductID=%s,EstimatedDelivery=%s,ShipDate=%s,ShipAWB=%s,ShipFreightName=%s,ShipmentQuantity=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(PID,DeliveryDate,ShipDate,ShipAWB,SFreight,SQuantity,LastUpdateOn,LastUpdateBy,SFMid))
	cursor.execute("""UPDATE blog_txpurchaseorderdtl SET EstimatedDeliveryDate=%s WHERE PONumber=%s""",(DeliveryDate,PONO))
	return HttpResponseRedirect('/accounts/ViewSFM/',{'full_name':request.user.first_name,'UserRole':userrole,'full_name':request.user.first_name})

def SFM_Quantity_details(request):
    DataFromPage=request.GET.get('val')
    logger.info(DataFromPage)
    PONumber=request.GET.get('PONumber')
    logger.info(PONumber)
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    formval=request.GET.get('formval')
    cursor = connection.cursor()
    if formval == "Insert":
        if ShipmentFromManufacture.objects.filter(PONumber=PONumber).filter(ProductID=ProductID).count()>0:
            cursor.execute("SELECT SUM(ShipmentQuantity) FROM blog_shipmentfrommanufacture where PONumber=('%s') and ProductId=('%s')" %(PONumber,ProductID))
            ShipMentQuantity=cursor.fetchone()[0]
            logger.info(ShipMentQuantity)
            cursor.execute("SELECT Quantity FROM blog_txpurchaseorderdtl where PONumber=('%s') and ProductId=('%s')" %(PONumber,ProductID))
            Quantity=cursor.fetchone()[0]
            logger.info(Quantity)
            RemainingQuantity=int(Quantity)-int(ShipMentQuantity)
            if int(DataFromPage) > int(RemainingQuantity):
                ValidationData="Quantity value is more than the remaining quantity for this PO and Product ID"
            else:
                ValidationData=''
        else:
            cursor.execute("SELECT Quantity FROM blog_txpurchaseorderdtl where PONumber=('%s') and ProductId=('%s')" %(PONumber,ProductID))
            Quantity=cursor.fetchone()[0]
            logger.info(Quantity)
            if int(DataFromPage) > int(Quantity):
                ValidationData="Quantity value is more than PO quantity value, please check again"
            else:
                ValidationData=''
    elif formval == "Edit":
        cursor.execute("SELECT Quantity FROM blog_txpurchaseorderdtl where PONumber=('%s') and ProductId=('%s')" %(PONumber,ProductID))
        Quantity=cursor.fetchone()[0]
        logger.info(Quantity)
        if int(DataFromPage) > int(Quantity):
            ValidationData="Quantity value is more than PO quantity value, please check again"
        else:
            ValidationData=''
        
    logger.info(ValidationData)
    if DataFromPage:
        c = {
         'Pagedata':ValidationData,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':ValidationData,
             }
        logger.info(c)
    return HttpResponse(ValidationData)


#-----------------------------------Custom Clearance--------------------------------------------------------------------------------

def CustomClearance_Details(request):
    DataFromPage=request.GET.get('PONumber')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    ValidationMessage=''
    if TxPurchaseOrderDtl.objects.filter(PONumber=DataFromPage).count()==0 or ShipmentFromManufacture.objects.filter(PONumber=DataFromPage).count()==0:
        ValidationMessage="Please add Products/Shipment Details for this PO Number"
        Data='' + ',' + '' + ',' + '' + ',' + ValidationMessage         
    else:
        cursor.execute("select PODate,PrincipalId,PrincipalName from blog_txpurchaseorderhdr where PONumber=('%s')" % (DataFromPage))
        TxData=cursor.fetchone()
        logger.info(TxData)
        Data=str(TxData[0]) + ',' + str(TxData[1]) + ',' + TxData[2] + ',' + ValidationMessage 
    logger.info(Data)
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

def ShipProductID_Details(request):
    DataFromPage=request.GET.get('PONumber')
    logger.info(DataFromPage)
    obj=ShipmentFromManufacture.objects.filter(PONumber=DataFromPage).values_list('PONumber','ShipNumber','ProductID')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)


def ShipNo_Details(request):
    PONumber=request.GET.get('PONumber')
    logger.info(PONumber)
    ShipNo=request.GET.get('ShipNo')
    logger.info(ShipNo)
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    ValidationData=''
    cursor = connection.cursor()
    if CustomClearance.objects.filter(PONumber=PONumber).filter(ShipNumber=ShipNo).filter(ProductID=ProductID).count()>0:
        ValidationData='Data already present for this PONumber please try again'
        ShipData='' + ',' + '' + ',' + '' + ',' + '' + ',' + '' + ',' + '' + ',' + '' + ',' +ValidationData
    else:
        cursor.execute("select ProductName,Quantity,EstimatedDeliveryDate from blog_txpurchaseorderdtl where PONumber=('%s') and ProductId=('%s')" % (PONumber,ProductID))
        TxData=cursor.fetchone()
        logger.info(TxData)
        cursor.execute("select ShipDate,ShipAWB,ShipFreightName,ShipmentQuantity from blog_shipmentfrommanufacture where ShipNumber=('%s')" % (ShipNo))
        SData=cursor.fetchone()
        logger.info(SData)
        ShipData=TxData[0] + ',' + str(TxData[1]) + ',' + str(TxData[2]) + ',' + str(SData[0]) + ',' + SData[1] + ',' + SData[2] + ',' + SData[3] + ',' + ValidationData
    return HttpResponse(ShipData)

def ProductID_Details(request):
    DataFromPage=request.GET.get('ProductID')
    logger.info(DataFromPage)
    PONumber=request.GET.get('PONumber')
    logger.info(PONumber)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName,Quantity,EstimatedDeliveryDate  FROM blog_txpurchaseorderdtl where ProductId=('%s') and PONumber=('%s')" % (DataFromPage,PONumber))
    PDetails=cursor.fetchone()
    logger.info(PDetails)
    Data=PDetails[0] + ',' + PDetails[1] + ',' + str(PDetails[2])
    return HttpResponse(Data)

def ProductName_Details(request):
    DataFromPage=request.GET.get('ProductID')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName  FROM blog_msproduct where ProductID=('%s')" % (DataFromPage))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    if DataFromPage:
        c = {
         'Pagedata':ProductName,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':ProductName,
             }
        logger.info(c)
    return HttpResponse(ProductName)
    


def ADD_CustomClearance(request):
    userrole=get_role(request.user.email)
    PONumber=request.POST.get('PONumber')
    PODate=request.POST.get('PODate')
    PSID=request.POST.get('PSID')
    #ProductID=request.POST.get('ProductID')
    PrinicpalID=request.POST.get('PrinicpalID')
    ProductName=request.POST.get('ProductName')
    PrincipalName=request.POST.get('PrincipalName')
    POQuantity=request.POST.get('POQuantity')
    DeliveryDate=request.POST.get('DeliveryDate')
    #ShipNo=request.POST.get('ShipNo')
    ShipDate=request.POST.get('ShipDate')
    ShipAWB=request.POST.get('ShipAWB')
    SFreight=request.POST.get('SFreight')
    SQuantity=request.POST.get('SQuantity')
    HsCode=request.POST.get('HsCode')
    StartDate=request.POST.get('StartDate')
    FinishDate=request.POST.get('FinishDate')
    CustomClearanceStatus=request.POST.get('ClearanceStatus')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    if CustomClearance.objects.filter(HsCode=HsCode).count()>0:
        return render(request, 'CustomClearance.html',{'full_name':request.user.first_name,'UserRole':userrole,'PONO':TxPurchaseOrderHdr.objects.filter(POStatus='Open'),'ProductID':TxPurchaseOrderDtl.objects.all(),'Error':'HSCode Already exists '})
    if HsCode != None:
        d=PSID.split(",")
        ShipNo=d[0]
        ProductID=d[1]
        logger.info(ProductID)
        logger.info(ShipNo)
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_customclearance(PONumber,PODate,ProductID,ProductName,POQuantity,CustomClearanceStatus,PrincipalID,PrincipalName,EstimatedDeliveryDate,ShipNumber,ShipDate,ShipAWB,ShipFreightName,ShipmentQuantity,HsCode,StartDate,FinishDate,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(PONumber,PODate,ProductID,ProductName,POQuantity,CustomClearanceStatus,PrinicpalID,PrincipalName,DeliveryDate,ShipNo,ShipDate,ShipAWB,SFreight,SQuantity,HsCode,StartDate,FinishDate,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return render_to_response('ViewCustomClearance.html',{'full_name':request.user.first_name,'UserRole':userrole,'obj':CustomClearance.objects.all(),'full_name':request.user.first_name})
    else:
        return render(request, 'CustomClearance.html',{'full_name':request.user.first_name,'UserRole':userrole,'PONO':TxPurchaseOrderHdr.objects.filter(POStatus='Open')})
    
    
		
def View_CustomClearance(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewCustomClearance.html',{'full_name':request.user.first_name,'UserRole':userrole,'obj':CustomClearance.objects.all(),'full_name':request.user.first_name})


def Edit_CustomClearance(request,u_id):
    userrole=get_role(request.user.email)
    now= datetime.now()
    currentDate="%s-%s-%s" % (now.year, now.month, now.day)
    logger.info(currentDate)
    CCList = CustomClearance.objects.raw('SELECT * FROM blog_customclearance where id =%s',[u_id])
    for c in CCList:
		if request.user.username == '':
			return HttpResponseRedirect('/accounts/login/')
		else:
			return render(request, 'EditCustomClearance.html',{'PONumber':c.PONumber,
                                                                'PODate':c.PODate,                                                                
                                                                'PID':c.ProductID,
                                                                'ProductName':c.ProductName,
                                                                'PrinicpalID':c.PrincipalID,
                                                                'PrincipalName':c.PrincipalName,
                                                                'POQuantity':c.POQuantity,
                                                                'DeliveryDate':c.EstimatedDeliveryDate,
                                                                'ShipNo':c.ShipNumber,
                                                                'ShipDate':c.ShipDate,
                                                                'ShipAWB':c.ShipAWB,
                                                                'SFreight':c.ShipFreightName,
                                                                'SQuantity':c.ShipmentQuantity,
                                                                'HsCode':c.HsCode,
                                                                'StartDate':c.StartDate,
                                                                'FinishDate':c.FinishDate,
                                                                'CreatedOn':c.CreatedOn,
                                                                'CreatedBy':c.CreatedBy,
                                                                'LastUpdateOn':c.LastUpdateOn,
                                                                'LastUpdateBy':c.LastUpdateBy,
                                                                'PONO':TxPurchaseOrderHdr.objects.filter(POStatus='Open'),
                                                                'ProductID':TxPurchaseOrderDtl.objects.filter(PONumber=c.PONumber),
                                                                'UserRole':userrole,
								'uid':u_id,
                                                                'nowdate':currentDate,
                                                                'full_name':request.user.first_name
                                                   })
												   
def Update_CustomClearance(request):
    userrole=get_role(request.user.email)
    ccid=request.POST.get('uid')
    logger.info(ccid)
    PONumber=request.POST.get('PONumber')
    PODate=request.POST.get('PODate')
    ProductID=request.POST.get('ProductID')
    PrinicpalID=request.POST.get('PrinicpalID')
    ProductName=request.POST.get('ProductName')
    PrincipalName=request.POST.get('PrincipalName')
    POQuantity=request.POST.get('POQuantity')
    DeliveryDate=request.POST.get('DeliveryDate')
    ShipNo=request.POST.get('ShipNo')
    ShipDate=request.POST.get('ShipDate')
    ShipAWB=request.POST.get('ShipAWB')
    SFreight=request.POST.get('SFreight')
    SQuantity=request.POST.get('SQuantity')
    HsCode=request.POST.get('HsCode')
    StartDate=request.POST.get('StartDate')
    FinishDate=request.POST.get('FinishDate')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    CurrentDate=str(now)[:10]
    logger.info(CurrentDate)
    cursor = connection.cursor()
    if FinishDate==CurrentDate:
        logger.info("FInishDateis equal to current date")
        cursor.execute("""UPDATE blog_customclearance SET PONumber=%s,ProductID=%s,HsCode=%s,StartDate=%s,FinishDate=%s,CustomClearanceStatus="Finished",LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
           (PONumber,ProductID,HsCode,StartDate,FinishDate,LastUpdateOn,LastUpdateBy,ccid))
    elif FinishDate < CurrentDate:
        cursor.execute("""UPDATE blog_customclearance SET PONumber=%s,ProductID=%s,HsCode=%s,StartDate=%s,FinishDate=%s,CustomClearanceStatus="Finished",LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
        (PONumber,ProductID,HsCode,StartDate,FinishDate,LastUpdateOn,LastUpdateBy,ccid))
    elif FinishDate > CurrentDate:
         cursor.execute("""UPDATE blog_customclearance SET PONumber=%s,ProductID=%s,HsCode=%s,StartDate=%s,FinishDate=%s,CustomClearanceStatus="On Progress",LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
        (PONumber,ProductID,HsCode,StartDate,FinishDate,LastUpdateOn,LastUpdateBy,ccid))
    return HttpResponseRedirect('/accounts/ViewCustomClearance/',{'UserRole':userrole,'full_name':request.user.first_name})


def customcleranceErrorLabel(request):
	FinishDate=request.GET.get('FinishDate')
	logger.info(FinishDate)
	TodayDate=request.GET.get('TodayDate')
	logger.info(TodayDate)
	Uid=request.GET.get('Uid')
	Validationmessage=''
        now=datetime.now()
        LastUpdateOn=str(now)[:19]
        LastUpdateBy=request.user.first_name
        cursor = connection.cursor()
	if FinishDate > TodayDate:
            Validationmessage="Custom Clearance Has Not Been Finished Yet, Please Check Again Finish Date"
            logger.info(Validationmessage)
            cursor.execute("""UPDATE blog_customclearance SET CustomClearanceStatus="On Progress",FinishDate=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",(FinishDate,LastUpdateOn,LastUpdateBy,Uid))
        elif FinishDate==TodayDate:
            logger.info("FInishDateis equal to current date")
            cursor.execute("""UPDATE blog_customclearance SET CustomClearanceStatus="Finished",FinishDate=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",(FinishDate,LastUpdateOn,LastUpdateBy,Uid))
        elif FinishDate < TodayDate:
            logger.info("FInishDateis less to current date")
            cursor.execute("""UPDATE blog_customclearance SET CustomClearanceStatus="Finished",FinishDate=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",(FinishDate,LastUpdateOn,LastUpdateBy,Uid))
        return HttpResponse(Validationmessage)

def customclerancemessageLabel(request):
        FinishDate=request.GET.get('FinishDate')
	logger.info(FinishDate)
	TodayDate=request.GET.get('TodayDate')
	logger.info(TodayDate)
	Uid=request.GET.get('Uid')
	Validationmessage=''
        now=datetime.now()
        LastUpdateOn=str(now)[:19]
        LastUpdateBy=request.user.first_name
        cursor = connection.cursor()
        if FinishDate > TodayDate:
            Validationmessage="Custom Clearance Process Still On Progress until given Finish Date,so Status Will Not Change"
            logger.info(Validationmessage)
            cursor.execute("""UPDATE blog_customclearance SET CustomClearanceStatus="On Progress",FinishDate=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",(FinishDate,LastUpdateOn,LastUpdateBy,Uid))
        elif FinishDate==TodayDate:
            cursor.execute("""UPDATE blog_customclearance SET CustomClearanceStatus="Finished",FinishDate=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",(FinishDate,LastUpdateOn,LastUpdateBy,Uid))
            Validationmessage="Custom Clearance Process Has Been Finished Today, so Status Will Change into Finished"
        elif FinishDate < TodayDate:
            cursor.execute("""UPDATE blog_customclearance SET CustomClearanceStatus="Finished",FinishDate=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",(FinishDate,LastUpdateOn,LastUpdateBy,Uid))
            Validationmessage="Custom Clearance Process Has Been Finished on given Finish Date, so Status Will Change into Finished"
        return HttpResponse(Validationmessage)

#---------------------------------------------Receiving Finish Good/Material-------------------------------------------------------------

def Receiving_Details(request):
    DataFromPage=request.GET.get('ShipNo')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT ShipAWB,ShipFreightName,ShipmentQuantity,PONumber,PODate,PrincipalID,PrincipalName,POQuantity,ProductID,ProductName,HsCode,CustomClearanceStatus from blog_customclearance where ShipNumber=('%s')" % (DataFromPage))
    SData=cursor.fetchone()
    logger.info(SData)
    if SData[8]!=None:
        cursor.execute("SELECT ProductSerialNumber FROM blog_msproduct WHERE ProductID=('%s')" % (SData[8]))
        ProductSN=cursor.fetchone()[0]
        logger.info(ProductSN)
    ReceivingID='REC' + str(randint(0001, 9999))
    logger.info(ReceivingID)
    cursor.execute("select ProductType from blog_msproduct where ProductID=('%s')" % (SData[8]))
    ProductType=cursor.fetchone()[0]
    getdata=''
    if TxStockSN.objects.filter(ProductID=SData[8]).count > 0:
        obj=TxStockSN.objects.filter(ProductID=SData[8]).filter(ShipmentNo=DataFromPage).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    Data=SData[0] + ':' + SData[1] + ':' + SData[2] + ':' + SData[3] + ':' + str(SData[4]) + ':' + SData[5] + ':' + SData[6] + ':' + SData[7] + ':' + SData[8] + ':' + SData[9] + ':' + SData[10] + ':' + ProductType + ':' + SData[11] + ':' + ReceivingID + ':' +  ProductSN + ':' + getdata
    logger.info(Data)
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

def SerialNumber_Details(request):
    Productid=request.GET.get('Productid')
    ShipNo=request.GET.get('ShipNo')
    ProductName=request.GET.get('ProductName')
    ProductType=request.GET.get('ProductType')
    SerialNumber=request.GET.get('SerialNumber')
    SQuantity=request.GET.get('SQuantity')
    RecevingID=request.GET.get('RecevingID')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    ValidationData=''
    getdata=''
    SerialCount=TxStockSN.objects.filter(ProductID=Productid).filter(ShipmentNo=ShipNo).count()
    if SerialNumber == '':
        ValidationData='Please Enter Serial Number'
    elif TxStockSN.objects.filter(SerialNumber=SerialNumber).count()>0:
        ValidationData='Data has already been added previously'
    elif SerialCount >= int(SQuantity):
        ValidationData='Serial Number count should not be more than Shipment Quantity'
    else:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_txstocksn(ProductID,ShipmentNo,RefNumber,ProductName,ProductType,SerialNumber,SNStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                   (Productid,ShipNo,RecevingID,ProductName,ProductType,SerialNumber,'IN',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
        obj=TxStockSN.objects.filter(ProductID=Productid).filter(ShipmentNo=ShipNo).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)

def ADD_Receiving(request):
    userrole=get_role(request.user.email)
    ShipNo=request.POST.get('ShipNo')
    PONumber=request.POST.get('PONumber')
    ProductID=request.POST.get('ProductID')
    SQuantity=request.POST.get('SQuantity')
    ReceivingID=request.POST.get('Receiving')
    ReceivingQty=request.POST.get('ReceivingQty')
    ReceivingStatus=request.POST.get('ReceivingStatus')
    WareHouseName=request.POST.get('WareHouseName')
    logger.info(WareHouseName)
    ProductName=request.POST.get('ProductName')
    POQuantity=request.POST.get('POQuantity')
    HsCode=request.POST.get('HsCode')
    PName=request.POST.get('PName')
    logger.info(PName)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    values=TxPurchaseOrderHdr.objects.exclude(POStatus='Closed').values_list('PONumber')
    if ShipNo !=None and ReceivingID !=None:
        logger.info("dsffg")
        if TxReceivingFG_Material.objects.filter(ShipmentNo=ShipNo).filter(POLineProductID=ProductID).filter(PONumber=PONumber).count() >0:
            logger.info("dsffgdsffdgdfg")
            return render(request, 'AddReceiving.html',{'ShipNo':CustomClearance.objects.filter(CustomClearanceStatus='Finished').filter(PONumber__in=values),'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name,'ShipProduct':CustomClearance.objects.all(),'Error':'Data already exists for selected ShipNo,Please Select another PONumberand ShipNo'})
        else:
            if ReceivingQty == '':
                RQty=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
                logger.info(RQty)
            else:
                RQty=request.POST.get('ReceivingQty')
                logger.info(RQty)
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO blog_txreceivingfg_material(ReceivingID,PONumber,POLineProductID,ProductName,ShipmentNo,HsCode,ShipmentQty,ReceivingQty,POQuantity,ReceivingStatus,WarehouseID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ReceivingID,PONumber,ProductID,ProductName,ShipNo,HsCode,SQuantity,RQty,POQuantity,ReceivingStatus,WareHouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            #cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s """,('Partial',PONumber))
            return render_to_response('ViewReceiving.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':TxReceivingFG_Material.objects.all()})
    else:
        return render(request, 'AddReceiving.html',{'ShipNo':CustomClearance.objects.filter(CustomClearanceStatus='Finished').filter(PONumber__in=values),'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name,'ShipProduct':CustomClearance.objects.all()})



def ReceiveQntyCheck(request):
    ProductID=request.GET.get('ProductID')
    ShipQuantity=request.GET.get('ShipQuantity')
    logger.info(ShipQuantity)
    ReceiveQuantity=request.GET.get('ReceiveQuantity')
    logger.info(ReceiveQuantity)
    POQuantity=request.GET.get('POQuantity')
    logger.info(POQuantity)
    ValidationData=''
    if int(ReceiveQuantity) > int(ShipQuantity):
        ValidationData="Receiving Quantity value is more than Shipment Quantity value. Please check it again"
    if int(ReceiveQuantity) > int(POQuantity):
        ValidationData="Receiving Quantity value is more than PO Quantity value. Please check it again"
    return HttpResponse(ValidationData)
		
def View_Receiving(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewReceiving.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':TxReceivingFG_Material.objects.all()})
	
def Edit_Receiving(request,u_id):
    userrole=get_role(request.user.email)
    TxReceivingList = TxReceivingFG_Material.objects.raw('SELECT r.id,r.ShipmentNo,c.ShipAWB,c.ShipFreightName,c.ShipmentQuantity,c.PONumber,c.PODate,c.PrincipalID,c.PrincipalName,c.POQuantity,c.ProductID,c.ProductName,c.HsCode,r.ReceivingID,r.ReceivingQty,r.ReceivingStatus,r.WarehouseID FROM blog_customclearance c,blog_txreceivingfg_material r WHERE r.ShipmentNo=c.ShipNumber AND r.id=%s',[u_id])
    for c in TxReceivingList:
        count=TxStockSN.objects.filter(ShipmentNo=c.ShipmentNo).filter(ProductID=c.ProductID).count()
        cursor = connection.cursor()
        cursor.execute("SELECT ProductSerialNumber from blog_msproduct where ProductID =('%s')" % (c.ProductID))
        ProductSN =  cursor.fetchone()[0]
        logger.info(ProductSN)
	if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
	else:
	    return render(request, 'EditReceiving.html',{
                                                        'ShipNo':c.ShipmentNo,
                                                        'SFreight':c.ShipFreightName,
                                                        'SQuantity':c.ShipmentQuantity,
                                                        'ShipAWB':c.ShipAWB,                                                    
                                                        'PONumber':c.PONumber,
                                                        'ProductID':c.ProductID,
                                                        'ProductName':c.ProductName,
                                                        'PODate':c.PODate,
                                                        'PrinicpalID':c.PrincipalID,
                                                        'PrincipalName':c.PrincipalName,
                                                        'ProductType':'Material',
                                                        'POQuantity':c.POQuantity,
                                                        'HsCode':c.HsCode,
                                                        'CCStatus':'Finished',
                                                        'Receiving':c.ReceivingID,
                                                        'ReceivingQty':c.ReceivingQty,
                                                        'ProductSN':ProductSN,
                                                        'ReceivingStatus':c.ReceivingStatus,
                                                        'WareHouseName':c.WarehouseID,
                                                        'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),
                                                        'obj':TxStockSN.objects.filter(ShipmentNo=c.ShipmentNo).filter(ProductID=c.ProductID),
                                                        'count':count,
                                                        'SerialCount':TxStockSN.objects.filter(ProductID=c.ProductID).count(),
                                                        'UserRole':userrole,
							'uid':u_id,
                                                        'full_name':request.user.first_name
                                                   })

def Update_Receiving(request):
    userrole=get_role(request.user.email)
    rid=request.POST.get('uid')
    logger.info(rid)
    ShipNo=request.POST.get('ShipNo')
    ProductID=request.POST.get('ProductID')
    ReceivingQty=request.POST.get('ReceivingQty')
    WareHouseName=request.POST.get('WareHouseName')
    SQuantity=request.POST.get('SQuantity')
    ReceivingID=request.POST.get('Receiving')
    StockOut=0
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    #cursor.execute("SELECT WarehouseID  FROM blog_warehouse where WarehouseName=('%s')" % (WareHouseName))
    #WarehouseID=cursor.fetchone()[0]
    if ReceivingQty != None:
        RQty=request.POST.get('ReceivingQty')
    else:
        RQty=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
    cursor.execute("""UPDATE blog_txreceivingfg_material SET ReceivingQty=%s,WarehouseID=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
    (RQty,WareHouseName,LastUpdateOn,LastUpdateBy,rid))
    return HttpResponseRedirect('/accounts/ViewReceiving/',{'UserRole':userrole,'full_name':request.user.first_name})

def all_same(items):
    return all(x == items[0] for x in items)


def StockInsert_Details(request):
    #=randint(100000, 999999)
    ReceivingID=request.GET.get('Receiving')
    ProductID=request.GET.get('ProductID')
    WareHouseName=request.GET.get('WareHouseName')
    ReceivingQty=request.GET.get('ReceivingQty')
    WareHouseName=request.GET.get('WareHouseName')
    ProductName=request.GET.get('ProductName')
    PrincipalName=request.GET.get('PrincipalName')
    ShipNo=request.GET.get('ShipNo')
    PONumber=request.GET.get('PONumber')
    POQuantity=request.GET.get('POQuantity')
    formval=request.GET.get('formval')
    SQuantity=request.GET.get('SQuantity')
    StockOut=0
    Data='Sucess'
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if WareHouseName == '':
        logger.info("DFgdfg")
        Data="Please Select WareHouse"
    else:
        if TxReceivingFG_Material.objects.filter(ReceivingID=ReceivingID).count()>0:
            if ReceivingQty != None:
                RQty=request.GET.get('ReceivingQty')
            else:
                RQty=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
            cursor.execute("""UPDATE blog_txreceivingfg_material SET ReceivingQty=%s,ReceivingStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  ReceivingID=%s""",(RQty,'Received',LastUpdateOn,LastUpdateBy,ReceivingID))
        else:       
            POQuantity=request.GET.get('POQuantity')
            HsCode=request.GET.get('HsCode')
            SQuantity=request.GET.get('SQuantity')
            if ReceivingQty != None:
                RQty=request.GET.get('ReceivingQty')
            else:
                RQty=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
        if formval == "Insert":
            if TxReceivingFG_Material.objects.filter(ShipmentNo=ShipNo).filter(POLineProductID=ProductID).filter(PONumber=PONumber).count() >0:
                Data="Data already exists for selected ShipNo,Please Select another PONumberand ShipNo"
            else:
                cursor.execute("""INSERT INTO blog_txreceivingfg_material(ReceivingID,PONumber,POLineProductID,ProductName,ShipmentNo,HsCode,ShipmentQty,ReceivingQty,POQuantity,ReceivingStatus,WarehouseID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ReceivingID,PONumber,ProductID,ProductName,ShipNo,HsCode,SQuantity,RQty,POQuantity,'Received',WareHouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
                if ReceivingQty!=None:
                    StockSN="No"
                    ReceivingQty=request.GET.get('ReceivingQty')
                    StockBalance=int(ReceivingQty)-int(StockOut)
                    logger.info(StockBalance)
                else:
                    StockSN="Yes"
                    ReceivingQty=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
                    logger.info(ReceivingQty)
                    StockBalance=int(ReceivingQty)-int(StockOut)
                cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ShipmentNo,StockQtyIN,StockQtyOut,StockQtyBalance,ProductName,StockSN,PrincipalName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ReceivingID,"Receiving",WareHouseName,ProductID,ShipNo,ReceivingQty,StockOut,StockBalance,ProductName,StockSN,PrincipalName,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
                if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).filter(ProductId=ProductID).count()>0:
                    cursor.execute("""select POReceivingQty from  blog_txpurchaseorderdtl WHERE  PONumber=%s and ProductId=%s""",(PONumber,ProductID))
                    POReQty=cursor.fetchone()[0]
                    logger.info(POReQty)
                    UpdatedPORQty=int(POReQty) + int(ReceivingQty)
                    cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POReceivingQty=%s WHERE  PONumber=%s and ProductId=%s""",(UpdatedPORQty,PONumber,ProductID))
                cursor.execute("""select sum(ReceivingQty) from  blog_txreceivingfg_material WHERE  PONumber=%s and POLineProductID=%s""",(PONumber,ProductID))
                RQtySum=cursor.fetchone()[0]
                logger.info(RQtySum)
                cursor.execute("""select sum(ShipmentQuantity) from  blog_shipmentfrommanufacture WHERE  PONumber=%s and ProductID=%s""",(PONumber,ProductID))
                SQtySum=cursor.fetchone()[0]
                logger.info(SQtySum)
                logger.info(SQuantity)
                logger.info(POQuantity)
                logger.info(ReceivingQty)
                if int(SQuantity) == int(POQuantity):
                    logger.info("S is equal to P")
                    if int(ReceivingQty) == int(POQuantity):
                        logger.info("R is equal to P")
                        cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Complete',PONumber,ProductID))
                        if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).count()>0:
                            cursor.execute("select GROUP_CONCAT(POStatus) from blog_txpurchaseorderdtl WHERE  PONumber =('%s')" % (PONumber))
                            POStatus=cursor.fetchone()[0]
                            logger.info(POStatus)
                            POStatuslist=POStatus.split(',')
                            if len(set(POStatuslist)) == 1:
                                cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Closed',PONumber))
                            else:
                                cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Open',PONumber))
                            #for i in ProIDs:
                                #cursor.execute("""select POStatus from blog_txpurchaseorderdtl WHERE  PONumber=%s and ProductID=%s""",(PONumber,i))
                                #GetPOStatus=cursor.fetchone()[0]
                                #logger.info(GetPOStatus)
                                
                        
                elif int(SQtySum) == int(POQuantity):
                    logger.info("Ssum is equal to P")
                    if int(RQtySum) == int(POQuantity):
                        logger.info("Rsum is equal to P")
                        cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Complete',PONumber,ProductID))
                        if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).count()>0:
                            cursor.execute("select GROUP_CONCAT(POStatus) from blog_txpurchaseorderdtl WHERE  PONumber =('%s')" % (PONumber))
                            POStatus=cursor.fetchone()[0]
                            logger.info(POStatus)
                            POStatuslist=POStatus.split(',')
                            if len(set(POStatuslist)) == 1:
                                cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Closed',PONumber))
                            else:
                                cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Open',PONumber))
                        #cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Complete',PONumber,ProductID))
                elif int(SQtySum) < int(POQuantity):
                    logger.info("S is less to P")
                    if int(RQtySum) < int(POQuantity):
                        logger.info("R is less to P")
                        cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Partial',PONumber,ProductID))
                elif int(ReceivingQty) < int(POQuantity):
                    logger.info("R is less to P")
                    cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Partial',PONumber,ProductID))
                    #cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s """,('Closed',PONumber))
        elif formval == "Edit":
            if ReceivingQty!=None:
                StockSN="No"
                ReceivingQty=request.GET.get('ReceivingQty')
                StockBalance=int(ReceivingQty)-int(StockOut)
                logger.info(StockBalance)
            else:
                StockSN="Yes"
                ReceivingQty=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
                logger.info(ReceivingQty)
                StockBalance=int(ReceivingQty)-int(StockOut)
            cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ShipmentNo,StockQtyIN,StockQtyOut,StockQtyBalance,ProductName,StockSN,PrincipalName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ReceivingID,"Receiving",WareHouseName,ProductID,ShipNo,ReceivingQty,StockOut,StockBalance,ProductName,StockSN,PrincipalName,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
            if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).filter(ProductId=ProductID).count()>0:
                cursor.execute("""select POReceivingQty from  blog_txpurchaseorderdtl WHERE  PONumber=%s and ProductId=%s""",(PONumber,ProductID))
                POReQty=cursor.fetchone()[0]
                logger.info(POReQty)
                UpdatedPORQty=int(POReQty) + int(ReceivingQty)
                cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POReceivingQty=%s WHERE  PONumber=%s and ProductId=%s""",(UpdatedPORQty,PONumber,ProductID))
            cursor.execute("""select sum(ReceivingQty) from  blog_txreceivingfg_material WHERE  PONumber=%s and POLineProductID=%s""",(PONumber,ProductID))
            RQtySum=cursor.fetchone()[0]
            logger.info(RQtySum)
            cursor.execute("""select sum(ShipmentQuantity) from  blog_shipmentfrommanufacture WHERE  PONumber=%s and ProductID=%s""",(PONumber,ProductID))
            SQtySum=cursor.fetchone()[0]
            logger.info(SQtySum)
            logger.info(SQuantity)
            logger.info(POQuantity)
            logger.info(ReceivingQty)
            if int(SQuantity) == int(POQuantity):
                logger.info("S is equal to P")
                if int(ReceivingQty) == int(POQuantity):
                    logger.info("R is equal to P")
                    cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Complete',PONumber,ProductID))
                    if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).count()>0:
                        cursor.execute("select GROUP_CONCAT(POStatus) from blog_txpurchaseorderdtl WHERE  PONumber =('%s')" % (PONumber))
                        POStatus=cursor.fetchone()[0]
                        logger.info(POStatus)
                        POStatuslist=POStatus.split(',')
                        if len(set(POStatuslist)) == 1:
                            cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Closed',PONumber))
                        else:
                            cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Open',PONumber))
                    #cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Complete',PONumber,ProductID))
            elif int(SQtySum) == int(POQuantity):
                logger.info("Ssum is equal to P")
                if int(RQtySum) == int(POQuantity):
                    logger.info("Rsum is equal to P")
                    cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Complete',PONumber,ProductID))
                    if TxPurchaseOrderDtl.objects.filter(PONumber=PONumber).count()>0:
                        cursor.execute("select GROUP_CONCAT(POStatus) from blog_txpurchaseorderdtl WHERE  PONumber =('%s')" % (PONumber))
                        POStatus=cursor.fetchone()[0]
                        logger.info(POStatus)
                        POStatuslist=POStatus.split(',')
                        if len(set(POStatuslist)) == 1:
                            cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Closed',PONumber))
                        else:
                            cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Open',PONumber))
                    #cursor.execute("""UPDATE blog_txpurchaseorderhdr SET POStatus=%s WHERE  PONumber=%s""",('Complete',PONumber))
            elif int(SQtySum) < int(POQuantity):
                logger.info("S is less to P")
                if int(RQtySum) < int(POQuantity):
                    logger.info("R is less to P")
                    cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Partial',PONumber,ProductID))
            elif int(ReceivingQty) < int(POQuantity):
                logger.info("R is less to P")
                cursor.execute("""UPDATE blog_txpurchaseorderdtl SET POStatus=%s WHERE  PONumber=%s and ProductID=%s""",('Partial',PONumber,ProductID))  
    return HttpResponse(Data)
    
    
def SerialNumberCount_Details(request):
    ShipNo=request.GET.get('ShipNo')
    ProductID=request.GET.get('ProductID')
    Data=0
    if TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()>0:
        Data=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).count()
    return HttpResponse(Data)

def SNValidation_Details(request):
    Productid=request.GET.get('Productid')
    ShipNo=request.GET.get('ShipNo')
    cursor = connection.cursor()
    Data=''
    StockCount=txStock.objects.filter(ShipmentNo=ShipNo).filter(ProductID=Productid).count()
    if StockCount==0:
        Data='Nothing'
    elif StockCount == 1:
        cursor.execute("SELECT StockSN FROM blog_txstock WHERE ProductID=('%s') AND ShipmentNo=('%s')" % (Productid,ShipNo))
        StockStatus=cursor.fetchone()[0]
        if StockStatus == 'Yes':
            Data='Yes'
        elif StockStatus == 'No':
            Data='No'
    return HttpResponse(Data)


def EditSerialNumber_View(request,SN):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT id from blog_txstocksn where SerialNumber =('%s')" % (SN))
    data =  cursor.fetchone()[0]
    logger.info(data)
    return render(request, 'EditRFGSerialNumber.html',{'lblSN':data,'SerialNumber':SN,'UserRole':userrole,'full_name':request.user.first_name})

def SNUpdate_Details(request):
    SNumber=request.GET.get('SNumber')
    lblSN=request.GET.get('lblSN')
    Productid=request.GET.get('Productid')
    ShipNo=request.GET.get('ShipNo')
    cursor = connection.cursor()
    ValidationData=''
    getdata=''
    if TxStockSN.objects.filter(SerialNumber=SNumber).count() > 0:
        ValidationData='Data has already been added please check it again'
    else:
        cursor.execute("""UPDATE blog_txstocksn SET SerialNumber=%s WHERE  id=%s""",(SNumber,lblSN))
        obj=TxStockSN.objects.filter(ProductID=Productid).filter(ShipmentNo=ShipNo).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)
    
def DeleteSerialNumber_View(request,SN):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT id from blog_txstocksn where SerialNumber =('%s')" % (SN))
    data =  cursor.fetchone()[0]
    logger.info(data)
    return render(request, 'DeleteRFGSerialNumber.html',{'SNid':data,'SN':SN,'UserRole':userrole,'full_name':request.user.first_name})

def SNDelete_Details(request):
    SN=request.GET.get('SN')
    SNid=request.GET.get('SNid')
    Productid=request.GET.get('Productid')
    ShipNo=request.GET.get('ShipNo')
    TxStockSN.objects.filter(ProductID=Productid).filter(ShipmentNo=ShipNo).filter(SerialNumber=SN).filter(id=SNid).delete()
    obj=TxStockSN.objects.filter(ProductID=Productid).filter(ShipmentNo=ShipNo).values_list('SerialNumber')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)

def SNDeleteCheck_Details(request):
    ShipNo=request.GET.get('ShipNo')
    ProductID=request.GET.get('ProductID')
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(SerialNumber) from blog_txstocksn where ProductID=('%s') AND ShipmentNo=('%s')" % (ProductID,ShipNo))
    SerialNumbersList=cursor.fetchone()[0]
    logger.info(SerialNumbersList)
    myList = [x for x in SerialNumbersList.split(',') if x]
    logger.info(myList)
    TxStockSN.objects.filter(SerialNumber__in=(myList)).delete()
    obj=TxStockSN.objects.filter(ProductID=ProductID).filter(ShipmentNo=ShipNo).values_list('SerialNumber')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)



# ------------------------------------Stock --------------------------------------------------------------------------------------------
def Stock_summary_Card(request):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
        ProductList = txStock.objects.raw('SELECT id,ProductID,ProductName,WarehouseID,SUM(StockQtyIN-StockQtyOut) AS StockQtyBalance FROM blog_txstock GROUP BY ProductID,WarehouseID')
        logger.info("Hi Test")
	return render_to_response('StockCardSummury.html',{'obj':ProductList,'full_name':request.user.first_name,'UserRole':userrole})

def View_Stock_summary_Card(request,ProductID,Warehouse):
    #logger.info(u_id)
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    #cursor.execute("SELECT ProductID FROM blog_txstock where id=('%s')" % (u_id))
    #Productlist=cursor.fetchone()[0]
    #logger.info(Productlist)
    cursor.execute("SELECT SUM(StockQtyIN) FROM blog_txstock where ProductID=('%s')" % (ProductID))
    StockQtyIN=cursor.fetchone()[0]
    logger.info(StockQtyIN)
    cursor.execute("SELECT SUM(StockQtyOut) FROM blog_txstock where ProductID=('%s')" % (ProductID))
    StockQtyOut=cursor.fetchone()[0]
    logger.info(StockQtyOut)
    cursor.execute("SELECT SUM(StockQtyBalance) FROM blog_txstock where ProductID=('%s')" % (ProductID))
    StockQtyBalance=cursor.fetchone()[0]
    logger.info(StockQtyBalance)
    cursor.execute("SELECT ProductName FROM blog_msproduct where ProductID=('%s')" % (ProductID))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    cursor.execute("SELECT PrincipalName FROM blog_msproduct where ProductID=('%s')" % (ProductID))
    PrincipalName=cursor.fetchone()[0]
    logger.info(PrincipalName)
    cursor.execute("SELECT WarehouseID FROM blog_txstock where ProductID=('%s')" % (ProductID))
    WarehouseID=cursor.fetchone()[0]
    logger.info(WarehouseID)
    #cursor.execute("SELECT SUM(StockQtyBalance) FROM blog_txstock where ProductID=('%s') And WarehouseID=('%s')" % (ProductID,WarehouseID))
    #StockQtyBalance=cursor.fetchone()[0]
    #logger.info(StockQtyBalance)
    cursor.execute("SELECT SUM(StockQtyIN) FROM blog_txstock where ProductID=('%s') And WarehouseID=('%s')" % (ProductID,Warehouse))
    INPStock=cursor.fetchone()[0]
    cursor.execute("SELECT SUM(StockQtyOut) FROM blog_txstock where ProductID=('%s') And WarehouseID=('%s')" % (ProductID,Warehouse))
    OUTStock=cursor.fetchone()[0]
    StockQtyBalance=int(INPStock)-int(OUTStock)
    Stocklist = txStock.objects.raw('SELECT * FROM blog_txstock where ProductID =%s AND WarehouseID=%s',[ProductID,Warehouse])
    for b in Stocklist:
        return render(request, 'StockCardDetails.html',{
                                                        #'obj':txStock.objects.filter(ProductID=ProductID),
                                                        'obj':Stocklist,
                                                        'prdctID':b.ProductID,
                                                        'PrdctName':ProductName,
                                                        'prncplName':PrincipalName,
                                                        'warehouse':Warehouse,
                                                        'UserRole':userrole,
                                                        'StockQtyBalance':StockQtyBalance,
							#'uid':u_id,
                                                        'full_name':request.user.first_name
                                                         })


def View_Stock_summary_Card_For_Search(request,ProductID,Warehouse):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(StockQtyIN) FROM blog_txstock where ProductID=('%s')" % (ProductID))
    StockQtyIN=cursor.fetchone()[0]
    logger.info(StockQtyIN)
    cursor.execute("SELECT SUM(StockQtyOut) FROM blog_txstock where ProductID=('%s')" % (ProductID))
    StockQtyOut=cursor.fetchone()[0]
    logger.info(StockQtyOut)
    cursor.execute("SELECT SUM(StockQtyBalance) FROM blog_txstock where ProductID=('%s')" % (ProductID))
    StockQtyBalance=cursor.fetchone()[0]
    logger.info(StockQtyBalance)
    cursor.execute("SELECT ProductName FROM blog_msproduct where ProductID=('%s')" % (ProductID))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    cursor.execute("SELECT PrincipalName FROM blog_msproduct where ProductID=('%s')" % (ProductID))
    PrincipalName=cursor.fetchone()[0]
    logger.info(PrincipalName)
    cursor.execute("SELECT WarehouseID FROM blog_txstock where ProductID=('%s')" % (ProductID))
    WarehouseID=cursor.fetchone()[0]
    logger.info(WarehouseID)
    cursor.execute("SELECT SUM(StockQtyIN) FROM blog_txstock where ProductID=('%s') And WarehouseID=('%s')" % (ProductID,Warehouse))
    INPStock=cursor.fetchone()[0]
    cursor.execute("SELECT SUM(StockQtyOut) FROM blog_txstock where ProductID=('%s') And WarehouseID=('%s')" % (ProductID,Warehouse))
    OUTStock=cursor.fetchone()[0]
    StockQtyBalance=int(INPStock)-int(OUTStock)
    cursor.execute("SET SESSION group_concat_max_len = 1000000")
    cursor.execute("SELECT GROUP_CONCAT(Refnumber) FROM blog_txstock where ProductID=('%s') And WarehouseID=('%s')" % (ProductID,Warehouse))
    Refnumber=cursor.fetchone()[0]
    logger.info(Refnumber)
    RefnumberIN="'" + Refnumber.replace(',',"','") + "'"
    objRefnumberIN = [x for x in Refnumber.split(',') if x]
    logger.info(RefnumberIN)
    cursor.execute("SELECT GROUP_CONCAT(SerialNumber) FROM blog_txstocksn WHERE SNStatus ='OUT' AND RefNumber IN(%s)"%(RefnumberIN))
    OutSN=cursor.fetchone()[0]
    logger.info(OutSN)
    if OutSN!=None:
		OutSN_List = [x for x in OutSN.split(',') if x]
		Stocklist=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber__in=objRefnumberIN).exclude(SerialNumber__in=OutSN_List)
    else:
		Stocklist=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber__in=objRefnumberIN)
    return render(request, 'StockCardDetailsforSearch.html',{
                                                        'obj':Stocklist,
                                                        'prdctID':ProductID,
                                                        'PrdctName':ProductName,
                                                        'prncplName':PrincipalName,
                                                        'warehouse':Warehouse,
                                                        'UserRole':userrole,
                                                        'StockQtyBalance':StockQtyBalance,
                                                        'full_name':request.user.first_name
                                                         })



def Serial_No_Details(request,u_id):
    logger.info(u_id)
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(ProductID) FROM blog_txstock where id=('%s')" % (u_id))
    Productlist=cursor.fetchone()[0]
    logger.info(Productlist)
    cursor.execute("SELECT RefNumber FROM blog_txstock where id=('%s')" % (u_id))
    RefNumber=cursor.fetchone()[0]
    logger.info(RefNumber)
    return render(request, 'SerialNODeatils.html',{'obj':TxStockSN.objects.filter(ProductID=Productlist).filter(RefNumber=RefNumber),'uid':u_id,'UserRole':userrole,'full_name':request.user.first_name})

def Card_Inquiry_View(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('prdctID')
    logger.info(ProductID)
    ProductName=request.POST.get('prdctName')
    logger.info(ProductName)
    Warehouse=request.POST.getlist('warehouse')
    logger.info(Warehouse)
    myString = ",".join(Warehouse)
    logger.info(myString)
    WarehouseIN="'" + myString.replace(',',"','") + "'"
    logger.info(WarehouseIN)
    PrincipleName=request.POST.get('PrncplName')
    logger.info(PrincipleName)
    #FromDate=request.POST.get('frmdate')
    #logger.info(FromDate)
    #ToDate=request.POST.get('Todate')
    #logger.info(ToDate)
    StockQtyBalance=''
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(DISTINCT ProductID) FROM blog_txstock")
    productslist=cursor.fetchone()[0]
    logger.info(productslist)
    if ProductID !=None:
        cursor.execute("SET SESSION group_concat_max_len = 1000000")
        cursor.execute("SELECT GROUP_CONCAT(ProductID) FROM blog_txstock WHERE ProductID=('%s') AND WarehouseID IN (%s)"  %(ProductID,WarehouseIN))
        Productlist=cursor.fetchone()[0]
        logger.info(Productlist)
        if Productlist ==None:
            return render(request, 'StackCardInquiry.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':MsProduct.objects.all(),'Warehouse':WareHouse.objects.all()})
        cursor.execute("TRUNCATE TABLE  blog_stockcard_result")
        for i in Warehouse:
            results=cursor.execute("SELECT id,ProductID,ProductName,StockSN,WarehouseID, SUM(StockQtyBalance) AS StockQtyBalance FROM blog_txstock where ProductID=('%s') AND WarehouseID=('%s') GROUP BY ProductID,WarehouseID"%(ProductID,i))
            DistributorDetails=cursor.fetchone()
            logger.info(DistributorDetails)
            if DistributorDetails !=None:
                id=DistributorDetails[0]
                logger.info(id)
                ProductID=DistributorDetails[1]
                logger.info(ProductID)
                ProductName=DistributorDetails[2]
                logger.info(ProductName)
                StockSN=DistributorDetails[3]
                logger.info(StockSN)
                WarehouseID=DistributorDetails[4]
                logger.info(WarehouseID)
                StockQtyBalance=DistributorDetails[5]
                logger.info(StockQtyBalance)
                balance=int(StockQtyBalance)
                cursor.execute("""INSERT INTO blog_stockcard_result(ProductID,ProductName,WarehouseID,Balance,StockSN) VALUES (%s,%s,%s,%s,%s)""",(ProductID,ProductName,WarehouseID,balance,StockSN))
                #results=txStock.objects.raw("SELECT id,ProductID,ProductName,StockSN,WarehouseID, SUM(StockQtyBalance) AS StockQtyBalance FROM blog_txstock where ProductID=('%s') AND WarehouseID IN(%s) GROUP BY ProductID,WarehouseID"%(ProductID,WarehouseIN))
        return HttpResponseRedirect('/accounts/Viewresult/',{'UserRole':userrole,'full_name':request.user.first_name})
        #return render(request,'StockCardSummuryForSearch.html',{'obj':StockCard_result.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})
        #return render_to_response('StockCardSummuryForSearch.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':results})
    else:
        return render(request, 'StackCardInquiry.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':MsProduct.objects.all(),'Warehouse':WareHouse.objects.all()})
def Stock_Result(request):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
        ProductList = txStock.objects.raw('SELECT id,ProductID,StockSN,ProductName,WarehouseID,Balance FROM blog_stockcard_result GROUP BY ProductID,WarehouseID')
        logger.info("Hi Test")
	return render_to_response('StockCardSummuryForSearch.html',{'obj':ProductList,'full_name':request.user.first_name,'UserRole':userrole})


def Card_Inquiry_Error_label(request):
    Fromdatefrompage=request.GET.get('fromDate')
    logger.info(Fromdatefrompage)
    Todatefrompage=request.GET.get('toDate')
    logger.info(Todatefrompage)
    ProductIDFromPage=request.GET.get('productID')
    logger.info(ProductIDFromPage)
    WareHouseID=request.GET.get('WareHouseID')
    logger.info(WareHouseID)
    ValiationData=''
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(ProductID) FROM blog_txstock WHERE LastUpdateOn BETWEEN  ('%s') AND ('%s') AND ProductID=('%s') AND WarehouseID=('%s')"  %(Fromdatefrompage,Todatefrompage,ProductIDFromPage,WareHouseID))
    Productlist=cursor.fetchone()[0]
    logger.info(Productlist)
    if Productlist ==None:
        ValiationData="No Data Found for the selected dates"
    logger.info(ValiationData)
    return HttpResponse(ValiationData)

def Card_Inquiry_Error_label_With_warehouse(request):
    Fromdatefrompage=request.GET.get('fromDate')
    logger.info(Fromdatefrompage)
    Todatefrompage=request.GET.get('toDate')
    logger.info(Todatefrompage)
    warehouseIDFromPage=request.GET.get('warehouseID')
    ValiationData=''
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(WarehouseID) FROM blog_txstock WHERE LastUpdateOn BETWEEN  ('%s') AND ('%s') AND WarehouseID=('%s')"  %(Fromdatefrompage,Todatefrompage,warehouseIDFromPage))
    Warehouselist=cursor.fetchone()[0]
    logger.info(Warehouselist)
    if Warehouselist ==None:
        ValiationData="No Data Found for the selected dates"
    logger.info(ValiationData)
    return HttpResponse(ValiationData)


def productId_sorting(request):
    ProductId=request.GET.get('productid')
    logger.info(ProductId)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName,PrincipalName from blog_msproduct where ProductID=('%s')" % (ProductId))
    FData=cursor.fetchone()
    logger.info(FData)
    Data=FData[0] + ',' + FData[1]
    logger.info(Data)
    if ProductId:
        c = {
         'Pagedata':Data,
         }
    else:
        ProductId = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)

def Card_Inquiry_Using_Warehouseid(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('prdctID')
    logger.info(ProductID)
    ProductName=request.POST.get('prdctName')
    logger.info(ProductName)
    Warehouse=request.POST.get('warehouse')
    logger.info(Warehouse)
    PrincipleName=request.POST.get('PrncplName')
    logger.info(PrincipleName)
    FromDate=request.POST.get('frmdate')
    logger.info(FromDate)
    ToDate=request.POST.get('Todate')
    logger.info(ToDate)
    if ProductID !=None:
        cursor = connection.cursor()
        cursor.execute("SELECT GROUP_CONCAT(WarehouseID) FROM blog_txstock WHERE LastUpdateOn BETWEEN  ('%s') AND ('%s') AND WarehouseID=('%s') AND ProductID=('%s')"  %(FromDate,ToDate,Warehouse,ProductID))
        warehouselist=cursor.fetchone()[0]
        logger.info(warehouselist)
        if warehouselist==None:
           return render(request, 'StackCardInquirywithwarehouse.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':MsProduct.objects.all(),'Warehouse':WareHouse.objects.all()})
        splitedwarehouselist=",".join("'{0}'".format(i) for i in warehouselist.split(','))
        logger.info(splitedwarehouselist)     
        results=txStock.objects.raw('SELECT id,ProductID,ProductName,WarehouseID, SUM(StockQtyBalance) AS StockQtyBalance FROM blog_txstock where ProductID =%s AND WarehouseID=%s',[ProductID,Warehouse])
        return render_to_response('StockCardSummuryForSearchwarehouse.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':results})
    else:
        return render(request, 'StackCardInquirywithwarehouse.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':MsProduct.objects.all(),'Warehouse':WareHouse.objects.all()})


def warehouseId_sorting(request):
    warehouseID=request.GET.get('warehouseID')
    logger.info(warehouseID)
    ValidationData=''
    Data=''
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(DISTINCT ProductID)  from blog_txstock where WarehouseID=('%s')" % (warehouseID))
    FData=cursor.fetchone()[0]
    logger.info(FData)
    if FData == None:
        Data="No Product ID is available with this wareHouse please select another wareHouse"
    else:
        Data=FData
        logger.info(Data)
        if warehouseID:
            c = {
             'Pagedata':Data,
             }
        else:
            warehouseID = "Nothing"
            c = {
                 'Pagedata':Data,
                 }
            logger.info(c)
    logger.info(Data)
    return HttpResponse(Data)

    
		
	
#----------------------------------------------------------------------Details--------------------------------------------------------------

def ProductID_Details(request):
    DataFromPage=request.GET.get('val')
    logger.info(DataFromPage)
    if MsProduct.objects.filter(ProductID=DataFromPage).count()>0:
        Data="ProductID already exists"
    else:
        Data=None
    if DataFromPage:
        c = {
         'Pagedata':Data,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':Data,
             }
        logger.info(c)
    return HttpResponse(Data)


#------------------------------------------------Receiving SAM Card-------------------------------------------------------------------------

def Add_ReceivingsamCard(request):
    userrole=get_role(request.user.email)
    RSamID=request.POST.get('RSamID')
    WarehouseName=request.POST.get('WarehouseName')
    #RPersoQuantity=request.POST.get('RPersoQuantity')
    #RSamStatus=request.POST.get('RSamStatus')
    RSID=''
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blog_txsetsamcard")
    ProductDetails=cursor.fetchone()
    if ProductDetails!=None:
        ProductID=ProductDetails[1]
        ProductType=ProductDetails[2]
        ProductName=ProductDetails[3]
        ProductModel=ProductDetails[4]
    else:
        return render(request, 'ReceivingSAMCard.html',{'SAMValue':'Yes','Error':'Please Set SAM Card Details','WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
    cursor.execute("select GROUP_CONCAT(SAM_SN) from blog_txsam where ReceivingSAMID =('%s')" %(RSamID))
    SAM_SN=cursor.fetchone()[0]
    logger.info(SAM_SN)
    SAMValue='Yes'
    if RSamID != None or WarehouseName != None:
        SAMValue='Yes'
        SAM_SN=request.POST.get('SAMSN')
        request.session['RID']=RSamID
        RSID=request.session['RID']
        request.session['RWHouse']=WarehouseName
        RSHouse=request.session['RWHouse']
        if request.POST.get('_AddToList'):
            if request.method == 'POST':
                form = TxSAMForm(request.POST.get, request.FILES)
                new_file = TxSAM(ReceivingSAMID=RSamID,
				SAM_SN=request.POST.get('SAMSN'),
                                SAM_UID=request.POST.get('SAMUID'),
                                SAMpinFile = request.FILES.get('docfile', False),
                                SAMpinFileDownload='0', 
                                WarehouseName= WarehouseName,
                                DataExportQty='0',
                                DataExportStatus='No', 
				CreatedOn=CreatedOn,
                                CreatedBy=CreatedBy,
				LastUpdateOn=LastUpdateOn,
                                LastUpdateBy=LastUpdateBy
                                )
		new_file.save()
		RPersoQty=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
                if TxSAM.objects.filter(ReceivingSAMID=RSamID).count()>0:
                    RPersoQuantity=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
                else:
                    RPersoQuantity='0'
                cursor.execute("""INSERT INTO blog_txreceivingsam(ReceivingSAMID,ReceivingPersoQty,WarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s)""",(RSamID,RPersoQuantity,WarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
                if SAM_SN != None:
                    cursor.execute("select id from blog_txsam where ReceivingSAMID =('%s') and SAM_SN =('%s')" %(RSamID,SAM_SN))
                    SAMID=cursor.fetchone()[0]
                    logger.info(SAMID)
                    cursor.execute("""INSERT INTO blog_txstocksn(RefNumber,ProductID,ProductName,ProductType,SerialNumber,SNStatus,SAMRefNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,ProductID,ProductName,ProductType,SAM_SN,'IN',SAMID,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
		return render(request, 'ReceivingSAMCard.html',{'RPersoQty':RPersoQty,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'obj':TxSAM.objects.filter(ReceivingSAMID=RSID),'RSID':RSID,'RSHouse':RSHouse,'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
	    else:
                return render(request, 'ReceivingSAMCard.html',{'RPersoQty':RPersoQty,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'RSID':RSID,'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
        else:
##            if TxSAM.objects.filter(ReceivingSAMID=RSamID).count()>0:
##                RPersoQuantity=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
##            else:
##                RPersoQuantity='0'
##            cursor.execute("""INSERT INTO blog_txreceivingsam(ReceivingSAMID,ReceivingPersoQty,WarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
##            VALUES (%s,%s,%s,%s,%s,%s,%s)""",(RSamID,RPersoQuantity,WarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            if ProductID != None:
                if TxSAM.objects.filter(ReceivingSAMID=RSamID).count()>0:
                    RPersoQuantity=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
                else:
                    RPersoQuantity='0'
                cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,"ReceivingSAM",WarehouseName,ProductID,ProductName,RPersoQuantity,'0',RPersoQuantity,'Yes',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
                
            return render(request, 'ViewReceivingSAMCard.html',{'obj':TxSAM.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})
    else:
        return render(request, 'ReceivingSAMCard.html',{'RSID':RSID,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'SAMValue':SAMValue,'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
            
def View_ReceivingsamCard(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewReceivingSAMCard.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':TxSAM.objects.all()})


def Edit_ReceivingsamCard(request,u_id):
    userrole=get_role(request.user.email)
    SAMList=TxReceivingSAM.objects.raw('SELECT * FROM blog_txreceivingsam where id =%s',[u_id])
    cursor = connection.cursor()
    cursor.execute('SELECT ReceivingSAMID FROM blog_txreceivingsam where id =%s',[u_id])
    ReceivingSAMID=cursor.fetchone()[0]
    logger.info(ReceivingSAMID)
    cursor.execute('SELECT ReceivingPersoQty FROM blog_txreceivingsam where id =%s',[u_id])
    ReceivingPersoQty=cursor.fetchone()[0]
    logger.info(ReceivingPersoQty)
    SAMcount=TxSAM.objects.filter(ReceivingSAMID=ReceivingSAMID).count()
    logger.info(SAMcount)
    cursor.execute("SELECT * FROM blog_txsetsamcard")
    ProductDetails=cursor.fetchone()
    ProductID=ProductDetails[1]
    ProductType=ProductDetails[2]
    ProductName=ProductDetails[3]
    ProductModel=ProductDetails[4]
    if int(SAMcount)<int(ReceivingPersoQty):
        SAMValue='Yes'
    else:
        SAMValue='No'
    for s in SAMList:
        if request.user.username == '':
            return HttpResponseRedirect('/accounts/login/')
	else:
            return render(request, 'EditReceivingSAMCard.html',{'RSamID':s.ReceivingSAMID,
                                                                'uid':u_id,
                                                                       'WarehouseName':s.WarehouseName,                                                                       
                                                                       'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),
                                                                       'samobj':TxSAM.objects.filter(ReceivingSAMID=ReceivingSAMID),
                                                                       'SAMValue':SAMValue,
                                                                       'ProductID':ProductID,
                                                                       'ProductType':ProductType,
                                                                       'ProductName':ProductName,
                                                                       'ProductModel':ProductModel, 
                                                                       'UserRole':userrole,
                                                                       'full_name':request.user.first_name
                                                                        })
def GetSAM_Details(request,u_id):
    userrole=get_role(request.user.email)
    SAMInfoList=TxSAM.objects.raw('SELECT * FROM blog_txsam where id =%s',[u_id])
    cursor = connection.cursor()
    cursor.execute("SELECT ReceivingSAMID FROM blog_txsam where id=('%s')" % (u_id))
    ReceivingSAMID=cursor.fetchone()[0]
    logger.info(ReceivingSAMID)
    cursor.execute("SELECT ProductID FROM blog_txstocksn where RefNumber=('%s')" % (ReceivingSAMID))
    snProductID=cursor.fetchone()[0]
    logger.info(snProductID)
    cursor.execute('SELECT r.id FROM blog_txreceivingsam r,blog_txsam s WHERE r.ReceivingSAMID=s.ReceivingSAMID AND s.id=%s',[u_id])
    samid =  cursor.fetchone()[0]
    logger.info(samid)
    for s in SAMInfoList:
        if request.user.username == '':
            return HttpResponseRedirect('/accounts/login/')
        else:
            return render(request, 'EditSAMDetails.html',{'samid':samid,
                                                        'uid':u_id,
                                                        'RSamID':s.ReceivingSAMID,
                                                        'WarehouseName':s.WarehouseName,
                                                        'SAMSN':s.SAM_SN,
                                                        'SAMUID':s.SAM_UID,
                                                        'docfile':s.SAMpinFile,
                                                        'SNProductID':snProductID,
                                                        'UserRole':userrole,
                                                        'full_name':request.user.first_name
                                                                        })

def Update_ReceivingsamCard(request):
    userrole=get_role(request.user.email)
    samid=request.POST.get('uid')
    RSamID=request.POST.get('RSamID')
    WarehouseName=request.POST.get('WarehouseName')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("select GROUP_CONCAT(SAM_SN) from blog_txsam where ReceivingSAMID =('%s')" %(RSamID))
    SAM_SN=cursor.fetchone()[0]
    logger.info(SAM_SN)
    cursor.execute("SELECT * FROM blog_txsetsamcard")
    ProductDetails=cursor.fetchone()
    ProductID=ProductDetails[1]
    ProductType=ProductDetails[2]
    ProductName=ProductDetails[3]
    ProductModel=ProductDetails[4]
    RPersoQty=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
    if TxSAM.objects.filter(ReceivingSAMID=RSamID).count()>0:
        RPersoQuantity=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
    else:
        RPersoQuantity='0'
    cursor.execute("""UPDATE blog_txreceivingsam SET ReceivingPersoQty=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(RPersoQuantity,LastUpdateOn,LastUpdateBy,samid))
    cursor.execute("""UPDATE  blog_txstocksn SET SerialNumber=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE SAMRefNumber=%s""",
            (SAM_SN,LastUpdateOn[:10],LastUpdateBy,RSamID))
    #cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                #VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,"ReceivingSAM",WarehouseName,ProductID,ProductName,RPersoQuantity,'0',RPersoQuantity,'Yes',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
        #cursor.execute("""UPDATE blog_txsam_txstock SET StockQtyIN=%s WHERE id=%s""",
	#(RPersoQuantity,samid))
    return HttpResponseRedirect('/accounts/ViewReceivingSamCard/',{'UserRole':userrole,'full_name':request.user.first_name})

def Update_SAMDetails(request):
    userrole=get_role(request.user.email)
    saminfoid=request.POST.get('uid')
    RSamID=request.POST.get('RSamID')
    WarehouseName=request.POST.get('WarehouseName')
    request.session['RID']=RSamID
    RSID=request.session['RID']
    request.session['RWHouse']=WarehouseName
    RSHouse=request.session['RWHouse']
    SAMSN=request.POST.get('SAMSN')
    logger.info(SAMSN)
    SAMUID=request.POST.get('SAMUID')
    logger.info(SAMUID)
    SAMpinFile = request.FILES.get('docfile', False)
    logger.info(SAMpinFile)
    samid=request.POST.get('samid')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    RPersoQty=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blog_txsetsamcard")
    ProductDetails=cursor.fetchone()
    if ProductDetails!=None:
        ProductID=ProductDetails[1]
        ProductType=ProductDetails[2]
        ProductName=ProductDetails[3]
        ProductModel=ProductDetails[4]
    if SAMpinFile != False:
        cursor.execute("SELECT SAMpinFileDownload  FROM blog_txsam where ReceivingSAMID=('%s') and SAM_SN=('%s')" % (RSamID,SAMSN))
        DQty=cursor.fetchone()[0]
        logger.info(DQty)
        if request.method == 'POST':
                form = TxSAMForm(request.POST.get, request.FILES)
                new_updatefile = TxSAM(ReceivingSAMID=RSamID,
                                SAM_SN=request.POST.get('SAMSN'),
                                SAM_UID=request.POST.get('SAMUID'),
                                SAMpinFile = request.FILES.get('docfile', False),
                                SAMpinFileDownload=DQty,
                                WarehouseName= WarehouseName,
                                DataExportQty='0',
                                DataExportStatus='No',
                                CreatedOn=CreatedOn,
                                CreatedBy=CreatedBy,
				LastUpdateOn=LastUpdateOn,
                                LastUpdateBy=LastUpdateBy,
                                id=saminfoid
                                )
		new_updatefile.save()
    else:
        cursor.execute("""UPDATE blog_txsam SET SAM_SN=%s,SAM_UID=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
        (SAMSN,SAMUID,LastUpdateOn,LastUpdateBy,saminfoid))
    cursor.execute("""UPDATE blog_txstocksn SET SerialNumber=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE RefNumber=%s and SAMRefNumber=%s""",
                   (SAMSN,LastUpdateOn[:10],LastUpdateBy,RSamID,saminfoid))
    return HttpResponseRedirect('/accounts/ViewReceivingSamCard/',{'UserRole':userrole,'full_name':request.user.first_name,'obj':TxSAM.objects.all()})


def SAMFileClick_Details(request):
    samid=request.GET.get('samid')
    uid=request.GET.get('uid')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("SELECT SAMpinFileDownload  FROM blog_txsam where id=('%s')" % (uid))
    DQty=cursor.fetchone()[0]
    SAMPINFileDownload=int(DQty)+1
    cursor.execute("""UPDATE blog_txsam SET SAMpinFileDownload=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(SAMPINFileDownload,LastUpdateOn,LastUpdateBy,uid))
    data="Sucess"
    return HttpResponse(data)

def GetSAMDuplicate_Details(request):
    SAMSN=request.GET.get('SAMSN')
    SAMUID=request.GET.get('SAMUID')
    ValidationData=''
    if SAMSN != None:
        if TxSAM.objects.filter(SAM_SN=SAMSN).count()>0:
            ValidationData='Data with same Serial Number already exist, please check again'
    if SAMUID != None:
        if TxSAM.objects.filter(SAM_UID=SAMUID).count()>0:
            ValidationData='Data with same UID already exist, please check again'
    return HttpResponse(ValidationData)
    
def SAMInsertUpdate_Details(request):
    RSamID=request.GET.get('RSamID')
    SAMSN=request.GET.get('SAMSN')
    SAMUID=request.GET.get('SAMUID')
    SAMPCID=request.GET.get('SAMPCID')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    ValidationData=''
    getdata=''
    
    if SAMSN =='':
        ValidationData='Please Enter SAM SerialNumber'
    elif SAMUID =='':
        ValidationData='Please Enter SAM UID'
    elif SAMPCID =='':
        ValidationData='Please Enter SAM PCID'
    elif TxSAM.objects.filter(SAM_SN=SAMSN).count()>0:
        ValidationData='Data with same Serial Number already exist, please check again'
    elif TxSAM.objects.filter(SAM_UID=SAMUID).count()>0:
        ValidationData='Data with same UID already exist, please check again'
    elif TxSAM.objects.filter(SAM_PCID=SAMPCID).count()>0:
        ValidationData='Data with same PCID already exist, please check again'
    else:
        cursor.execute("""INSERT INTO blog_txsam(ReceivingSAMID,SAM_SN,SAM_UID,SAM_PCID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,SAMSN,SAMUID,SAMPCID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        obj = TxSAM.objects.filter(ReceivingSAMID=RSamID).values_list('SAM_SN', 'SAM_UID', 'SAM_PCID')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)

def SAMInsert_Details(request):
    RSamID=request.GET.get('RSamID')
    RPersoQuantity=request.GET.get('RPersoQuantity')
    logger.info(RPersoQuantity)
    SAMSN=request.GET.get('SAMSN')
    SAMUID=request.GET.get('SAMUID')
    SAMPCID=request.GET.get('SAMPCID')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    ValidationData=''
    getdata=''
    
    if SAMSN =='':
        ValidationData='Please Enter SAM SerialNumber'
    elif SAMUID =='':
        ValidationData='Please Enter SAM UID'
    elif SAMPCID =='':
        ValidationData='Please Enter SAM PCID'
    elif TxSAM.objects.filter(SAM_SN=SAMSN).count()>0:
        ValidationData='Data with same Serial Number already exist, please check again'
    elif TxSAM.objects.filter(SAM_UID=SAMUID).count()>0:
        ValidationData='Data with same UID already exist, please check again'
    elif TxSAM.objects.filter(SAM_PCID=SAMPCID).count()>0:
        ValidationData='Data with same PCID already exist, please check again'
    else:
        SAMcount=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
        logger.info(SAMcount)
        if int(RPersoQuantity)<=int(SAMcount):
            ValidationData='You cannot add another new SAM record due to it has reached the Receiving Perso Quantity number,Please set Receiving Status into Received'
        else:
            cursor.execute("""INSERT INTO blog_txsam(ReceivingSAMID,SAM_SN,SAM_UID,SAM_PCID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,SAMSN,SAMUID,SAMPCID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            obj = TxSAM.objects.filter(ReceivingSAMID=RSamID).values_list('SAM_SN', 'SAM_UID', 'SAM_PCID')
            getdata = json.dumps(list(obj))
            logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)


#------------------------------------------------InputStock-------------------------------------------------

def ProductName_Details(request):
    DataFromPage=request.GET.get('ProductID')
    logger.info(DataFromPage)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName  FROM blog_msproduct where ProductID=('%s')" % (DataFromPage))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    cursor.execute("SELECT ProductSerialNumber FROM blog_msproduct WHERE ProductID=('%s')" % (DataFromPage))
    ProductSN=cursor.fetchone()[0]
    logger.info(ProductSN)
    Data=ProductName + ',' + ProductSN
    if DataFromPage:
        c = {
         'Pagedata':ProductName,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':ProductName,
             }
        logger.info(c)
    return HttpResponse(Data)

def ProductID_Details(request):
    DataFromPage=request.GET.get('ProductID')
    logger.info(DataFromPage)
    PONumber=request.GET.get('PONumber')
    logger.info(PONumber)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName,Quantity,EstimatedDeliveryDate  FROM blog_txpurchaseorderdtl where ProductId=('%s') and PONumber=('%s')" % (DataFromPage,PONumber))
    PDetails=cursor.fetchone()
    logger.info(PDetails)
    Data=PDetails[0] + ',' + PDetails[1] + ',' + str(PDetails[2])
    return HttpResponse(Data)

def SNInputStock_Details(request):
    ProductID=request.GET.get('ProductID')
    ProductName=request.GET.get('ProductName')
    SerialNumber=request.GET.get('SerialNumber')
    logger.info(SerialNumber)
    RefNumber=request.GET.get('RefNumber')
    cursor = connection.cursor()
    cursor.execute("select ProductType from blog_msproduct where ProductID=('%s')"%(ProductID))
    ProductType=cursor.fetchone()[0]
    logger.info(ProductType)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    ValidationData=''
    getdata=''
    if SerialNumber == '':
        ValidationData='Please Enter Serial Number'
    elif TxStockSN.objects.filter(SerialNumber=SerialNumber).count()>0:
        ValidationData='Data has already been added previously'
    else:
        cursor.execute("""INSERT INTO blog_txstocksn(ProductID,RefNumber,ProductName,ProductType,SerialNumber,SNStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (ProductID,RefNumber,ProductName,ProductType,SerialNumber,'IN',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
        #cursor.execute("""INSERT INTO blog_txinput_txstocksn(ProductID,RefNumber,ProductName,ProductType,SN,SNStatus) VALUES (%s,%s,%s,%s,%s,%s)""",
                  # (ProductID,RefNumber,ProductName,ProductType,SerialNumber,'IN'))
        obj=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)
    
def SNInputDeleteCheck_Details(request):
    RefNumber=request.GET.get('RefNumber')
    ProductID=request.GET.get('ProductID')
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(SerialNumber) from blog_txstocksn where ProductID=('%s') AND InputStockRefNumber=('%s')" % (ProductID,RefNumber))
    #cursor.execute("SELECT GROUP_CONCAT(SN) from blog_txinput_txstocksn where ProductID=('%s') AND RefNumber=('%s')" % (ProductID,RefNumber))
    SerialNumbersList=cursor.fetchone()[0]
    logger.info(SerialNumbersList)
    myList = [x for x in SerialNumbersList.split(',') if x]
    logger.info(myList)
    TxStockSN.objects.filter(SerialNumber__in=(myList)).delete()
    obj=TxStockSN.objects.filter(ProductID=ProductID).filter(InputStockRefNumber=RefNumber).values_list('SerialNumber')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)

def EditInputSN_View(request,SN):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT id from blog_txstocksn where SerialNumber =('%s')" % (SN))
    data =  cursor.fetchone()[0]
    logger.info(data)
    return render(request, 'EditInputSerialNumber.html',{'lblSN':data,'SerialNumber':SN,'UserRole':userrole,'full_name':request.user.first_name})

def InputSNUpdate_Details(request):
    SNumber=request.GET.get('SNumber')
    lblSN=request.GET.get('lblSN')
    ProductID=request.GET.get('ProductID')
    RefNumber=request.GET.get('RefNumber')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    ValidationData=''
    getdata=''
    if TxStockSN.objects.filter(SerialNumber=SNumber).count() > 0:
        ValidationData='Data has already been added please check it again'
    else:
        cursor.execute("""UPDATE blog_txstocksn SET SerialNumber=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  id=%s""",(SNumber,LastUpdateOn[:10],LastUpdateBy,lblSN))
        obj=TxStockSN.objects.filter(ProductID=ProductID).filter(InputStockRefNumber=RefNumber).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)
    
def DeleteInputSN_View(request,SN):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT id from blog_txstocksn where SerialNumber =('%s')" % (SN))
    data =  cursor.fetchone()[0]
    logger.info(data)
    return render(request, 'DeleteInputSerialNumber.html',{'SNid':data,'SN':SN,'UserRole':userrole,'full_name':request.user.first_name})

def InputSNDelete_Details(request):
    SN=request.GET.get('SN')
    SNid=request.GET.get('SNid')
    ProductID=request.GET.get('ProductID')
    RefNumber=request.GET.get('RefNumber')
    TxStockSN.objects.filter(ProductID=ProductID).filter(InputStockRefNumber=RefNumber).filter(SerialNumber=SN).filter(id=SNid).delete()
    obj=TxStockSN.objects.filter(ProductID=ProductID).filter(InputStockRefNumber=RefNumber).values_list('SerialNumber')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)


def AddInputStock_View(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('ProductID')
    RefNumber=request.POST.get('RefNumber')
    ProductName=request.POST.get('ProductName')
    RefTransaction=request.POST.get('RefTransaction')
    WareHouseName=request.POST.get('WareHouseName')
    Status=request.POST.get('Status')
    StockQty=request.POST.get('StockQty')
    logger.info(StockQty)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if RefNumber != None and ProductID != None:
        if StockQty !='':
            StockSN='No'
        else:
            StockSN='Yes'
            StockQty=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).count()
            logger.info(StockQty)
        if request.POST.get('_Save&Send'):
            Status='Stored'
            cursor.execute("""INSERT INTO blog_txinputstock(InputStockID,RefTransaction,ProductID,ProductName,InputStockQty,StockSN,InputStockStatus,WarehouseID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,ProductID,ProductName,StockQty,StockSN,Status,WareHouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,InputStockStatus,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,WareHouseName,ProductID,ProductName,Status,StockQty,'0',StockQty,StockSN,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
            #cursor.execute("""INSERT INTO blog_txinput_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,InputStockStatus,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN)
            #VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,WareHouseName,ProductID,ProductName,Status,StockQty,'0',StockQty,StockSN))
        else:
            cursor.execute("""INSERT INTO blog_txinputstock(InputStockID,RefTransaction,ProductID,ProductName,InputStockQty,StockSN,InputStockStatus,WarehouseID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,ProductID,ProductName,StockQty,StockSN,Status,WareHouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            #cursor.execute("""INSERT INTO blog_txinput_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,InputStockStatus,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN)
           # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,WareHouseName,ProductID,ProductName,Status,StockQty,'0',StockQty,StockSN))
        return render(request, 'ViewInputStock.html',{'obj':TxInputStock.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})
    else:
        return render(request, 'AddInputStock.html',{'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WareHouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})

def View_InputStock(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewInputStock.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':TxInputStock.objects.all()})


def Edit_InputStock(request,u_id):
    userrole=get_role(request.user.email)
    InputStockList=TxInputStock.objects.raw('SELECT * FROM blog_txinputstock where id =%s',[u_id])
    for i in InputStockList:
        count=TxStockSN.objects.filter(RefNumber=i.InputStockID).filter(ProductID=i.ProductID).count()
        cursor = connection.cursor()
        cursor.execute("SELECT ProductSerialNumber from blog_msproduct where ProductID =('%s')" % (i.ProductID))
        ProductSN =  cursor.fetchone()[0]
        logger.info(ProductSN)
        if request.user.username == '':
            return HttpResponseRedirect('/accounts/login/')
	else:
            return render(request, 'EditInputStock.html',{'lblIS':u_id,
                                                        'ProductID':i.ProductID,
                                                        'RefNumber':i.InputStockID,  
                                                        'ProductName':i.ProductName,
                                                        'RefTransaction':i.RefTransaction,
                                                        'WHName':i.WarehouseID,
                                                        'Status':i.InputStockStatus,
                                                        'StockQty':i.InputStockQty,
                                                        'count':count,
                                                        'ProductSN':ProductSN,
                                                        'WareHouseName':WareHouse.objects.filter(WarehouseStatus='Active'),
                                                        'obj':TxStockSN.objects.filter(ProductID=i.ProductID).filter(RefNumber=i.InputStockID),
                                                        'UserRole':userrole,
                                                        'full_name':request.user.first_name
                                                                        })

def Update_InputStock(request):
    userrole=get_role(request.user.email)
    lblIS=request.POST.get('lblIS')
    ProductID=request.POST.get('ProductID')
    RefNumber=request.POST.get('RefNumber')
    RefTransaction=request.POST.get('RefTransaction')
    WareHouseName=request.POST.get('WareHouseName')
    ProductName=request.POST.get('ProductName')
    Status=request.POST.get('Status')
    StockQty=request.POST.get('StockQty')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if request.POST.get('_Save&Send'):
        Status='Stored'
        StockSN='No'
        if StockQty !=None:
            StockQty=request.POST.get('StockQty')
        if TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).count() > 0:
            StockQty=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).count()
            StockSN='Yes'
        cursor.execute("""UPDATE blog_txinputstock SET WarehouseID=%s,InputStockQty=%s,InputStockStatus=%s,StockSN=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(WareHouseName,StockQty,Status,StockSN,LastUpdateOn,LastUpdateBy,lblIS))
        if txStock.objects.filter(RefNumber=RefNumber).filter(ProductID=ProductID).count() == 0:
            cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,InputStockStatus,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,WareHouseName,ProductID,ProductName,Status,StockQty,'0',StockQty,StockSN,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
        else:
            cursor.execute("""UPDATE blog_txstock SET WarehouseID=%s,InputStockStatus=%s,StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s,StockSN=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
            (WareHouseName,Status,StockQty,'0',StockQty,StockSN,LastUpdateOn[:10],LastUpdateBy,lblIS))
    else:
        Status='Progress'
        StockSN='No'
        if TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).count() > 0:
            StockQty=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).count()
            StockSN='Yes'
        logger.info(StockQty)
        cursor.execute("""UPDATE blog_txinputstock SET InputStockQty=%s,WarehouseID=%s,InputStockStatus=%s,StockSN=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(StockQty,WareHouseName,Status,StockSN,LastUpdateOn,LastUpdateBy,lblIS))
        #cursor.execute("""UPDATE blog_txinput_txstock SET WarehouseID=%s,InputStockStatus=%s,StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s,StockSN=%s WHERE id=%s""",
	#(WareHouseName,Status,StockQty,'0',StockQty,StockSN,lblIS))
    return render_to_response('ViewInputStock.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':TxInputStock.objects.all()})

#def SNInputCount_Details(request):
    #ProductID=request.GET.get('val')
    #logger.info(ProductID)
    #Data=''
    #if TxInputStock.objects.filter(ProductID=ProductID).count()>0:
        #Data="Product Already Exist Please Go to Edit and Update It"
    #return HttpResponse(Data)
    
#------------------------------------------------------HandOverMaterial-----------------------------------------------------------------------------------

def MaterialList_Details(request):
    ProductID=request.GET.get('ProductID')
    ValidationData=''
    getdata=''
    if MsBOMDetail.objects.filter(ProductID=ProductID).count()==0:
        ValidationData='Please check materials are not added for this Goods'
    else:
        obj=MsBOMDetail.objects.filter(ProductID=ProductID).values_list('MaterialCode', 'MaterialName', 'MaterialQty')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)

def SAMSNTest_Details(request):
    SAMSN=request.GET.get('val')
    ProductID=request.GET.get('ProductID')
    cursor = connection.cursor()
    Data=''
    SAMPINFile=''
    SAMUID=''
    if TxSAM.objects.filter(SAM_SN=SAMSN).count()>0:
        if TxHandOverMaterialHdr.objects.filter(SAM_SN=SAMSN).count() >0:
            Data='SAM_SN is not available or already used by another Device / Product_SN, please check again'
        else:
            cursor.execute("SELECT ReceivingSAMID FROM  blog_txsam WHERE SAM_SN=('%s')" % (SAMSN))
            RecevingSAMID=cursor.fetchone()[0]
            logger.info(RecevingSAMID)
            if TxStockSN.objects.filter(RefNumber=RecevingSAMID).filter(SerialNumber=SAMSN).count()>0:
                cursor.execute("SELECT SAMpinFile FROM  blog_txsam WHERE SAM_SN=('%s') and ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
                SAMPINFile=cursor.fetchone()[0]
                logger.info(SAMPINFile)
                cursor.execute("SELECT SAM_UID FROM  blog_txsam WHERE SAM_SN=('%s') and ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
                SAMUID=cursor.fetchone()[0]
                logger.info(SAMUID)
    else:
        Data='SAM_SN is not available or already used by another Device / Product_SN, please check again'
    getdata=Data + ':' + SAMPINFile + ':' + SAMUID
    return HttpResponse(getdata)

def ProductSNTest_Details(request):
    ProductSN=request.GET.get('val')
    Data=''
    cursor = connection.cursor()
    if TxHandOverMaterialHdr.objects.filter(Product_SN=ProductSN).count() >0:
        if TxStockSN.objects.filter(SerialNumber=ProductSN).count()>0:
            Data='Product SN already exist (it is duplicate), please insert another Product Serial Number'
    else:
        Data=''
    return HttpResponse(Data)

def AndroidValidation_Details(request):
    Android=request.GET.get('val')
    Data=''
    cursor = connection.cursor()
    if TxSAM.objects.filter(AndriodID=Android).count() >0:
            Data='Android is already exist (it is duplicate), please insert another Android ID'
    else:
        Data=''
    return HttpResponse(Data)


def Material_Details_Validation(request):
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    Data=''
    ValidationData=''
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(MaterialCode) FROM blog_msbomdetail WHERE ProductID=('%s')" % (ProductID))
    MaterialCodes=cursor.fetchone()[0]
    logger.info(MaterialCodes)
    MaterialCodesList = MaterialCodes.split(",")
    logger.info(MaterialCodesList)
    for i in MaterialCodesList:
        logger.info(i)
        cursor.execute("SELECT GROUP_CONCAT(WarehouseID) FROM blog_txstock WHERE ProductID=('%s')" % (i))
        WarehouseName=cursor.fetchone()[0]
        logger.info(WarehouseName)
        if WarehouseName !=None:
            cursor.execute("SELECT InputWarehouseName FROM blog_txwarehouseforproduction")
            InputWarehouseName=cursor.fetchone()[0]
            logger.info(InputWarehouseName)
            if InputWarehouseName in WarehouseName:
                logger.info("Warehouse Exist")
                cursor.execute("SELECT SUM(StockQtyBalance) FROM blog_txstock WHERE ProductID=('%s') AND WarehouseID=('%s')" % (i,InputWarehouseName))
                StockQtyBalance=cursor.fetchone()[0]
                StockQty=int(StockQtyBalance)
                logger.info(StockQty)
                cursor.execute("SELECT MaterialQty FROM blog_msbomdetail WHERE MaterialCode=('%s')" % (i))
                MaterialQuantity=cursor.fetchone()[0]
                logger.info(MaterialQuantity)
                if int(MaterialQuantity)>StockQty:
                    logger.info(MaterialQuantity)
                    logger.info(StockQty)
                    ValidationData="SAM Serial Number and/or Material used in this transaction are not available in the predefined Warehouse, please check again and make sure Warehouse has enough quantity"
                    logger.info(ValidationData)
        else:
            ValidationData='Material used in here not available, make sure to put the stock'
    Data=ValidationData
    logger.info(Data)
    return HttpResponse(Data)

def ADDHOM_View(request):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    now=datetime.now()
    GMonth=str(now)[8:10]
    GYear=str(now)[2:4]
    if TxHandOverMaterialHdr.objects.all().count() ==0:
        PSeq='0001'
    else:
        cursor.execute("SELECT ProductionID FROM blog_txhandovermaterialhdr ORDER BY id DESC LIMIT 1")
        ProID=cursor.fetchone()[0]
        PCount=int(ProID[8:]) + 1
        PSeq=str(PCount).zfill(4)
    logger.info(PSeq)
    ProductionID='PROD' + GMonth + GYear + PSeq
    RefNumber=ProductionID + '00'
    logger.info(RefNumber)
    PID=request.POST.get('PID')
    PName=request.POST.get('PName')
    PModel=request.POST.get('PModel')
    ProSN=request.POST.get('ProSN')
    SAMSN=request.POST.get('SAMSN')
    logger.info(SAMSN)
    SIMSN=request.POST.get('SIMSN')
    logger.info(SIMSN)
    PStatus=request.POST.get('PStatus')
    AndriodID=request.POST.get('AndriodID')
    if SAMSN=='':
        SAMSN=SIMSN
    CreatedOn=str(now)[:10]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:10]
    LastUpdateBy=request.user.first_name
    cursor.execute("SELECT * FROM blog_txsetsamcard")
    ProductDetails=cursor.fetchone()
    if ProductDetails!=None:
        ProductID=ProductDetails[1]
        ProductType=ProductDetails[2]
        ProductName=ProductDetails[3]
        ProductModel=ProductDetails[4]
    else:
        return render(request, 'AddHandOverMaterial.html',{'Error':'Please set SAM Card details','ProductionID':ProductionID,'PType':MsBOMHeader.objects.filter(ProductStatus='Active'),'CreatedOn':CreatedOn[:10],'CreatedBy':CreatedBy,'LastUpdateBy':LastUpdateBy,'LastUpdateOn':LastUpdateOn[:10],'UserRole':userrole,'full_name':request.user.first_name})
    StartPDate=CreatedOn[:10]
    logger.info(StartPDate)
    if  ProductionID!= None and PID != None:
        cursor.execute("""INSERT INTO blog_txhandovermaterialhdr(ProductionID,RefNumber,ProductID,ProductName,ProductModel,Product_SN,SAM_SN,AndriodID,StartProductionDate,ProductionStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductionID,RefNumber,PID,PName,PModel,ProSN,SAMSN,AndriodID,StartPDate,PStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        cursor.execute("SELECT ReceivingSAMID FROM  blog_txsam WHERE SAM_SN=('%s')" % (SAMSN))
        RecevingSAMID=cursor.fetchone()[0]
        logger.info(RecevingSAMID)
        cursor.execute("""UPDATE blog_txsam SET Product_SN=%s,AndriodID=%s,DataExportStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ReceivingSAMID=%s and SAM_SN=%s""",
	(ProSN,AndriodID,'No',LastUpdateOn,LastUpdateBy,RecevingSAMID,SAMSN))
        if MsBOMDetail.objects.filter(ProductID=PID).count()>0:
            cursor.execute("select GROUP_CONCAT(id) from blog_msbomdetail where ProductID =('%s')" %(PID))
            Materialid=cursor.fetchone()[0]            
            MaterialList=Materialid.split(',')
            for i in MaterialList:
                cursor.execute("select MaterialCode,MaterialName,MaterialQty from blog_msbomdetail where id =('%s')" %(i))
                Materialdetails=cursor.fetchall()[0]
                MaterialCode=Materialdetails[0]
                MaterialName=Materialdetails[1]                
                MaterialQty=Materialdetails[2]            
                if TxHandOverMaterialDtl.objects.filter(ProductionID=ProductionID).count() ==0:
                    RefMaterial='01'
                    RefNumber=ProductionID + RefMaterial                    
                else:
                    cursor.execute("SELECT RefNumber FROM blog_txhandovermaterialdtl ORDER BY id DESC LIMIT 1")
                    RefID=cursor.fetchone()[0]
                    logger.info(RefID)
                    PCount=int(RefID[12:]) + 1
                    logger.info(PCount)
                    RefMaterial=str(PCount).zfill(2)
                    logger.info(RefMaterial)
                    RefNumber=ProductionID + RefMaterial
                    logger.info(RefNumber)
                cursor.execute("""INSERT INTO blog_txhandovermaterialdtl(ProductionID,RefNumber,MaterialCode,MaterialName,MaterialQty,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductionID,RefNumber,MaterialCode,MaterialName,MaterialQty,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return render_to_response('ViewHOM.html',{'UserRole':userrole,'obj':TxHandOverMaterialHdr.objects.all(),'full_name':request.user.first_name})    
    else:
        return render(request, 'AddHandOverMaterial.html',{'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'ProductionID':ProductionID,'PType':MsBOMHeader.objects.filter(ProductStatus='Active'),'CreatedOn':CreatedOn[:10],'CreatedBy':CreatedBy,'LastUpdateBy':LastUpdateBy,'LastUpdateOn':LastUpdateOn[:10],'UserRole':userrole,'full_name':request.user.first_name})

            
            

def View_HOM(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
    else:
	    return render_to_response('ViewHOM.html',{'UserRole':userrole,'obj':TxHandOverMaterialHdr.objects.all(),'full_name':request.user.first_name})

def EditHOM_View(request,u_id):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blog_txsetsamcard")
    ProductDetails=cursor.fetchone()
    ProID=ProductDetails[1]
    ProType=ProductDetails[2]
    ProName=ProductDetails[3]
    ProModel=ProductDetails[4]
    results = TxHandOverMaterialHdr.objects.raw("SELECT * FROM blog_txhandovermaterialhdr WHERE id=('%s')"%(u_id))
    for h in results:
        cursor.execute("SELECT AndriodID FROM  blog_txsam WHERE SAM_SN=('%s')" % (h.SAM_SN))
        AndriodID=cursor.fetchone()[0]
        cursor.execute("SELECT SAMpinFile FROM  blog_txsam WHERE SAM_SN=('%s')" % (h.SAM_SN))
        SAMpinFile=cursor.fetchone()[0]
        return render(request, 'EditHOM.html',{'obj':MsBOMDetail.objects.filter(ProductID=h.ProductID),
                                                         'HOverID':h.ProductionID,
                                                         'ProductID':h.ProductID,
                                                         'ProductName':h.ProductName,
                                                         'ProductModel':h.ProductModel,
                                                         'ProSN':h.Product_SN,
                                                         'SAMSN':h.SAM_SN,
                                                         'StartPDate':h.StartProductionDate,
                                                         'PStatus':h.ProductionStatus,
                                                         'AndriodID': AndriodID,
                                                         'docfile': SAMpinFile,  
                                                         'CreatedOn':h.CreatedOn,
                                                         'CreatedBy':h.CreatedBy,
                                                         'LastUpdateBy':h.LastUpdateBy,
                                                         'LastUpdateOn':h.LastUpdateOn,
                                                         'uid':u_id,
                                                         'ProID':ProID,
                                                         'ProType':ProType,
                                                         'ProName':ProName,
                                                         'ProModel':ProModel,  
                                                         'UserRole':userrole,
                                                         'full_name':request.user.first_name
                                                         })

def UpdateHOM_View(request):
    userrole=get_role(request.user.email)
    hid=request.POST.get('uid')
    ProSN=request.POST.get('ProSN')
    SAMSN=request.POST.get('SAMSN')
    SIMSN=request.POST.get('SIMSN')
    AndriodID=request.POST.get('AndriodID')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    if SAMSN=='':
        SAMSN=SIMSN
        logger.info(SAMSN)
    cursor = connection.cursor()
    cursor.execute("""UPDATE blog_txhandovermaterialhdr SET Product_SN=%s,SAM_SN=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
	(ProSN,SAMSN,LastUpdateOn,LastUpdateBy,hid))
    cursor.execute("""UPDATE blog_txsam SET AndriodID=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  SAM_SN=%s""",
	(AndriodID,LastUpdateOn,LastUpdateBy,SAMSN))
    return render_to_response('ViewHOM.html',{'UserRole':userrole,'obj':TxHandOverMaterialHdr.objects.all(),'full_name':request.user.first_name})


def SAMHOMFileClick_Details(request):
    SAMSN=request.GET.get('SAMSN')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("SELECT ReceivingSAMID FROM  blog_txsam WHERE SAM_SN=('%s')" % (SAMSN))
    RecevingSAMID=cursor.fetchone()[0]
    logger.info(RecevingSAMID)
    cursor.execute("Select SAMpinFile FROM blog_txsam WHERE SAM_SN=('%s') and ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
    PINFile=cursor.fetchone()[0]
    logger.info(PINFile)
    f = open('/opt/BIMSDevelopment/Production/BCAT/AssetManagment/blog/static/files/'+PINFile,'r')
    myfile = File(f)
    testfile=myfile.read()
    logger.info(testfile)
    SamPinFileName=testfile.replace('samPin=','')
    logger.info(SamPinFileName)
    myfile.close()
    cursor.execute("SELECT SAMpinFileDownload  FROM blog_txsam where ReceivingSAMID=('%s')" % (RecevingSAMID))
    DQty=cursor.fetchone()[0]
    SAMpinFileDownload=int(DQty)+1
    cursor.execute("""UPDATE blog_txsam SET SAMpinFileDownload=%s,SAMPIN=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ReceivingSAMID=%s and SAM_SN=%s""",
	(SAMpinFileDownload,SamPinFileName,LastUpdateOn,LastUpdateBy,RecevingSAMID,SAMSN))
    #cursor.execute("SELECT Product_SN FROM  blog_txsam WHERE SAM_SN=('%s') and  ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
    #ProductSN=cursor.fetchone()[0]
    #logger.info(ProductSN)
    #if ProductSN !=None:
        #cursor.execute("""UPDATE blog_txsam SET DataExportStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ReceivingSAMID=%s and SAM_SN=%s""",
	#('Yes',LastUpdateOn,LastUpdateBy,RecevingSAMID,SAMSN))
    data="Sucess"
    return HttpResponse(data)
    

#------------------------------------------------------Set WareHouse----------------------------------------------

def WarehouseName_Details(request):
    WarehouseID=request.GET.get('WarehouseID')
    cursor = connection.cursor()
    cursor.execute("SELECT WarehouseName  FROM blog_warehouse where WarehouseID=('%s')" % (WarehouseID))
    WarehouseName=cursor.fetchone()[0]
    return HttpResponse(WarehouseName)

def SaveWareHouseClick_Details(request):
    MWarehouseID=request.GET.get('MWarehouseID')
    MWarehouseName=request.GET.get('MWarehouseName')
    FGWarehouseID=request.GET.get('FGWarehouseID')
    logger.info(FGWarehouseID)
    FGWarehouseName=request.GET.get('FGWarehouseName')
    RNumber=randint(001, 9999)
    ProdWarehouseNo='ProWH' + str(RNumber)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    ValidationData=''
    if MWarehouseID =='':
        ValidationData='Please Select InputWareHouseID'
    elif FGWarehouseID =='':
        ValidationData='Please Select OutputWareHouseID'
    else:
        ValidationData='Sucess'
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO blog_txwarehouseforproduction(ProdWarehouseNo,InputWarehouseID,InputWarehouseName,OutputWarehouseID,OutputWarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProdWarehouseNo,MWarehouseID,MWarehouseName,FGWarehouseID,FGWarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
    return HttpResponse(ValidationData)

def UpdateWareHouseClick_Details(request):
    MWarehouseID=request.GET.get('MWarehouseID')
    MWarehouseName=request.GET.get('MWarehouseName')
    FGWarehouseID=request.GET.get('FGWarehouseID')
    FGWarehouseName=request.GET.get('FGWarehouseName')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    ValidationData=''
    if MWarehouseID =='':
        ValidationData='Please Select InputWareHouseID'
    elif FGWarehouseID =='':
        ValidationData='Please Select OutputWareHouseID'
    else:
        ValidationData='Sucess'
        cursor.execute("""UPDATE blog_txwarehouseforproduction SET InputWarehouseID=%s,InputWarehouseName=%s,OutputWarehouseID=%s,OutputWarehouseName=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE id=%s""",
        (MWarehouseID,MWarehouseName,FGWarehouseID,FGWarehouseName,LastUpdateOn,LastUpdateBy,'1'))
    return HttpResponse(ValidationData)


def SetWareHouse_View(request):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    if TxWarehouseForProduction.objects.all().count()>0:
        cursor.execute("SELECT InputWarehouseID,InputWarehouseName,OutputWarehouseID,OutputWarehouseName  FROM blog_txwarehouseforproduction")
        WHDetails=cursor.fetchone()
        InputWarehouseID=WHDetails[0]
        InputWarehouseName=WHDetails[1]
        OutputWarehouseID=WHDetails[2]
        OutputWarehouseName=WHDetails[3]
        WHValue='YES'
        return render(request, 'WarehouseProduction.html',{'WHValue':WHValue,'InputWarehouseID':InputWarehouseID,'InputWarehouseName':InputWarehouseName,'OutputWarehouseID':OutputWarehouseID,'OutputWarehouseName':OutputWarehouseName,'UserRole':userrole,'obj':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})        
    else:
        WHValue='NO'
        return render(request, 'WarehouseProduction.html',{'WHValue':WHValue,'UserRole':userrole,'obj':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})



#-----------------------------------------------------Set SAMCard-----------------------------------------------------


def ProductSAM_Details(request):
    ProductID=request.GET.get('ProductID')
    cursor = connection.cursor()
    cursor.execute("SELECT ProductType,ProductName,ProductModel,ProductStatus  FROM blog_msproduct where ProductID=('%s')" % (ProductID))
    ProductDetails=cursor.fetchone()
    Data=ProductDetails[0] + ',' + ProductDetails[1] + ',' + ProductDetails[2] + ',' + ProductDetails[3]
    return HttpResponse(Data)

def SaveProductClick_Details(request):
    ProductID=request.GET.get('ProductID')
    PType=request.GET.get('PType')
    PName=request.GET.get('PName')
    logger.info(PName)
    PModel=request.GET.get('PModel')
    PStatus=request.GET.get('PStatus')
    cursor = connection.cursor()
    ValidationData=''
    if ProductID =='':
        ValidationData='Please Select ProductID'
    else:
        cursor.execute("""INSERT INTO blog_txsetsamcard(ProductID,ProductType,ProductName,ProductModel,ProductStatus)
        VALUES (%s,%s,%s,%s,%s)""",(ProductID,PType,PName,PModel,PStatus))
        ValidationData='Sucess'
    return HttpResponse(ValidationData)

def UpdateProductClick_Details(request):
    ProductID=request.GET.get('ProductID')
    PType=request.GET.get('PType')
    PName=request.GET.get('PName')
    PModel=request.GET.get('PModel')
    PStatus=request.GET.get('PStatus')
    cursor = connection.cursor()
    ValidationData=''
    if ProductID =='':
        ValidationData='Please Select ProductID'
    else:
        cursor.execute("""UPDATE blog_txsetsamcard SET ProductID=%s,ProductType=%s,ProductName=%s,ProductModel=%s,ProductStatus=%s WHERE id=%s""",
        (ProductID,PType,PName,PModel,PStatus,'1'))
        ValidationData='Sucess'
    return HttpResponse(ValidationData)



def SetSamCard_View(request):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    if TxSetSAMCard.objects.all().count()>0:
        cursor.execute("SELECT ProductID,ProductType,ProductName,ProductModel,ProductStatus  FROM blog_txsetsamcard")
        ProductDetails=cursor.fetchone()
        ProductID=ProductDetails[0]
        ProductType=ProductDetails[1]
        ProductName=ProductDetails[2]
        ProductModel=ProductDetails[3]
        ProductStatus=ProductDetails[4]
        WHValue='YES'
        return render(request, 'SetSAMCard.html',{'WHValue':WHValue,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'ProductStatus':ProductStatus,'UserRole':userrole,'obj':MsProduct.objects.filter(ProductName='SAM Card').filter(ProductStatus='Active'),'full_name':request.user.first_name})        
    else:
        WHValue='NO'
        return render(request, 'SetSAMCard.html',{'WHValue':WHValue,'UserRole':userrole,'obj':MsProduct.objects.filter(ProductName='SAM Card').filter(ProductStatus='Active'),'full_name':request.user.first_name})



#-------------------------------------------------Finish Good Receiving--------------------------------------------------------------

def View_FGReceiving(request):
    userrole=get_role(request.user.email)
    RefNumber=request.POST.getlist('PurchaseCheck')
    logger.info(RefNumber)
    if RefNumber !=[]:
        for i in RefNumber:
            cursor = connection.cursor()
            cursor.execute("SELECT SAM_SN  FROM blog_txhandovermaterialhdr where RefNumber=('%s')" % (i))
            SAM_SN=cursor.fetchone()[0]
            logger.info(SAM_SN)
            cursor.execute("SELECT SAMPIN  FROM blog_txsam where SAM_SN=('%s')" % (SAM_SN))
            SAMPIN=cursor.fetchone()[0]
            logger.info(SAMPIN)
            if SAMPIN == '':
                return render(request,'ViewFinishGoodReceiving.html',{'Error':'Please Download SAM PIN File in Edit HandOver Material by downloading the SAMPIN file','UserRole':userrole,'obj':TxHandOverMaterialHdr.objects.filter(ProductionStatus='Staging'),'full_name':request.user.first_name})
            cursor.execute("SELECT OutputWarehouseName  FROM blog_txwarehouseforproduction")
            OutputWarehouseID=cursor.fetchone()[0]
            cursor.execute("SELECT ProductID  FROM blog_txhandovermaterialhdr where RefNumber=('%s')" % (i))
            ProductID=cursor.fetchone()[0]
            cursor.execute("SELECT ProductName  FROM blog_txhandovermaterialhdr where RefNumber=('%s')" % (i))
            ProductName=cursor.fetchone()[0]
            cursor.execute("SELECT ProductModel  FROM blog_txhandovermaterialhdr where RefNumber=('%s')" % (i))
            ProductModel=cursor.fetchone()[0]
            cursor.execute("SELECT Product_SN  FROM blog_txhandovermaterialhdr where RefNumber=('%s')" % (i))
            Product_SN=cursor.fetchone()[0]
            cursor.execute("SELECT SAM_SN  FROM blog_txhandovermaterialhdr where RefNumber=('%s')" % (i))
            SAM_SN=cursor.fetchone()[0]
            now=datetime.now()
            CreatedOn=str(now)[:19]
            CreatedBy=request.user.first_name
            LastUpdateOn=str(now)[:19]
            LastUpdateBy=request.user.first_name
            cursor.execute("""UPDATE blog_txhandovermaterialhdr SET EndProductionDate=%s,ProductionStatus=%s WHERE  RefNumber=%s""",(CreatedOn[:10],'Finished',i))

            cursor.execute("""UPDATE blog_txsam SET Product_SN=%s,Product_Model=%s,Product_Name=%s,Production_Date=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  SAM_SN=%s""",(Product_SN,ProductModel,ProductName,CreatedOn,LastUpdateOn,LastUpdateBy,SAM_SN))
    
            cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(i,"FinishGoodReceiving",OutputWarehouseID,ProductID,ProductName,'1','0','1','Yes',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
            
            cursor.execute("""INSERT INTO blog_txstocksn(ProductID,ProductName,SerialNumber,SNStatus,RefNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,ProductName,Product_SN,'IN',i,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
            
            if TxHandOverMaterialDtl.objects.filter(ProductionID=i[:12]).count()>0:
                cursor.execute("SELECT InputWarehouseName  FROM blog_txwarehouseforproduction")
                InputWarehouseID=cursor.fetchone()[0]
                cursor.execute("select GROUP_CONCAT(RefNumber) from blog_txhandovermaterialdtl where ProductionID =('%s')" %(i[:12]))
                MaterialRefid=cursor.fetchone()[0]
                logger.info(MaterialRefid)
                MaterialRefList=MaterialRefid.split(',')
                for j in MaterialRefList:
                    cursor.execute("select MaterialQty from blog_txhandovermaterialdtl where RefNumber =('%s')" %(j))
                    MaterialQty=cursor.fetchone()[0]
                    cursor.execute("select MaterialCode from blog_txhandovermaterialdtl where RefNumber =('%s')" %(j))
                    MaterialCode=cursor.fetchone()[0]
                    cursor.execute("select MaterialName from blog_txhandovermaterialdtl where RefNumber =('%s')" %(j))
                    MaterialName=cursor.fetchone()[0]
                    cursor.execute("select ProductSerialNumber from blog_msproduct where ProductID =('%s')" %(MaterialCode))
                    StockSN=cursor.fetchone()[0]
                    StockBalance=0-int(MaterialQty)
                    logger.info(StockBalance)
                    cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(j,"FinishGoodReceiving",OutputWarehouseID,MaterialCode,MaterialName,'0',MaterialQty,StockBalance,StockSN,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))

                    #cursor.execute("""INSERT INTO blog_txproductionmaterial_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,StockQtyIN,StockQtyOut,StockQtyBalance)
                    #VALUES (%s,%s,%s,%s,%s,%s,%s)""",(j,"FinishGoodReceiving",InputWarehouseID,ProductID,'0',MaterialQty,MaterialQty))
                    
                    cursor.execute("""INSERT INTO blog_txstocksn(ProductID,ProductName,SerialNumber,SNStatus,RefNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(MaterialCode,MaterialName,SAM_SN,'OUT',j,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
            
                    
        return render(request,'ViewFinishGoodReceiving.html',{'UserRole':userrole,'obj':TxHandOverMaterialHdr.objects.filter(ProductionStatus='Staging'),'full_name':request.user.first_name})
    else:
	return render(request,'ViewFinishGoodReceiving.html',{'UserRole':userrole,'obj':TxHandOverMaterialHdr.objects.filter(ProductionStatus='Staging'),'full_name':request.user.first_name})
	
    

#------------------------------------------------------------------- Adjustment Stock ------------------------------------------------------------------------------------------------------------------------------------
def ADjustment_serial_Insertation(request):
    ProductId=request.GET.get('ProductID')
    logger.info(ProductId)
    ProductName=request.GET.get('ProductName')
    logger.info(ProductName)
    AdjustmentType=request.GET.get('SNStatus')
    logger.info(AdjustmentType)
    SerialNumber=request.GET.get('SerialNumber')
    logger.info(SerialNumber)
    AdjustmentID=request.GET.get('AdjustmentID')
    logger.info(AdjustmentID)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductType from blog_msproduct where ProductID=('%s')" % (ProductId))
    ProductType=cursor.fetchone()
    logger.info(ProductType)
    now=datetime.now().date()
    logger.info(now)
    CreatedOn=str(now)[:10]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:10]
    LastUpdateBy=request.user.first_name
    ValidationData=''
    getdata=''
    if SerialNumber =='':
        ValidationData='Please Enter Serial Number'
        if AdjustmentType =='':
            ValidationData='Please Select Adjustment Type'
        elif TxStockSN.objects.filter(SerialNumber=SerialNumber).count()>0:
            ValidationData='Data has already been added previously'
    else:
        cursor.execute("""INSERT INTO blog_txstocksn(ProductID,ProductName,SNStatus,SerialNumber,ProductType,RefNumber,AdjustmentStockID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (ProductId,ProductName,AdjustmentType,SerialNumber,ProductType,AdjustmentID,AdjustmentID,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        obj=TxStockSN.objects.filter(ProductID=ProductId).filter(RefNumber=AdjustmentID).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)


def Adjustment_Add_to_Stock_List(request):
    AdjustmentType=request.GET.get('SNStatus')
    logger.info(AdjustmentType)
    StockNumber=request.GET.get('StockNO')
    logger.info(StockNumber)
    Warehouse=request.GET.get('Warehouse')
    logger.info(Warehouse)
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    AdjustmentStockID=request.GET.get('ReferenceNO')
    logger.info(AdjustmentStockID)
    ReferenceTransaction=request.GET.get('ReferenceTranscation')
    logger.info(ReferenceTransaction)
    ProductName=request.GET.get('ProductName')
    logger.info(ProductName)
    PreviousCount=request.GET.get('PreviousCount')
    logger.info(PreviousCount)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    ValidationData=''
    getdata=''
    CountSerialStatus='Yes'
    SerialCount=''
    cursor = connection.cursor()
    #cursor.execute("SELECT WarehouseID from blog_warehouse where WarehouseName=('%s')" % (Warehouse))
    #WarehouseID=cursor.fetchone()[0]
    #logger.info(WarehouseID)
    if StockNumber !=None:
        SerialStatus="No"
    else:
        SerialStatus="Yes"
	cursor.execute("SELECT COUNT(AdjustmentStockID) FROM blog_txstocksn where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
        StockNumber=cursor.fetchone()[0]
    logger.info(SerialStatus)
    if AdjustmentType=='IN':
        logger.info(StockNumber)
        OutputstockQTY=0
        logger.info(OutputstockQTY)
    else:
        AdjustmentType=='OUT'
        logger.info(StockNumber)
        InputstockQTY=0
        logger.info(InputstockQTY)
    if ProductID =='' and Warehouse =='' and AdjustmentType=='':
        ValidationData='Please Select ProductId and Warehouse and AdjustmentType'
    else:
        if AdjustmentType =='IN':
            cursor.execute("""INSERT INTO blog_txadjustmentstock_dtl(ProductID,AdjustmentStockID,AdjustmentType,InputStockQty,OutputStockQty,WarehouseID,InputOutput,SerialStatus,RefTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,AdjustmentType,StockNumber,OutputstockQTY,Warehouse,StockNumber,SerialStatus,ReferenceTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            obj=TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).filter(AdjustmentStockID=AdjustmentStockID).values_list('AdjustmentType','ProductID','InputOutput','WarehouseID','SerialStatus','id','InputStockQty')
        else:
            cursor.execute("""INSERT INTO blog_txadjustmentstock_dtl(ProductID,AdjustmentStockID,AdjustmentType,OutputStockQty,InputStockQty,WarehouseID,InputOutput,SerialStatus,RefTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,AdjustmentType,StockNumber,InputstockQTY,Warehouse,StockNumber,SerialStatus,ReferenceTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            obj=TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).filter(AdjustmentStockID=AdjustmentStockID).values_list('AdjustmentType','ProductID','InputOutput','WarehouseID','SerialStatus','id','OutputStockQty')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
        if TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).count()>0:
            cursor.execute("SELECT COUNT(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            InputStockQTYcount=cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            OutputStockQTYcount=cursor.fetchone()[0]
            if InputStockQTYcount>0:
                cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
                StockBalance=cursor.fetchone()[0]
                logger.info(StockBalance)
            else:
                if OutputStockQTYcount>0:
                    cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
                StockBalance=cursor.fetchone()[0]
                logger.info(StockBalance)
    data=ValidationData + '.' + getdata+'.'+str(StockBalance)
    logger.info(data)
    return HttpResponse(data)


def Adjustment_Add_to_Stock_List_SerialCount(request):
    AdjustmentType=request.GET.get('SNStatus')
    logger.info(AdjustmentType)
    StockNumber=request.GET.get('StockNO')
    logger.info(StockNumber)
    Warehouse=request.GET.get('Warehouse')
    logger.info(Warehouse)
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    AdjustmentStockID=request.GET.get('ReferenceNO')
    logger.info(AdjustmentStockID)
    Serialcount=request.GET.get('SerialCount')
    logger.info(Serialcount)
    ReferenceTransaction=request.GET.get('ReferenceTranscation')
    logger.info(ReferenceTransaction)
    ProductName=request.GET.get('ProductName')
    logger.info(ProductName)
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    ValidationData=''
    getdata=''
    cursor = connection.cursor()
    #cursor.execute("SELECT WarehouseID from blog_warehouse where WarehouseName=('%s')" % (Warehouse))
    #WarehouseID=cursor.fetchone()[0]
    #logger.info(WarehouseID)
    if StockNumber !=None:
        SerialStatus="No"
    else:
        SerialStatus="Yes"
        cursor.execute("SELECT COUNT(AdjustmentStockID) FROM blog_txstocksn where ProductID=('%s')" % (ProductID))
        StockNumber=cursor.fetchone()[0]
        logger.info(StockNumber)
        logger.info(SerialStatus)
        if StockNumber>0:
            StockNumber=int(StockNumber)-int(Serialcount)
            logger.info(StockNumber)
    if AdjustmentType=='IN':
        logger.info(StockNumber)
        OutputstockQTY=0
        logger.info(OutputstockQTY)
    else:
        AdjustmentType=='OUT'
        logger.info(StockNumber)
        InputstockQTY=0
        logger.info(InputstockQTY)
    if ProductID =='' and Warehouse =='':
        ValidationData='Please Select ProductId and Warehouse'
    #elif TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).count()>0:
        #ValidationData='Data has already been added previously'
    else:
        if AdjustmentType =='IN':
            cursor.execute("""INSERT INTO blog_txadjustmentstock_dtl(ProductID,AdjustmentStockID,AdjustmentType,InputStockQty,OutputStockQty,WarehouseID,InputOutput,SerialStatus,RefTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,AdjustmentType,StockNumber,OutputstockQTY,Warehouse,StockNumber,SerialStatus,ReferenceTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            obj=TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).values_list('AdjustmentType','InputOutput','WarehouseID','SerialStatus','id','InputStockQty')
        else:
            cursor.execute("""INSERT INTO blog_txadjustmentstock_dtl(ProductID,AdjustmentStockID,AdjustmentType,OutputStockQty,InputStockQty,WarehouseID,InputOutput,SerialStatus,RefTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,AdjustmentType,StockNumber,InputstockQTY,Warehouse,StockNumber,SerialStatus,ReferenceTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            obj=TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).values_list('AdjustmentType','InputOutput','WarehouseID','SerialStatus','id','OutputStockQty')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)


def AdjustmentStock(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('ProductID')
    logger.info(ProductID)
    AdjustmentStockID=request.POST.get('RefNumber')
    logger.info(AdjustmentStockID)
    ProductName=request.POST.get('ProductName')
    logger.info(ProductName)
    ReferenceTransaction=request.POST.get('RefTransaction')
    logger.info(ReferenceTransaction)
    AdjustmentType=request.POST.get('AdjustmentType')
    logger.info(AdjustmentType)
    IOStockStatus=request.POST.get('Status')
    logger.info(IOStockStatus)
    StockNumber=request.POST.get('StockNumber')
    logger.info(StockNumber)
    Warehouse=request.POST.get('WareHouseName')
    logger.info(Warehouse)
    Remarks=request.POST.get('Remark')
    logger.info(Remarks)
    StockQty=''
    now=datetime.now()
    CreatedOn=str(now)[:10]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:10]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if AdjustmentStockID!=None and ProductID!=None:
        if StockNumber !='':
            SerialStatus="No"
        else:
            SerialStatus="Yes"
            cursor.execute("SELECT COUNT(AdjustmentStockID) from blog_txstocksn where ProductID=('%s') AND RefNumber=('%s')" % (ProductID,AdjustmentStockID))
            StockNumber=cursor.fetchone()[0]
            logger.info(StockNumber)
        if request.POST.get('_Save'):
            logger.info("Save Button Log")
            if StockNumber!='':
                StockQty=int(StockNumber)
                logger.info(StockQty)
            if AdjustmentType=='IN':
                OutputstockQTY=0
            elif AdjustmentType=='OUT':
                OutputstockQTY=StockQty
                StockQty=0
            cursor.execute("""INSERT INTO blog_txadjustmentstock_dtl(ProductID,AdjustmentStockID,AdjustmentType,InputStockQty,OutputStockQty,WarehouseID,InputOutput,SerialStatus,RefTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,AdjustmentType,StockQty,OutputstockQTY,Warehouse,StockNumber,SerialStatus,ReferenceTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            StockQtyIn=cursor.fetchone()[0]
            logger.info(StockQtyIn)
            InStock=int(StockQtyIn)
            cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            StockQtyOut=cursor.fetchone()[0]
            logger.info(StockQtyOut)
            OutStock=int(StockQtyOut)
            StockBalance=InStock-OutStock
            logger.info(StockBalance)
            cursor.execute("""INSERT INTO blog_txadjustmentstock_hdr(ProductID,AdjustmentStockID,IOStockStatus,IOStockBalance,ProductName,RefTransaction,WarehouseID,Remark,AdjustmentType,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,IOStockStatus,StockBalance,ProductName,ReferenceTransaction,Warehouse,Remarks,AdjustmentType,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            return HttpResponseRedirect('/accounts/ViewAdjustmentStockList/',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
        if request.POST.get('_Save&Send'):
            logger.info("Save and Send Button Log")
            StockQty=int(StockNumber)
            logger.info(StockQty)
            if AdjustmentType=='IN':
                OutputstockQTY=0
            elif AdjustmentType=='OUT':
                OutputstockQTY=StockQty
                StockQty=0
            cursor.execute("""INSERT INTO blog_txadjustmentstock_dtl(ProductID,AdjustmentStockID,AdjustmentType,InputStockQty,OutputStockQty,WarehouseID,InputOutput,SerialStatus,RefTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,AdjustmentType,StockQty,OutputstockQTY,Warehouse,StockNumber,SerialStatus,ReferenceTransaction,ProductName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            StockQtyIn=cursor.fetchone()[0]
            logger.info(StockQtyIn)
            InStock=int(StockQtyIn)
            cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            StockQtyOut=cursor.fetchone()[0]
            logger.info(StockQtyOut)
            OutStock=int(StockQtyOut)
            StockBalance=InStock-OutStock
            logger.info(StockBalance)
            cursor.execute("""INSERT INTO blog_txadjustmentstock_hdr(ProductID,AdjustmentStockID,IOStockStatus,IOStockBalance,ProductName,RefTransaction,WarehouseID,Remark,AdjustmentType,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,'Commit',StockBalance,ProductName,ReferenceTransaction,Warehouse,Remarks,AdjustmentType,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            cursor.execute("""INSERT INTO blog_txstock(ProductID,RefNumber,RefTransaction,StockQtyIN,StockQtyOut,WarehouseID,StockQtyBalance,ProductName,StockSN,ADJIOStockStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,ReferenceTransaction,StockQty,OutputstockQTY,Warehouse,StockBalance,ProductName,SerialStatus,'Commit',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            return HttpResponseRedirect('/accounts/ViewAdjustmentStockList/',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
    return render(request, 'AdjustmentStock.html',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})


def StockbalanceLabel(request):
    ProductIDfrompage=request.GET.get('ProductID')
    logger.info(ProductIDfrompage)
    AdjustmentIDfrompage=request.GET.get('AdjustmentID')
    logger.info(AdjustmentIDfrompage)
    validationData=''
    StockBalance=''
    cursor = connection.cursor()
    if TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductIDfrompage).count()>0:
        validationData="This product is already having stock quantity please go to View Adjustment Stocklist and Edit it"
    cursor.execute("SELECT COUNT(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductIDfrompage,AdjustmentIDfrompage))
    InputStockQTYcount=cursor.fetchone()[0]
    logger.info(InputStockQTYcount)
    cursor.execute("SELECT COUNT(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductIDfrompage,AdjustmentIDfrompage))
    OutputStockQTYcount=cursor.fetchone()[0]
    logger.info(OutputStockQTYcount)
    if InputStockQTYcount>0:
        cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductIDfrompage,AdjustmentIDfrompage))
        StockBalance=cursor.fetchone()[0]
        logger.info(StockBalance)
    elif OutputStockQTYcount>0:
        cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductIDfrompage,AdjustmentIDfrompage))
        StockBalance=cursor.fetchone()[0]
        logger.info(StockBalance)
    else:
        validationData="There is No Stock Available For This Product Please Add Stock Quantity"
    data=validationData + '.' + str(StockBalance)
    logger.info(data)
    return HttpResponse(data)

def Adjustment_Product_Details(request):
    ProductIDFromPage=request.GET.get('ProductID')
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName from blog_msproduct where ProductID=('%s')" % (ProductIDFromPage))
    ProductName=cursor.fetchone()[0]
    logger.info(ProductName)
    StockQtyBalance=0
    if TxAdjustmentStock_Hdr.objects.filter(ProductID=ProductIDFromPage).count()>0:
        cursor.execute("SELECT SUM(IOStockBalance) from blog_txadjustmentstock_hdr where ProductID=('%s')" % (ProductIDFromPage))
        StockQtyBalance=cursor.fetchone()[0]
        logger.info(StockQtyBalance)
    if ProductIDFromPage:
        c = {
         'Pagedata':ProductName,
         }
    else:
        DataFromPage = "Nothing"
        c = {
             'Pagedata':ProductName,
             }
        logger.info(c)
    Data=ProductName+ '.' +str(StockQtyBalance)
    return HttpResponse(Data)


def view_Adjustment_StockList(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
        return HttpResponseRedirect('/accounts/login/')
    else:
        return render_to_response('ViewAdjustmentStock.html',{'obj':TxAdjustmentStock_Hdr.objects.all(),'full_name':request.user.first_name,'UserRole':userrole})



def Edit_Adjustment_Stock(request,u_id):
    userrole=get_role(request.user.email)
    StockNumber=''
    cursor = connection.cursor()
    InStockresult=TxAdjustmentStock_Hdr.objects.raw("SELECT h.id,h.AdjustmentStockID,h.ProductID,h.IOStockBalance,h.IOStockStatus,h.Remark,h.ProductName,h.WarehouseID,h.RefTransaction,h.AdjustmentType FROM blog_txadjustmentstock_hdr h WHERE h.id=('%s')"%(u_id))
    for i in InStockresult:
        cursor.execute("SELECT COUNT(AdjustmentStockID) FROM blog_txstocksn where ProductID=('%s') AND RefNumber=('%s')" % (i.ProductID,i.AdjustmentStockID))
        SerialCount=cursor.fetchone()[0]
        logger.info(SerialCount)
        cursor.execute("SELECT ProductSerialNumber from blog_msproduct where ProductID=('%s')" % (i.ProductID))
        ProductSerialNumber =cursor.fetchone()[0]
        logger.info(ProductSerialNumber)
        cursor.execute("SELECT SUM(IOStockBalance) from blog_txadjustmentstock_hdr where ProductID=('%s')" % (i.ProductID))
        IOStockBalance =cursor.fetchone()[0]
        logger.info(IOStockBalance)
        StockBalance=int(IOStockBalance)
        cursor.execute("SELECT AdjustmentType from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (i.ProductID,i.AdjustmentStockID))
        AdjustmentType =cursor.fetchone()[0]
        logger.info(AdjustmentType)
        if AdjustmentType=='OUT':
            StockNumber=-(StockBalance)
	else:
	     if AdjustmentType=='IN':
		StockNumber=(StockBalance)
        if request.user.username == '':
            return HttpResponseRedirect('/accounts/login/')
        else:
            return render(request, 'EditAdjustmentStock.html',{
                    'lblAS':u_id,
                    'Productid':i.ProductID,
                    'RefNumber':i.AdjustmentStockID,
                    'ProductName':i.ProductName,
                    'RefTransaction':i.RefTransaction,
                    'AdjustmentType':i.AdjustmentType,
                    'IOStatus':i.IOStockStatus,
                    'Warehouse':i.WarehouseID,
                    'Remark':i.Remark,
                    'SerialStatus':ProductSerialNumber,
                    'StockNumber':i.IOStockBalance,
                    'StockBalance':StockBalance,
                    'lblNumber':'Total Number of Serial Number has been added:'+ str(SerialCount),
                    'obj':TxStockSN.objects.filter(ProductID=i.ProductID).filter(AdjustmentStockID=i.AdjustmentStockID),
                    'stocklist':TxAdjustmentStock_Dtl.objects.filter(ProductID=i.ProductID).filter(AdjustmentStockID=i.AdjustmentStockID),
                    'ProductID':MsProduct.objects.filter(ProductStatus='Active'),
                    'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),
                    'UserRole':userrole,
                    'full_name':request.user.first_name
                })



def Update_Adjustment(request):
    userrole=get_role(request.user.email)
    ProductID=request.POST.get('ProductID')
    logger.info(ProductID)
    AdjustmentStockID=request.POST.get('RefNumber')
    logger.info(AdjustmentStockID)
    ReferenceTransaction=request.POST.get('RefTransaction')
    logger.info(ReferenceTransaction)
    ProductName=request.POST.get('ProductName')
    logger.info(ProductName)
    AdjustmentType=request.POST.get('AdjustmentType')
    logger.info(AdjustmentType)
    StockNumber=request.POST.get('StockNumber')
    logger.info(StockNumber)
    Warehouse=request.POST.get('WareHouseName')
    logger.info(Warehouse)
    IOStockStatus=request.POST.get('Status')
    logger.info(IOStockStatus)
    Remarks=request.POST.get('Remark')
    logger.info(Remarks)
    OutputstockQTY=''
    StockQty=''
    StockBalance=''
    now=datetime.now()
    CreatedOn=str(now)[:10]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:10]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if StockNumber !=None:
        SerialStatus="No"
        logger.info(SerialStatus)
    else:
        SerialStatus="Yes"
        cursor.execute("SELECT COUNT(AdjustmentStockID) from blog_txstocksn where ProductID=('%s') AND RefNumber=('%s')" % (ProductID,AdjustmentStockID))
        StockNumber=cursor.fetchone()[0]
        logger.info(StockNumber)
    if request.POST.get('_Save'):
        if StockNumber!=None:
            StockQty=int(StockNumber)
            logger.info(StockQty)
        if AdjustmentType=='IN':
            OutputstockQTY=0
            logger.info(OutputstockQTY)
        elif AdjustmentType=='OUT':
            OutputstockQTY=StockQty
            StockQty=0
        if TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).filter(AdjustmentStockID=AdjustmentStockID).count()>0:
            cursor.execute("""UPDATE blog_txadjustmentstock_dtl SET InputStockQty=%s,OutputStockQty=%s,InputOutput=%s WHERE ProductID=%s AND AdjustmentStockID= %s""",(StockQty,OutputstockQTY,StockQty,ProductID,AdjustmentStockID))
            cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            StockQtyIn=cursor.fetchone()[0]
            logger.info(StockQtyIn)
            InStock=int(StockQtyIn)
            cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
            StockQtyOut=cursor.fetchone()[0]
            logger.info(StockQtyOut)
            OutStock=int(StockQtyOut)
            StockBalance=InStock-OutStock
            logger.info(StockBalance)
            cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,Remark=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s AND AdjustmentStockID=%s""",(StockBalance,Remarks,LastUpdateOn,LastUpdateBy,ProductID,AdjustmentStockID))
            return HttpResponseRedirect('/accounts/ViewAdjustmentStockList/',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
    else:
        if request.POST.get('_Save&Send'):
            if StockNumber!='':
                StockQty=int(StockNumber)
                logger.info(StockQty)
            if AdjustmentType=='IN':
                OutputstockQTY=0
            elif AdjustmentType=='OUT':
                OutputstockQTY=StockQty
                StockQty=0
            if TxAdjustmentStock_Dtl.objects.filter(ProductID=ProductID).filter(AdjustmentStockID=AdjustmentStockID).count()>0:
                cursor.execute("""UPDATE blog_txadjustmentstock_dtl SET InputStockQty=%s,OutputStockQty=%s,InputOutput=%s WHERE ProductID=%s AND AdjustmentStockID= %s""",(StockQty,OutputstockQTY,StockQty,ProductID,AdjustmentStockID))
                cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
                StockQtyIn=cursor.fetchone()[0]
                logger.info(StockQtyIn)
                InStock=int(StockQtyIn)
                cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (ProductID,AdjustmentStockID))
                StockQtyOut=cursor.fetchone()[0]
                logger.info(StockQtyOut)
                OutStock=int(StockQtyOut)
                StockBalance=InStock-OutStock
                logger.info(StockBalance)
                cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,Remark=%s,IOStockStatus=%s,AdjustmentStockID=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s """,(StockBalance,Remarks,'Commit',AdjustmentStockID,LastUpdateOn,LastUpdateBy,ProductID))
            if txStock.objects.filter(ProductID=ProductID).filter(RefNumber=AdjustmentStockID).count()>0:
                cursor.execute("""UPDATE blog_txstock SET StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s,ADJIOStockStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s AND RefNumber=%s""",(StockQty,OutputstockQTY,StockBalance,'Commit',LastUpdateOn,LastUpdateBy,ProductID,AdjustmentStockID))
                return HttpResponseRedirect('/accounts/ViewAdjustmentStockList/',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
            else:
                cursor.execute("""INSERT INTO blog_txstock(ProductID,RefNumber,RefTransaction,StockQtyOut,StockQtyIN,WarehouseID,StockQtyBalance,ProductName,StockSN,ADJIOStockStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,AdjustmentStockID,ReferenceTransaction,OutputstockQTY,StockQty,Warehouse,StockBalance,ProductName,SerialStatus,'Commit',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
                return HttpResponseRedirect('/accounts/ViewAdjustmentStockList/',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
    return render(request, 'EditAdjustmentStock.html',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})


def Edit_Adjustment_SerialNumber(request,serialNumber):
    userrole=get_role(request.user.email)
    cursor = connection.cursor()
    cursor.execute("SELECT id from blog_txstocksn where SerialNumber =('%s')" % (serialNumber))
    data =  cursor.fetchone()[0]
    logger.info(data)
    cursor.execute("SELECT AdjustmentStockID from blog_txstocksn where SerialNumber =('%s')" % (serialNumber))
    AdjustmentStockID = cursor.fetchone()[0]
    logger.info(AdjustmentStockID)
    cursor.execute("SELECT ProductID from blog_txstocksn where SerialNumber =('%s')" % (serialNumber))
    ProductID = cursor.fetchone()[0]
    logger.info(ProductID)
    if request.user.username == '':
        return HttpResponseRedirect('/accounts/login/')
    else:
        return render(request, 'AdjustmentSerialNO.html',{'lblSN':data,
                                                        'SerialNumber':serialNumber,
                                                        'SrlAdjustmentID':AdjustmentStockID,
                                                        'Productid':ProductID,
                                                        'UserRole':userrole,
                                                        'full_name':request.user.first_name
                                                        })




def Update_Adjustment_SerialNumber(request):
    userrole=get_role(request.user.email)
    SerialNumber=request.GET.get('SerialNumber')
    logger.info(SerialNumber)
    snid=request.GET.get('lblSN')
    logger.info(snid)
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    AdjustmentID=request.GET.get('ModalAdjustmentID')
    logger.info(AdjustmentID)
    ValidationData=''
    getdata=''
    data=''
    cursor = connection.cursor()
    if TxAdjustmentStock_TxStockSN.objects.filter(SerialNumber=SerialNumber).count() > 0:
        ValidationData='Data has already been added please check it again'
    else:
        cursor.execute("""UPDATE blog_txstocksn SET SerialNumber=%s WHERE id=%s""",
	(SerialNumber,snid))
        obj=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=AdjustmentID).values_list('SerialNumber')
        getdata=json.dumps(list(obj))
        logger.info(getdata)
    data=ValidationData + '.' + getdata
    logger.info(data)
    return HttpResponse(data)


def Delete_Adjustment_SN_View(request,uid):
    userrole=get_role(request.user.email)
    SerialNO=uid
    logger.info(SerialNO)
    cursor = connection.cursor()
    cursor.execute("SELECT AdjustmentStockID from blog_txstocksn where SerialNumber=('%s')" % (SerialNO))
    AdjstmntID=cursor.fetchone()[0]
    logger.info(AdjstmntID)
    cursor.execute("SELECT id from blog_txstocksn where SerialNumber=('%s')" % (SerialNO))
    SNid=cursor.fetchone()[0]
    logger.info(SNid)
    cursor.execute("SELECT ProductID from blog_txstocksn where SerialNumber=('%s')" % (SerialNO))
    Productid=cursor.fetchone()[0]
    logger.info(Productid)
    return render(request, 'DeleteAdjustmentSN.html',{'SNid':SNid,'SerialNO':SerialNO,'AdjstmntID':AdjstmntID,'Productid':Productid,'UserRole':userrole,'full_name':request.user.first_name})


def Delete_Adjustment_SerialNumber(request):
    uid=request.GET.get('SNid')
    logger.info(uid)
    dbProductID=request.GET.get('Productid')
    logger.info(dbProductID)
    AdjustmentID=request.GET.get('AdjustmentID')
    logger.info(AdjustmentID)
    SerialNumber=request.GET.get('SerialNumber')
    logger.info(SerialNumber)
    ProductName=request.GET.get('ProductName')
    logger.info(ProductName)
    Dtltableinputqty=''
    Dtltableoutputqty=''
    Stockbalance=''
    cursor = connection.cursor()
    cursor.execute("SELECT SNStatus from blog_txstocksn where ProductID=('%s') AND SerialNumber=('%s')" % (dbProductID,SerialNumber))
    AdjustmentType=cursor.fetchone()[0]
    logger.info(AdjustmentType)
    cursor.execute("SELECT StockQtyIN from blog_txstock where ProductID=('%s') AND RefNumber=('%s')" % (dbProductID,AdjustmentID))
    InputQuantity=cursor.fetchone()
    logger.info(InputQuantity)
    cursor.execute("SELECT StockQtyOut from blog_txstock where ProductID=('%s') AND RefNumber=('%s')" % (dbProductID,AdjustmentID))
    OutputQuantity=cursor.fetchone()
    logger.info(OutputQuantity)
    cursor.execute("SELECT InputStockQty from blog_txadjustmentstock_dtl where AdjustmentStockID=('%s') AND AdjustmentType=('%s') AND ProductID=('%s') AND SerialStatus=('%s')" % (AdjustmentID,AdjustmentType,dbProductID,'Yes'))
    Dtltableinputqty=cursor.fetchone()
    logger.info(Dtltableinputqty)
    cursor.execute("SELECT OutputStockQty from blog_txadjustmentstock_dtl where AdjustmentStockID=('%s') AND AdjustmentType=('%s') AND ProductID=('%s') AND SerialStatus=('%s')" % (AdjustmentID,AdjustmentType,dbProductID,'Yes'))
    Dtltableoutputqty=cursor.fetchone()
    logger.info(Dtltableoutputqty)
    if Dtltableinputqty==None or Dtltableoutputqty==None:
        logger.info("Hi IO LOg")
        TxStockSN.objects.filter(id=uid).delete()
    else:
        if InputQuantity!=None or Dtltableoutputqty!=None:
            TxStockSN.objects.filter(id=uid).delete()
            if AdjustmentID!=None:
                if AdjustmentType=="IN":
                    deletevalue=1
                    cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                    Dtltableinputqty=cursor.fetchone()[0]
                    logger.info(Dtltableinputqty)
                    inputqtydtl=int(Dtltableinputqty)-int(deletevalue)
                    logger.info(inputqtydtl)
                    cursor.execute("""UPDATE blog_txadjustmentstock_dtl SET InputStockQty=%s,InputOutput=%s WHERE ProductID=%s AND SerialStatus=%s AND AdjustmentStockID=%s""",
                    (inputqtydtl,inputqtydtl,dbProductID,'Yes',AdjustmentID))
                else:
                    if AdjustmentType=="OUT":
                        outdeletevalue=1
                        cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                        Dtltableoutputqty=cursor.fetchone()[0]
                        logger.info(Dtltableoutputqty)
                        outputqtydtl=int(Dtltableoutputqty)-int(outdeletevalue)
                        logger.info(outputqtydtl)
                        cursor.execute("""UPDATE blog_txadjustmentstock_dtl SET OutputStockQty=%s,InputOutput=%s WHERE ProductID=%s AND SerialStatus=%s AND AdjustmentStockID=%s""",
                        (outputqtydtl,outputqtydtl,dbProductID,'Yes',AdjustmentID))
                cursor.execute("SELECT SUM(InputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                InputQuantity=cursor.fetchone()[0]
                logger.info(InputQuantity)
                cursor.execute("SELECT SUM(OutputStockQty) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                OutputQuantity=cursor.fetchone()[0]
                Stockbalance=int(InputQuantity)-int(OutputQuantity)
                logger.info(Stockbalance)
                cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s WHERE ProductID=%s""",
                (Stockbalance,dbProductID))
    obj=TxStockSN.objects.filter(ProductID=dbProductID).filter(AdjustmentStockID=AdjustmentID).values_list('SerialNumber')
    getdata=json.dumps(list(obj))
    logger.info(getdata)
    logger.info(Stockbalance)
    data=str(Stockbalance) + '.' + getdata
    logger.info(data)
    return HttpResponse(data)


def Edit_Adjustment_StockList(request,u_id):
    userrole=get_role(request.user.email)
    uid=u_id
    logger.info(uid)
    cursor = connection.cursor()
    cursor.execute("SELECT AdjustmentType from blog_txadjustmentstock_dtl where id=('%s')" % (u_id))
    AdjustmentType=cursor.fetchone()[0]
    logger.info(AdjustmentType)
    cursor.execute("SELECT WarehouseID from blog_txadjustmentstock_dtl where id=('%s')" % (u_id))
    WarehouseName=cursor.fetchone()[0]
    logger.info(WarehouseName)
    #cursor.execute("SELECT WarehouseName from blog_warehouse where WarehouseID=('%s')" % (WarehouseID))
    #WarehouseName=cursor.fetchone()[0]
    #logger.info(WarehouseName)
    if AdjustmentType=='IN':
        StockList=TxAdjustmentStock_TxStockSN.objects.raw('SELECT * FROM blog_txadjustmentstock_dtl where id =%s',[u_id])
        for s in StockList:
            if request.user.username == '':
                return HttpResponseRedirect('/accounts/login/')
        else:
            return render(request, 'EditAdjustmentStockList.html',{'uid':u_id,
            'dtlProductid':s.ProductID,
            'dtlAdjustmentStockid':s.AdjustmentStockID,
            'dtlAdjustmentType':s.AdjustmentType,
            'dtlStockNO':s.InputStockQty,
            'InputOutput':s.InputOutput,
            'dtlWarehouseID':WarehouseName,
            'ProductID':MsProduct.objects.filter(ProductStatus='Active'),
            'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),
            'UserRole':userrole,
            'full_name':request.user.first_name
            })
    else:
        if AdjustmentType=='OUT':
            OutStockList=TxAdjustmentStock_TxStockSN.objects.raw('SELECT * FROM blog_txadjustmentstock_dtl where id =%s',[u_id])
            for t in OutStockList:
                if request.user.username == '':
                    return HttpResponseRedirect('/accounts/login/')
            else:
                return render(request, 'EditAdjustmentStockList.html',{'uid':u_id,
                'dtlProductid':t.ProductID,
                'dtlAdjustmentStockid':t.AdjustmentStockID,
                'dtlAdjustmentType':t.AdjustmentType,
                'dtlStockNO':t.OutputStockQty,
                'InputOutput':t.InputOutput,
                'dtlWarehouseID':WarehouseName,
                'ProductID':MsProduct.objects.filter(ProductStatus='Active'),
                'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),
                'UserRole':userrole,
                'full_name':request.user.first_name
                })




def Update_Adjustment_StockList(request):
    #userrole=get_role(request.user.email)
    AdjustmentType=request.GET.get('dtlAdjustmentType')
    logger.info(AdjustmentType)
    ProductID=request.GET.get('dtlProductID')
    logger.info(ProductID)
    Uid=request.GET.get('uid')
    logger.info(Uid)
    Warehouse=request.GET.get('dtlWareHouseName')
    logger.info(Warehouse)
    Stocknumber=request.GET.get('dtlStockNumber')
    logger.info(Stocknumber)
    StockID=request.GET.get('StockID')
    logger.info(StockID)
    InputStock=''
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    #cursor.execute("SELECT WarehouseID from blog_warehouse where WarehouseName=('%s')" % (Warehouse))
    #WarehouseID=cursor.fetchone()[0]
    #logger.info(WarehouseID)
    if AdjustmentType=='IN':
        cursor.execute("SELECT InputStockQty from blog_txadjustmentstock_dtl where id=('%s')" % (Uid))
        InputStockqnty=cursor.fetchone()[0]
        logger.info(InputStockqnty)
        cursor.execute("""UPDATE blog_txadjustmentstock_dtl SET InputStockQty=%s,InputOutput=%s,OutputStockQty=%s,WarehouseID=%s,AdjustmentType=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s AND id=%s""",
        (Stocknumber,Stocknumber,'0',Warehouse,AdjustmentType,LastUpdateOn,LastUpdateBy,ProductID,Uid))
        cursor.execute("SELECT SUM(InputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (ProductID))
        InputStock=cursor.fetchone()[0]
        logger.info(InputStock)            
        cursor.execute("SELECT SUM(OutputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (ProductID))
        OutputStock=cursor.fetchone()[0]
        logger.info(OutputStock)
        StockBalance=int(InputStock)-int(OutputStock)
        logger.info(StockBalance)
        cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,WarehouseID=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s""",
        (StockBalance,Warehouse,LastUpdateOn,LastUpdateBy,ProductID))
        #cursor.execute("""UPDATE blog_txadjustmentstock_txstock SET StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s WHERE ProductID=%s""",
        #(InputStock,OutputStock,StockBalance,ProductID))
        cursor.execute("""UPDATE blog_txstocksn SET SNStatus=%s WHERE ProductID=%s AND AdjustmentStockID=%s""",
        (AdjustmentType,ProductID,StockID))
    else:
        if AdjustmentType=='OUT':
            cursor.execute("SELECT OutputStockQty from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (Uid,ProductID))
            OutputStockqnty=cursor.fetchone()[0]
            logger.info(OutputStockqnty)
            cursor.execute("""UPDATE blog_txadjustmentstock_dtl SET OutputStockQty=%s,InputOutput=%s,InputStockQty=%s,WarehouseID=%s,AdjustmentType=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s AND id=%s""",
            (Stocknumber,Stocknumber,'0',WarehouseID,AdjustmentType,LastUpdateOn,LastUpdateBy,ProductID,Uid))
            cursor.execute("SELECT SUM(InputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (ProductID))
            InputStock=cursor.fetchone()[0]
            logger.info(InputStock)            
            cursor.execute("SELECT SUM(OutputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (ProductID))
            OutputStock=cursor.fetchone()[0]
            logger.info(OutputStock)
        StockBalance=int(InputStock)-int(OutputStock)
        logger.info(StockBalance)
        cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,WarehouseID=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s""",
        (StockBalance,Warehouse,LastUpdateOn,LastUpdateBy,ProductID))
        #cursor.execute("""UPDATE blog_txadjustmentstock_txstock SET StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s WHERE ProductID=%s""",
        #(InputStock,OutputStock,StockBalance,ProductID))
        cursor.execute("""UPDATE blog_txstocksn SET SNStatus=%s WHERE ProductID=%s AND AdjustmentStockID=%s""",
        (AdjustmentType,ProductID,StockID,))
    #return render(request, 'ViewAdjustmentStock.html',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
    #return render_to_response('ViewAdjustmentStock.html',{'UserRole':userrole,'ProductID':MsProduct.objects.filter(ProductStatus='Active'),'WarehouseName':WareHouse.objects.filter(WarehouseStatus='Active'),'full_name':request.user.first_name})
    return HttpResponse(StockBalance)



def Delete_Adjustment_StockList_View(request,uid):
    userrole=get_role(request.user.email)
    SNID=uid
    logger.info(SNID)
    cursor = connection.cursor()
    cursor.execute("SELECT ProductID from blog_txadjustmentstock_dtl where id=('%s')" % (uid))
    StockProductID=cursor.fetchone()[0]
    logger.info(StockProductID)
    cursor.execute("SELECT AdjustmentStockID from blog_txadjustmentstock_dtl where id=('%s')" % (uid))
    AdjustmentStockID=cursor.fetchone()[0]
    logger.info(AdjustmentStockID)
    return render(request, 'DeleteAdjustmentStocklist.html',{'delstckProductid':StockProductID,'AdjustmentStockID':AdjustmentStockID,'SNID':SNID,'UserRole':userrole,'full_name':request.user.first_name})


def Delete_Adjustment_StockList(request):
    #userrole=get_role(request.user.email)
    uid=request.GET.get('uid')
    logger.info(uid)
    dbProductID=request.GET.get('StocklistProductID')
    logger.info(dbProductID)
    InputStock=''
    OutputStock=''
    AdjustmentID=''
    StockBalance=''
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("SELECT AdjustmentType from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
    AdjustmentType=cursor.fetchone()[0]
    if AdjustmentType=='IN':
        cursor.execute("SELECT InputStockQty from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
        InputStockqnty=cursor.fetchone()[0]
        logger.info(InputStockqnty)
        cursor.execute("SELECT AdjustmentStockID from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
        AdjustmentID=cursor.fetchone()[0]
        logger.info(AdjustmentID)
        cursor.execute("SELECT SerialStatus from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
        SerialStatus=cursor.fetchone()[0]
        logger.info(SerialStatus)
        if SerialStatus=='No':
            TxAdjustmentStock_Dtl.objects.filter(id=uid).delete()
            cursor.execute("SELECT SUM(InputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (dbProductID))
            InputStock=cursor.fetchone()[0]
            logger.info(InputStock)
            cursor.execute("SELECT SUM(OutputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (dbProductID))
            OutputStock=cursor.fetchone()[0]
            logger.info(OutputStock)
            if InputStock!=None or OutputStock!=None:
                StockBalance=int(InputStock)-int(OutputStock)
                logger.info(StockBalance)
                cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s""",
                (StockBalance,LastUpdateOn,LastUpdateBy,dbProductID))
            #cursor.execute("""UPDATE blog_txadjustmentstock_txstock SET StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s WHERE ProductID=%s""",
            #(InputStock,OutputStock,StockBalance,dbProductID))
        else:
            if SerialStatus=='Yes':
                cursor.execute("SELECT GROUP_CONCAT(SerialNumber) from blog_txstocksn where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                SerialNumbersList=cursor.fetchone()[0]
                logger.info(SerialNumbersList)
                if SerialNumbersList==None:
                    TxAdjustmentStock_Dtl.objects.filter(id=uid).delete()
                    InputStock=0
                    OutputStock=0
                else:
                    myList = [int(x) for x in SerialNumbersList.split(',') if x]
                    logger.info(myList)
                    deleteserialcount=len(myList)
                    logger.info(deleteserialcount)
                    TxStockSN.objects.filter(SerialNumber__in=(myList)).delete()
                    TxAdjustmentStock_Dtl.objects.filter(id=uid).delete()
                    cursor.execute("SELECT SUM(InputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                    InputStock=cursor.fetchone()[0]
                    logger.info(InputStock)
                    cursor.execute("SELECT SUM(OutputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                    OutputStock=cursor.fetchone()[0]
                    logger.info(OutputStock)
                    if InputStock!=None or OutputStock!=None:
                        StockBalance=int(InputStock)-int(OutputStock)
                        logger.info(StockBalance)
                        cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s""",
                        (StockBalance,LastUpdateOn,LastUpdateBy,dbProductID))
            #cursor.execute("""UPDATE blog_txadjustmentstock_txstock SET StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s WHERE ProductID=%s""",
            #(InputStock,OutputStock,StockBalance,dbProductID))
    else:
        if AdjustmentType=='OUT':
            cursor.execute("SELECT OutputStockQty from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
            OutputStockqnty=cursor.fetchone()[0]
            logger.info(OutputStockqnty)
            cursor.execute("SELECT AdjustmentStockID from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
            AdjustmentID=cursor.fetchone()[0]
            logger.info(AdjustmentID)
            cursor.execute("SELECT SerialStatus from blog_txadjustmentstock_dtl where id=('%s') AND ProductID=('%s')" % (uid,dbProductID))
            SerialStatus=cursor.fetchone()[0]
            logger.info(SerialStatus)
            if SerialStatus=='No':
                TxAdjustmentStock_Dtl.objects.filter(id=uid).delete()
                cursor.execute("SELECT SUM(InputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                InputStock=cursor.fetchone()[0]
                logger.info(InputStock)
                cursor.execute("SELECT SUM(OutputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                OutputStock=cursor.fetchone()[0]
                logger.info(OutputStock)
                if InputStock!=None or OutputStock!=None:
                    StockBalance=int(InputStock)-int(OutputStock)
                    logger.info(StockBalance)
                    cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s""",
                    (StockBalance,LastUpdateOn,LastUpdateBy,dbProductID))
                #cursor.execute("""UPDATE blog_txadjustmentstock_txstock SET StockQtyIN=%s,StockQtyOut=%s,StockQtyBalance=%s WHERE ProductID=%s""",
                #(InputStock,OutputStock,StockBalance,dbProductID))
            else:
                if SerialStatus=='Yes':
                    cursor.execute("SELECT GROUP_CONCAT(SerialNumber) from blog_txstocksn where ProductID=('%s') AND AdjustmentStockID=('%s')" % (dbProductID,AdjustmentID))
                    SerialNumbersList=cursor.fetchone()[0]
                    logger.info(SerialNumbersList)
                    if SerialNumbersList==None:
                        TxAdjustmentStock_Dtl.objects.filter(id=uid).delete()
                        InputStock=0
                        OutputStock=0
                    else:
                        myList = [int(x) for x in SerialNumbersList.split(',') if x]
                        logger.info(myList)
                        deleteserialcount=len(myList)
                        logger.info(deleteserialcount)
                        TxStockSN.objects.filter(SerialNumber__in=(myList)).delete()
                        TxAdjustmentStock_Dtl.objects.filter(id=uid).delete()
                        cursor.execute("SELECT SUM(InputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (dbProductID))
                        InputStock=cursor.fetchone()[0]
                        logger.info(InputStock)
                        cursor.execute("SELECT SUM(OutputStockQTY) from blog_txadjustmentstock_dtl where ProductID=('%s')" % (dbProductID))
                        OutputStock=cursor.fetchone()[0]
                        logger.info(OutputStock)
                        if InputStock!=None or OutputStock!=None:
                            StockBalance=int(InputStock)-int(OutputStock)
                            logger.info(StockBalance)
                            cursor.execute("""UPDATE blog_txadjustmentstock_hdr SET IOStockBalance=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE ProductID=%s""",
                            (StockBalance,LastUpdateOn,LastUpdateBy,dbProductID))
    obj=TxAdjustmentStock_Dtl.objects.filter(ProductID=dbProductID).values_list('AdjustmentType','InputOutput','WarehouseID','SerialStatus','id','OutputStockQty')
    getdata=json.dumps(list(obj))
    logger.info(getdata)
    data=str(StockBalance) + '.' + getdata
    logger.info(data)                        
    return HttpResponse(data)

def SNStatus_Validation_Lable(request):
    ProductIDfrompage=request.GET.get('val')
    cursor = connection.cursor()
    cursor.execute("SELECT ProductSerialNumber from blog_msproduct where ProductID=('%s')" % (ProductIDfrompage))
    SerialNumberStatus=cursor.fetchone()[0]
    Data=SerialNumberStatus
    return HttpResponse(Data)
	
def Adjustment_SNDeleteCheck_Details(request):
    AdjstmntID=request.GET.get('AdjustmentID')
    ProductID=request.GET.get('ProductID')
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_CONCAT(SerialNumber) from blog_txstocksn where ProductID=('%s') AND RefNumber=('%s')" % (ProductID,AdjstmntID))
    SerialNumbersList=cursor.fetchone()[0]
    logger.info(SerialNumbersList)
    myList = [x for x in SerialNumbersList.split(',') if x]
    logger.info(myList)
    TxStockSN.objects.filter(SerialNumber__in=(myList)).delete()
    obj=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=AdjstmntID).values_list('SerialNumber')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)



#--------------------------------------------------ShipmentToCustomer-------------------------------------------------------------------------------------

def GetDistributor_Details(request):
    DistributorID=request.GET.get('DistributorID')
    cursor = connection.cursor()
    cursor.execute("SELECT ThirdPartyName,ThirdPartyAddress,ThirdPartyCiy,ThirdPartyCountry  FROM blog_thirdparty where ThirdPartyID=('%s')" % (DistributorID))
    DistributorDetails=cursor.fetchone()
    Data=DistributorDetails[0] + ':' + DistributorDetails[1] + ':' + DistributorDetails[2] + ':'  + DistributorDetails[3]
    return HttpResponse(Data)

def GetCustomer_Details(request):
    CustomerID=request.GET.get('CustomerID')
    cursor = connection.cursor()
    cursor.execute("SELECT ThirdPartyName,ThirdPartyAddress,ThirdPartyCiy,ThirdPartyCountry  FROM blog_thirdparty where ThirdPartyID=('%s')" % (CustomerID))
    CustomerDetails=cursor.fetchone()
    Data=CustomerDetails[0] + ':' + CustomerDetails[1] + ':' + CustomerDetails[2] + ':'  + CustomerDetails[3]
    return HttpResponse(Data)

def GetDeviceSN_Details(request):
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    Product_SN=''
    cursor = connection.cursor()
    if TxShipmentToCustomer_Dtl.objects.all().count()>0:
	cursor.execute("SET SESSION group_concat_max_len = 1000000")
	cursor.execute("SELECT GROUP_CONCAT(Product_SN) FROM blog_txshipmenttocustomer_dtl")
	Product_SN=cursor.fetchone()[0]
	logger.info(Product_SN)
    Product_SNList = [x for x in Product_SN.split(',') if x]
    logger.info(Product_SNList)
    obj=TxStockSN.objects.filter(ProductID=ProductID).filter(SNStatus='IN').exclude(SerialNumber__in=Product_SNList).values_list('SerialNumber')
    getdata = json.dumps(list(obj))
    logger.info(getdata)
    return HttpResponse(getdata)

def GetDeviceSNList_Details(request):
    ListData=request.GET.get('ListData')
    ProductID=request.GET.get('ProductID')
    ProductName=request.GET.get('ProductName')
    RefNumber=request.GET.get('RefNumber')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    #Product_SNList="['" + ListData.replace(',',"','") + "']"
    Product_SNList = [x for x in ListData.split(',') if x]
    logger.info(Product_SNList)
    ValidationMessage=''
    getdata=''
    for i in Product_SNList:
        logger.info(i)
        if TxSAM.objects.filter(Product_SN=i).count()==0:
            ValidationMessage='Product_SN is not yet ready to ship to customer, please check again'
        else:
            if TxStockSN.objects.filter(ProductID=ProductID).filter(SerialNumber=i).filter(SNStatus='OUT').count()== 0:
                cursor.execute("""INSERT INTO blog_txstocksn(ProductID,ProductName,ProductType,SerialNumber,SNStatus,RefNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,ProductName,"Finish Good",i,'OUT',RefNumber,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
                cursor.execute("""INSERT INTO blog_txshipmenttocustomer_dtl(ShipToCustomerID,ProductID,ProductName,Product_SN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,ProductID,ProductName,i,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            obj=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber=RefNumber).values_list('SerialNumber')
            getdata = json.dumps(list(obj))
            logger.info(getdata)
    Data=getdata + '.' + ValidationMessage
    return HttpResponse(Data)

def SaveStockInsert_Details(request):
    RefNumber=request.GET.get('RefNumber')
    RefTransaction="Shipment to Customer"
    ProductID=request.GET.get('ProductID')
    ProductName=request.GET.get('ProductName')
    DistributorID=request.GET.get('DistributorID')
    logger.info(DistributorID)
    DistributorName=request.GET.get('DistributorName')
    CustomerID=request.GET.get('CustomerID')
    logger.info(CustomerID)
    CustomerName=request.GET.get('CustomerName')
    logger.info(CustomerName)
    ShipDate=request.GET.get('ShipDate')
    ListData=request.GET.get('ListData')
    Product_SNList = [x for x in ListData.split(',') if x]
    logger.info(Product_SNList)
    SQuantity=request.GET.get('SQuantity')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    Data='Success'
    if DistributorID == '':
        Data='Please select Distributor ID'
    else:
        if TxShipmentToCustomer_Hdr.objects.filter(ShipToCustomerID=RefNumber).count()>0:
            cursor.execute("""UPDATE blog_txshipmenttocustomer_hdr SET ShipQty=%s,Status=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  ShipToCustomerID=%s""",(SQuantity,'Shipped',LastUpdateOn,LastUpdateBy,RefNumber))
        else:
            cursor.execute("""INSERT INTO blog_txshipmenttocustomer_hdr(ShipToCustomerID,RefTransaction,DistributorID,CustomerID,ProductID,DistributorName,CustomerName,ProductName,ShipDate,ShipQty,Status,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,DistributorID,CustomerID,ProductID,DistributorName,CustomerName,ProductName,ShipDate,SQuantity,'Shipped',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            for i in Product_SNList:
                if TxShipmentToCustomer_Dtl.objects.filter(ShipToCustomerID=RefNumber).filter(Product_SN=i).count()==0:
                    cursor.execute("""INSERT INTO blog_txshipmenttocustomer_dtl(ShipToCustomerID,ProductID,Product_SN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,ProductID,i,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            logger.info(Product_SNList)
        for i in Product_SNList:
            logger.info(i)
            if TxSAM.objects.filter(Product_SN=i).count()>0:
                cursor.execute("""UPDATE blog_txsam SET CustomerID=%s,DistributorID=%s,EndCustomerName=%s,DistributorName=%s,DataExportQty=%s,DataExportStatus=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  Product_SN=%s""",
                (CustomerID,DistributorID,CustomerName,DistributorName,'0','Open',LastUpdateOn,LastUpdateBy,i))
                cursor.execute("Select RefNumber from blog_txstocksn where SNStatus='IN' and  SerialNumber=('%s')" % (i))
                ReFNum=cursor.fetchone()
                cursor.execute("Select WarehouseID from blog_txstock where  RefNumber=('%s')" % (ReFNum))
                WarehouseID=cursor.fetchone()
        StockQtyBalance=0-int(SQuantity)
        cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,'0',SQuantity,StockQtyBalance,'Yes',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
    return HttpResponse(Data)        
        



def Add_ShipmentToCustomer(request):
    userrole=get_role(request.user.email)
    RNumber=randint(001, 9999)
    ShipToCustomerID='STC' + str(RNumber)
    RefNumber=request.POST.get('RefNumber')
    RefTransaction="Shipment to Customer"
    DistributorID=request.POST.get('DistributorID')
    CustomerID=request.POST.get('CustomerID')
    ProductID=request.POST.get('ProductID')
    ProductName=request.POST.get('PName')
    DistributorName=request.POST.get('DistributorName')
    CustomerName=request.POST.get('CustomerName')
    ShipDate=request.POST.get('ShipDate')
    SQuantity=request.POST.get('SQuantity')
    ShipmentStatus=request.POST.get('ShipmentStatus')
    Product_SNList=request.POST.getlist('PurchaseCheck')
    logger.info(Product_SNList)
    Remarks=request.POST.get('Remarks')
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if DistributorID !=None  and ProductID !=None:
        cursor.execute("""INSERT INTO blog_txshipmenttocustomer_hdr(ShipToCustomerID,RefTransaction,DistributorID,CustomerID,ProductID,DistributorName,CustomerName,ProductName,ShipDate,ShipQty,Status,Remarks,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,RefTransaction,DistributorID,CustomerID,ProductID,DistributorName,CustomerName,ProductName,ShipDate,SQuantity,ShipmentStatus,Remarks,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        #for i in Product_SNList:
            #cursor.execute("""INSERT INTO blog_txshipmenttocustomer_dtl(ShipToCustomerID,ProductID,ProductName,Product_SN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
           # VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(ShipToCustomerID,ProductID,ProductName,i,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))           
        return render(request,'ViewShipmentToCustomer.html',{'obj':TxShipmentToCustomer_Hdr.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})
    else:
        return render(request,'AddShipmentToCustomer.html',{'RefNumber':ShipToCustomerID,'PType':MsProduct.objects.filter(ProductType='Finish Good').filter(ProductStatus='Active'),'DistributorID':ThirdParty.objects.filter(ThirdPartyType='Distributor').filter(ThirdPartyStatus='Active'),'CustomerID':ThirdParty.objects.filter(ThirdPartyType='Customer').filter(ThirdPartyStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})


def View_ShipmentToCustomer(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	return HttpResponseRedirect('/accounts/login/')
    else:
	ProductList = TxShipmentToCustomer_Hdr.objects.raw('SELECT id,ShipDate,ProductID,ProductName,DistributorName,DistributorName,SUM(ShipQty) AS ShipQty FROM blog_txshipmenttocustomer_hdr GROUP BY DistributorName,CustomerName')
	return render(request,'ViewShipmentToCustomer.html',{'obj':ProductList,'UserRole':userrole,'full_name':request.user.first_name})

def Edit_ShipmentToCustomer(request,u_id):
    userrole=get_role(request.user.email)
    CustomerDetails=''
    CustomerAddress=''
    CustomerCity=''
    CustomerCountry=''
    STCList = TxShipmentToCustomer_Hdr.objects.raw('SELECT * FROM blog_txshipmenttocustomer_hdr where id =%s',[u_id])
    for s in STCList:
        cursor = connection.cursor()
        cursor.execute("SELECT CustomerID  FROM blog_txshipmenttocustomer_hdr where id=('%s')" % (u_id))
        CustomerID=cursor.fetchone()[0]
        if CustomerID!='':
            cursor.execute("SELECT ThirdPartyAddress,ThirdPartyCiy,ThirdPartyCountry  FROM blog_thirdparty where ThirdPartyID=('%s')" % (s.CustomerID))
            CustomerDetails=cursor.fetchone()
            CustomerAddress=CustomerDetails[0]
            CustomerCity=CustomerDetails[1]
            CustomerCountry=CustomerDetails[2]
        cursor.execute("SELECT ThirdPartyAddress,ThirdPartyCiy,ThirdPartyCountry  FROM blog_thirdparty where ThirdPartyID=('%s')" % (s.DistributorID))
        DistributorDetails=cursor.fetchone()
        DistributorAddress=DistributorDetails[0]
        DistributorCity=DistributorDetails[1]
        DistributorCountry=DistributorDetails[2]
        cursor.execute("SELECT ProductModel  FROM blog_msproduct where ProductID=('%s')" % (s.ProductID))
        ProductModel=cursor.fetchone()[0]
        if request.user.username == '':
	    return HttpResponseRedirect('/accounts/login/')
	else:
            logger.info(s.ProductID)
            logger.info(s.ShipToCustomerID)
            cursor.execute("SELECT GROUP_CONCAT(Product_SN)  FROM blog_txshipmenttocustomer_dtl where ShipToCustomerID=('%s')" % (s.ShipToCustomerID))
            DeviceList=cursor.fetchone()[0]
            logger.info(DeviceList)
	    return render(request, 'EditShipmentToCustomer.html',{'lblSTDID':u_id,
                                                                  'RefNumber':s.ShipToCustomerID,
                                                                  'DistributorID':s.DistributorID,
                                                                  'DistributorName':s.DistributorName,
                                                                  'DistributorAddress':DistributorAddress,
                                                                  'DistributorCity':DistributorCity,
                                                                  'DistributorCountry':DistributorCountry,
                                                                  'CustomerID':s.CustomerID,
                                                                  'CustomerName':s.CustomerName,
                                                                  'CustomerAddress':CustomerAddress,
                                                                  'CustomerCity':CustomerCity,
                                                                  'CustomerCountry':CustomerCountry,
                                                                  'ProductID':s.ProductID,
                                                                  'PName':s.ProductName,
                                                                  'PModel':ProductModel,
                                                                  'ShipDate':s.ShipDate,
                                                                  'SQuantity':s.ShipQty,
                                                                  'ShipmentStatus':s.Status,
                                                                  'Remarks':s.Remarks,
                                                                  'DeviceList':DeviceList,
                                                                  'DeviceSNData':TxStockSN.objects.filter(ProductID=s.ProductID).filter(SNStatus='IN'),
                                                                  'DeviceData':TxShipmentToCustomer_Dtl.objects.filter(ShipToCustomerID=s.ShipToCustomerID),
                                                                  'UserRole':userrole,
                                                                  'full_name':request.user.first_name
                                                                  })        
def Update_ShipmentToCustomer(request):
    userrole=get_role(request.user.email)
    lblSTDID=request.POST.get('lblSTDID')
    ShipDate=request.POST.get('ShipDate')
    SQuantity=request.POST.get('SQuantity')
    ShipmentStatus=request.POST.get('ShipmentStatus')
    now=datetime.now()
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("""UPDATE blog_txshipmenttocustomer_hdr SET ShipDate=%s,ShipQty=%s,Status=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  id=%s""",(ShipDate,SQuantity,ShipmentStatus,LastUpdateOn,LastUpdateBy,lblSTDID))
    return render(request,'ViewShipmentToCustomer.html',{'obj':TxShipmentToCustomer_Hdr.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})

def DetailCount_Details(request):
    RefNumber=request.GET.get('RefNumber')
    count=TxShipmentToCustomer_Dtl.objects.filter(ShipToCustomerID=RefNumber).count()
    cursor = connection.cursor()
    cursor.execute("SET SESSION group_concat_max_len = 1000000")
    cursor.execute("SELECT GROUP_CONCAT(Product_SN)  FROM blog_txshipmenttocustomer_dtl where ShipToCustomerID=('%s')" % (RefNumber))
    DeviceList=cursor.fetchone()[0]
    logger.info(DeviceList)
    Data=str(count) + ':' + str(DeviceList)
    return HttpResponse(Data)      

#-----------------------------------------------------------------Reports-------------------------------------------------------------------------------


def CustomerReport_DataView(request):
    userrole=get_role(request.user.email)
    return render(request,'CustomerDataReport.html',{'obj':ThirdParty.objects.filter(ThirdPartyType='Customer').filter(ThirdPartyStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})


def CustomerReport_Details(request):
    CustomerID=request.GET.get('CustomerID')
    logger.info(CustomerID)
    if CustomerID !='':
        #CustomerIDIN=CustomerID.replace(',',"','")
        #logger.info(CustomerIDIN)
        CustomerIDList = [str(x) for x in CustomerID.split(',') if x]
        logger.info(CustomerIDList)
        xml = render_to_string('Customer_template.xml', {'query_set':ThirdParty.objects.filter(ThirdPartyID__in=CustomerIDList)})
        logger.info(xml)
        filename=str(time()).replace('.','_')
        logger.info(filename)
        f = open('/opt/BIMSDevelopment/Production/BCAT/AssetManagment/blog/static/files/xmlfiles/'+filename+'.xml','w')
        myfile = File(f)
        myfile.write(xml)
        myfile.close()
        Data=filename
        cursor = connection.cursor()
        CustomerIDList = CustomerID.split(",")
        logger.info(CustomerIDList)
        for i in CustomerIDList:
            logger.info(i)
            cursor.execute("SELECT DataExportQty  FROM blog_thirdparty where ThirdPartyID =('%s')" % (i))
            DQty=cursor.fetchone()[0]
            logger.info(DQty)
            DataEty=int(DQty)+1
            cursor.execute("UPDATE blog_thirdparty SET DataExportStatus='%s',DataExportQty='%s' WHERE  ThirdPartyID =('%s')" % ('Yes',DataEty,i))
    else:
        Data='Please select the checkbox'
    return HttpResponse(Data)


def DistributorReport_DataView(request):
    userrole=get_role(request.user.email)
    return render(request,'DistributorDataReport.html',{'obj':ThirdParty.objects.filter(ThirdPartyType='Distributor').filter(ThirdPartyStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})


def DistributorReport_Details(request):
    DistributorID=request.GET.get('DistributorID')
    logger.info(DistributorID)
    Data=''
    if DistributorID !='':
        DistributorIDList = [str(x) for x in DistributorID.split(',') if x]
        xml = render_to_string('Distributor_template.xml', {'query_set':ThirdParty.objects.filter(id__in=DistributorIDList)})
        logger.info(xml)
        filename=str(time()).replace('.','_')
        logger.info(filename)
        f = open('/opt/BIMSDevelopment/Production/BCAT/AssetManagment/blog/static/files/xmlfiles/'+filename+'.xml','w')
        myfile = File(f)
        myfile.write(xml)
        myfile.close()
        Data=filename
        cursor = connection.cursor()
        DistributorList = DistributorID.split(",")
        logger.info(DistributorList)
        for i in DistributorList:
            logger.info(i)
            cursor.execute("SELECT DataExportQty  FROM blog_thirdparty where id=('%s')" % (i))
            DQty=cursor.fetchone()[0]
            DataEty=int(DQty)+1
            cursor.execute("""UPDATE blog_thirdparty SET DataExportStatus=%s,DataExportQty=%s WHERE  id=%s""",('Yes',DataEty,i))
    else:
        Data='Please select the checkbox'
    return HttpResponse(Data)

def DeviceReport_DataView(request):
    userrole=get_role(request.user.email)
    return render(request,'DeviceDataReport.html',{'obj':TxSAM.objects.exclude(DataExportStatus='No'),'UserRole':userrole,'full_name':request.user.first_name})

def DeviceReport_Details(request):
    DeviceID=request.GET.get('DeviceID')
    Data=''
    if DeviceID !='':
        DeviceIDList = [str(x) for x in DeviceID.split(',') if x]
        xml = render_to_string('Device_template.xml', {'query_set':TxSAM.objects.filter(id__in=DeviceIDList)})
        logger.info(xml)
        filename=str(time()).replace('.','_')
        logger.info(filename)
        f = open('/opt/BIMSDevelopment/Production/BCAT/AssetManagment/blog/static/files/xmlfiles/'+filename+'.xml','w')
        myfile = File(f)
        myfile.write(xml)
        myfile.close()
        Data=filename
        cursor = connection.cursor()
        DeviceList = DeviceID.split(",")
        logger.info(DeviceList)
        for i in DeviceList:
            logger.info(i)
            cursor.execute("SELECT DataExportQty  FROM blog_txsam where id=('%s')" % (i))
            DQty=cursor.fetchone()[0]
            DataEty=int(DQty)+1
            cursor.execute("""UPDATE blog_txsam SET DataExportStatus=%s,DataExportQty=%s WHERE  id=%s""",('Yes',DataEty,i))
    else:
        Data='Please select the checkbox'
    return HttpResponse(Data)

def ProductionReport_DataView(request):
    userrole=get_role(request.user.email)
    Fromdate=request.POST.get('Fromdate')
    Todate=request.POST.get('Todate')
    logger.info(Fromdate)
    logger.info(Todate)
    if Fromdate!=None and Todate!=None:
        return render(request,'ProductionDataReport.html',{'obj':TxHandOverMaterialHdr.objects.filter(ProductionStatus='Finished').filter(EndProductionDate__range=(Fromdate,Todate)),'UserRole':userrole,'full_name':request.user.first_name})
    else:
        return render(request,'ProductionDataReport.html',{'UserRole':userrole,'full_name':request.user.first_name})


#-----------------------------------------------------------------------------Transfer Location

def Transfer_Stock_Location_View(request):
    userrole=get_role(request.user.email)
    RefNumber=request.POST.get('RefNumber')
    logger.info(RefNumber)
    WarehouseFrom=request.POST.get('WarehouseFrom')
    logger.info(WarehouseFrom)
    ProductID=request.POST.get('ProductID')
    logger.info(ProductID)
    ProductName=request.POST.get('ProductName')
    logger.info(ProductName)
    ProductModel=request.POST.get('ProductModel')
    logger.info(ProductModel)
    ProductType=request.POST.get('ProductType')
    logger.info(ProductType)
    ExistingQuantity=request.POST.get('ExistingQuantity')
    logger.info(ExistingQuantity)
    WarehouseTo=request.POST.get('WarehouseTo')
    logger.info(WarehouseTo)
    TransferQuantity=request.POST.get('TransferQuantity')
    logger.info(TransferQuantity)
    StockBalance=''
    now=datetime.now()
    CreatedOn=str(now)[:10]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:10]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if ProductID !=None and WarehouseFrom !=None:
        cursor.execute("SELECT ProductSerialNumber from blog_msproduct where ProductID=('%s')" % (ProductID))
        SerialStatus=cursor.fetchone()[0]
        logger.info(SerialStatus)
        if SerialStatus=='No':
            StockBalance=0-int(TransferQuantity)
            logger.info(StockBalance)
            cursor.execute("""INSERT INTO blog_txstock(ProductID,RefNumber,RefTransaction,StockQtyIN,StockQtyOut,WarehouseID,StockQtyBalance,ProductName,StockSN,ADJIOStockStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,RefNumber,'TransferLocation','0',TransferQuantity,WarehouseFrom,StockBalance,ProductName,SerialStatus,'Open',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            logger.info("Insert Query")
        cursor.execute("""INSERT INTO blog_txtransfer_location(RefNumber,WarehouseFrom,ProductID,ProductName,ProductModel,ProductType,ExistingQuantity,WarehouseTo,TransferQuantity,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RefNumber,WarehouseFrom,ProductID,ProductName,ProductModel,ProductType,ExistingQuantity,WarehouseTo,TransferQuantity,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        cursor.execute("""INSERT INTO blog_txstock(ProductID,RefNumber,RefTransaction,StockQtyIN,StockQtyOut,WarehouseID,StockQtyBalance,ProductName,StockSN,ADJIOStockStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(ProductID,RefNumber,'TransferLocation',TransferQuantity,'0',WarehouseTo,TransferQuantity,ProductName,SerialStatus,'Open',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
        return render(request, 'ViewLocationTransfer.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':Txtransfer_location.objects.all()})
    return render(request,'TransferStockLocation.html',{'full_name':request.user.first_name,'UserRole':userrole,'WarehouseFrom':WareHouse.objects.all(),'ProductID':MsProduct.objects.all()})


def Transfer_Stock_ProductID_Sorting(request):
    ProductID=request.GET.get('ProductID')
    logger.info(ProductID)
    WarehouseFrom=request.GET.get('WarehouseFrom')
    logger.info(WarehouseFrom)
    Data=''
    ExistingQuantity=''
    ValidationData=''
    cursor = connection.cursor()
    cursor.execute("SELECT ProductName,ProductModel,ProductType,ProductSerialNumber from blog_msproduct where ProductID=('%s')" % (ProductID))
    ProductDetails=cursor.fetchone()
    ProductName=ProductDetails[0]
    logger.info(ProductName)
    ProductModel=ProductDetails[1]
    logger.info(ProductModel)
    ProductType=ProductDetails[2]
    logger.info(ProductType)
    ProductSerialNumber=ProductDetails[3]
    logger.info(ProductSerialNumber)
    cursor.execute("SELECT COUNT(ProductID) FROM blog_txstock where ProductID=('%s') AND WarehouseID=('%s')" % (ProductID,WarehouseFrom))
    ProductIDCount=cursor.fetchone()[0]
    logger.info(ProductIDCount)
    if ProductIDCount>0:
        cursor.execute("SELECT SUM(StockQtyBalance) from blog_txstock where ProductID=('%s') AND WarehouseID=('%s')" % (ProductID,WarehouseFrom))
        ExistingQuantity=cursor.fetchone()[0]
        logger.info(ExistingQuantity)
    else:
        ValidationData='Selected ProductID and WarehouseID is Not Available'
    Data=ProductName + '.' +ProductModel+ '.' +ProductType+ '.' +str(ExistingQuantity)+ '.' +ValidationData+ '.' +ProductSerialNumber
    logger.info(Data)
    return HttpResponse(Data)


def Transfer_Stock_Existing_Stock_Validation(request):
    TransferQuantity=request.GET.get('val')
    logger.info(TransferQuantity)
    ExistingQuantity=request.GET.get('ExistingQty')
    logger.info(ExistingQuantity)
    TransferQty=int(TransferQuantity)
    logger.info(TransferQty)
    ExistingQty=int(ExistingQuantity)
    logger.info(ExistingQty)
    Data=''
    if TransferQty>ExistingQty:
        Data='Transfer Quantity is More Than Existing Quantity'
    else:
        Data=''
    return HttpResponse(Data)


def Transfer_Stock_SerialNumber_Details(request):
    ProductID=request.GET.get('ProductID')
    WarehouseFrom=request.GET.get('WarehouseFrom')
    getdata=''
    stockQty=''
    obj=''
    cursor = connection.cursor()
    if txStock.objects.filter(ProductID=ProductID).filter(WarehouseID=WarehouseFrom).count()>0 :
        cursor.execute("SET SESSION group_concat_max_len = 1000000")
        cursor.execute("SELECT GROUP_CONCAT(RefNumber) FROM blog_txstock where ProductID=('%s') AND WarehouseID=('%s')" % (ProductID,WarehouseFrom))
        RefNumber=cursor.fetchone()[0]
        logger.info(RefNumber)
        RefNumber_List = [x for x in RefNumber.split(',') if x]
        logger.info(RefNumber_List)
        RefNumberIN="'" + RefNumber.replace(',',"','") + "'"
        cursor.execute("SELECT GROUP_CONCAT(SerialNumber) FROM blog_txstocksn WHERE SNStatus ='OUT' AND RefNumber IN(%s)"%(RefNumberIN))
        OutSN=cursor.fetchone()[0]
        logger.info(OutSN)
        if OutSN!=None:
            OutSN_List = [x for x in OutSN.split(',') if x]
            logger.info(OutSN_List)
            cursor.execute("SELECT SUM(StockQtyBalance) FROM blog_txstock where ProductID=('%s') AND WarehouseID=('%s')" % (ProductID,WarehouseFrom))
            StockQtyBalance=cursor.fetchone()[0]
            logger.info(StockQtyBalance)
            stockQty=int(StockQtyBalance)
            logger.info(stockQty)
            if stockQty>0:
                obj=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber__in=RefNumber_List).exclude(SerialNumber__in=OutSN_List).values_list('SerialNumber')
        else:
            cursor.execute("SELECT SUM(StockQtyBalance) FROM blog_txstock where ProductID=('%s') AND WarehouseID=('%s')" % (ProductID,WarehouseFrom))
            StockQtyBalance=cursor.fetchone()[0]
            logger.info(StockQtyBalance)
            stockQty=int(StockQtyBalance)
            logger.info(stockQty)
            if stockQty>0:
                obj=TxStockSN.objects.filter(ProductID=ProductID).filter(RefNumber__in=RefNumber_List).values_list('SerialNumber')
        getdata = json.dumps(list(obj))
        logger.info(getdata)
    data=getdata+ '.' +str(stockQty)
    return HttpResponse(data)


def Checked_SerialNumber_Details(request):
    CheckedSerialNumber=request.GET.get('CheckedSerialNo')
    logger.info(CheckedSerialNumber)
    CheckedSerialNumberIN="'" + CheckedSerialNumber.replace(',',"','") + "'"
    logger.info(CheckedSerialNumberIN)
    ReferenceNo=request.GET.get('ReferenceNo')
    logger.info(ReferenceNo)
    TransferStock=request.GET.get('len')
    logger.info(TransferStock)
    TransferStock=int(TransferStock)
    data=''
    now=datetime.now()
    LastUpdateOn=str(now)[:10]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    if TransferStock !=0:
        SplitedSerialNo = CheckedSerialNumber.split(",")
        logger.info(SplitedSerialNo)
        for i in SplitedSerialNo:
            cursor.execute("SELECT RefNumber FROM blog_txstocksn where SerialNumber=('%s')" % (i))
            RefNum=cursor.fetchone()[0]
            logger.info(RefNum)
            cursor.execute("SELECT StockQtyIN,StockQtyout,StockQtyBalance FROM blog_txstock where RefNumber=('%s')" % (RefNum))
            StockDetails=cursor.fetchone()
            StockQtyIN=StockDetails[0]
            logger.info(StockQtyIN)
            StockQtyout=StockDetails[1]
            logger.info(StockQtyout)
            StockQtyBalance=StockDetails[2]
            logger.info(StockQtyBalance)
            StockQtyIN=int(StockQtyIN)-1
            StockQtyBalance=int(StockQtyBalance)-1
            cursor.execute("""UPDATE blog_txstock SET StockQtyIN=%s,StockQtyBalance=%s,LastUpdateOn=%s,LastUpdateBy=%s WHERE  RefNumber=(%s)""",(StockQtyIN,StockQtyBalance,LastUpdateOn,LastUpdateBy,RefNum))
            cursor.execute("UPDATE blog_txstocksn SET RefNumber=('%s') WHERE SerialNumber=('%s') AND RefNumber=('%s')" % (ReferenceNo,i,RefNum))
    else:
        data='Please Serial Numbers'
    return HttpResponse(data)


def Transfer_StocK_Location_List(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	return HttpResponseRedirect('/accounts/login/')
    else:
	return render_to_response('ViewLocationTransfer.html',{'UserRole':userrole,'full_name':request.user.first_name,'obj':Txtransfer_location.objects.all()})


def Transfer_Location_Warehouse_Validation(request):
    WarehouseFrom=request.GET.get('WarehouseFrom')
    logger.info(WarehouseFrom)
    WarehouseTo=request.GET.get('WarehouseTo')
    logger.info(WarehouseTo)
    Data=''
    if WarehouseFrom==WarehouseTo:
        Data='warehouse from and warehouse to cannot be the same'
    return HttpResponse(Data)

#-------------------------------------------Search------------------------------
def SAMDeviceID(request):
    userrole=get_role(request.user.email)
    if request.user.username == '':
	return HttpResponseRedirect('/accounts/login/')
    else:
		return render(request,'SAMDeviceID.html',{'obj':TxSAM.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})

#-------------------------------------------ReceivingSIMCard------------------------------
def Add_ReceivingSimCard(request):
    userrole=get_role(request.user.email)
    RSamID=request.POST.get('RSamID')
    logger.info(RSamID)
    WarehouseName=request.POST.get('WarehouseName')
    logger.info(WarehouseName)
    RSID=''
    now=datetime.now()
    CreatedOn=str(now)[:19]
    CreatedBy=request.user.first_name
    LastUpdateOn=str(now)[:19]
    LastUpdateBy=request.user.first_name
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blog_msproduct where ProductID=('%s')" % ('SIMCARD01'))
    ProductDetails=cursor.fetchone()
    if ProductDetails!=None:
        ProductID=ProductDetails[1]
        ProductType=ProductDetails[2]
        ProductName=ProductDetails[3]
        ProductModel=ProductDetails[4]
    else:
        return render(request, 'ReceivingSIM.html',{'SAMValue':'Yes','Error':'Please set SIM Card details','WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
    SAMValue='Yes'
    if RSamID != None or WarehouseName != None:
        SAMValue='Yes'
        SIM_SN=request.POST.get('SIMSN')
        logger.info(SIM_SN)
        Mobile_No=request.POST.get('MobileNo')
        logger.info(Mobile_No)
        request.session['RID']=RSamID
        RSID=request.session['RID']
        request.session['RWHouse']=WarehouseName
        RSHouse=request.session['RWHouse']
        if request.POST.get('_AddToSIMList'):
            logger.info("GetLoist Button")
            cursor.execute("""INSERT INTO blog_txsam(ReceivingSAMID,Product_SN,SAM_SN,SAM_UID,WarehouseName,DataExportQty,DataExportStatus,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,'',SIM_SN,Mobile_No,WarehouseName,'0','No',CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            RPersoQty=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
            if TxSAM.objects.filter(ReceivingSAMID=RSamID).count()>0:
                RPersoQuantity=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
            else:
                RPersoQuantity='0'
            cursor.execute("""INSERT INTO blog_txreceivingsam(ReceivingSAMID,ReceivingPersoQty,WarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s)""",(RSamID,RPersoQuantity,WarehouseName,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy))
            if SIM_SN != None:
                cursor.execute("select id from blog_txsam where ReceivingSAMID =('%s') and SAM_SN =('%s')" %(RSamID,SIM_SN))
                SIMID=cursor.fetchone()[0]
                logger.info(SIMID)
                cursor.execute("""INSERT INTO blog_txstocksn(RefNumber,ProductID,ProductName,ProductType,SerialNumber,SNStatus,SAMRefNumber,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,ProductID,ProductName,ProductType,SIM_SN,'IN',SIMID,CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy))
                return render(request, 'ReceivingSIM.html',{'RPersoQty':RPersoQty,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'obj':TxSAM.objects.filter(ReceivingSAMID=RSID),'RSID':RSID,'RSHouse':RSHouse,'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
            else:
                return render(request, 'ReceivingSIM.html',{'RPersoQty':RPersoQty,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'RSID':RSID,'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})
        else:
            if ProductID != None:
                if TxSAM.objects.filter(ReceivingSAMID=RSamID).count()>0:
                    RPersoQuantity=TxSAM.objects.filter(ReceivingSAMID=RSamID).count()
                else:
                    RPersoQuantity='0'
                cursor.execute("""INSERT INTO blog_txstock(RefNumber,RefTransaction,WarehouseID,ProductID,ProductName,StockQtyIN,StockQtyOut,StockQtyBalance,StockSN,CreatedOn,CreatedBy,LastUpdateOn,LastUpdateBy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(RSamID,"ReceivingSAM",WarehouseName,ProductID,ProductName,RPersoQuantity,'0',RPersoQuantity,'Yes',CreatedOn[:10],CreatedBy,LastUpdateOn[:10],LastUpdateBy)) 
            return render(request, 'ViewReceivingSAMCard.html',{'obj':TxSAM.objects.all(),'UserRole':userrole,'full_name':request.user.first_name})
    else:
        return render(request, 'ReceivingSIM.html',{'RSID':RSID,'ProductID':ProductID,'ProductType':ProductType,'ProductName':ProductName,'ProductModel':ProductModel,'SAMValue':SAMValue,'WHName':WareHouse.objects.filter(WarehouseStatus='Active'),'UserRole':userrole,'full_name':request.user.first_name})


def GetSIMDuplicate_Details(request):
    SIMSN=request.GET.get('SIMSN')
    MobileNo=request.GET.get('MobileNo')
    ValidationData=''
    if SIMSN != None:
        if TxSAM.objects.filter(SAM_SN=SIMSN).count()>0:
            ValidationData='Data with same Serial Number already exist, please check again'
    if MobileNo != None:
        if TxSAM.objects.filter(SAM_UID=MobileNo).count()>0:
            ValidationData='Data with same Mobile number already exist, please check again'
    return HttpResponse(ValidationData)


def SIMSNTest_Details(request):
    SAMSN=request.GET.get('val')
    logger.info(SAMSN)
    ProductID=request.GET.get('ProductID')
    cursor = connection.cursor()
    Data=''
    SAMPINFile=''
    SAMUID=''
    if TxSAM.objects.filter(SAM_SN=SAMSN).count()>0:
        if TxHandOverMaterialHdr.objects.filter(SAM_SN=SAMSN).count() >0:
            Data='SAM SN is not available or already used by another Device / Product SN, please check once again'
        else:
            cursor.execute("SELECT ReceivingSAMID FROM  blog_txsam WHERE SAM_SN=('%s')" % (SAMSN))
            RecevingSAMID=cursor.fetchone()[0]
            logger.info(RecevingSAMID)
            if TxStockSN.objects.filter(RefNumber=RecevingSAMID).filter(SerialNumber=SAMSN).count()>0:
                cursor.execute("SELECT ProductID FROM  blog_txstocksn WHERE SerialNumber=('%s')" % (SAMSN))
                ProductID=cursor.fetchone()[0]
                logger.info(ProductID)
                if ProductID=='SAMCARD01':
                    cursor.execute("SELECT SAMpinFile FROM  blog_txsam WHERE SAM_SN=('%s') and ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
                    SAMPINFile=cursor.fetchone()[0]
                    logger.info(SAMPINFile)
                    cursor.execute("SELECT SAM_UID FROM  blog_txsam WHERE SAM_SN=('%s') and ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
                    SAMUID=cursor.fetchone()[0]
                    logger.info(SAMUID)
                else:
                    cursor.execute("SELECT SAM_UID FROM  blog_txsam WHERE SAM_SN=('%s') and ReceivingSAMID=('%s')" % (SAMSN,RecevingSAMID))
                    SAMUID=cursor.fetchone()[0]
                    logger.info(SAMUID)
                    SAMPINFile=''
    else:
        Data='SAM SN is not available or already used by another Device / Product SN, please check once again'
    getdata=Data + ':' + SAMPINFile + ':' + SAMUID
    logger.info(getdata)
    return HttpResponse(getdata)

