import json
from django.contrib.auth.decorators import login_required
from multiprocessing import context
from sklearn import preprocessing
from django.views.decorators.csrf import csrf_exempt
import pandas, numpy, pickle
from django.shortcuts import render, redirect
from .models import PatientData,FormData, PredictedData,SensorData
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Signup
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('myapp:signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('myapp:signup')
            else:
                myuser = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password,is_staff=True,is_superuser=False,is_active=True)
                
                myuser.save()
                
                return redirect('myapp:loginpage')
        else:
            messages.info(request, 'Password is not the same')
            return redirect('myapp:signup')
    else:
        return render(request, 'signup.html')

#Login
def loginpage(request):
    if request.method == "POST":
        
        userid = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = userid, password = password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('myapp:index')
            else:    
                login(request, user)
                return redirect('myapp:home')
            
               
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('myapp:loginpage')

    else:
        return render(request, 'loginpage.html')
        

#Home
# @login_required
def home(request):
    return render(request, 'home.html')

#About
@login_required
def about(request):
    return render(request, 'about.html')

#Results
# @login_required
def results(request):
    return render(request, 'results.html')

# @login_required
@csrf_exempt
def patientreport(request):
    global pred_pat,sens_pat,pats_pat
    if request.method == 'POST':
        name= request.POST.get('patname')
        contact= request.POST.get('contact')
        
        # print(name)
        # print(contact)

        if PredictedData.objects.filter(name= name ).exists():
            pred=PredictedData.objects.filter(name= name )
            for pat in pred:
                # print(pat.detail())
                pred_pat=pat.detail()
                pred_pat1=pat.detail1()
                pred_pat2=pat.detail2()
        else:
            messages.info(request, 'Patient has not tested stroke prediction!')
            return redirect('myapp:patientreport')
        
        if FormData.objects.filter(name= name ).exists():
            fd=FormData.objects.filter(name= name )
            for pat in fd:
                # print(pat.detail())
                f_pat=pat.detail()
                
        else:
            messages.info(request, 'Patient has not tested stroke prediction!')
            return redirect('myapp:patientreport')

        if SensorData.objects.filter(name= name ).exists():
            sens=SensorData.objects.filter(name= name )
            for pat in sens:
                # print(pat.detail())
                sens_pat=pat.detail()
                sens_pat1=pat.detail1()
        else:
            messages.info(request, 'Patient has not used the platform!')
            return redirect('myapp:patientreport')        
            
        if PatientData.objects.filter(contact=contact):
            pats=PatientData.objects.filter(contact= contact)
            for pat in pats:
                # print(pat.detail())  
                pats_pat=pat.detail() 
                pats_pat1=pat.detail1() 
                
        else:
            messages.info(request, 'Patient does not exist!')
            return redirect('myapp:patientreport') 
          
        return render(request, 'patientreport.html',{'patients':PatientData.objects.all(),'pred_pat':pred_pat,'pred_pat1':pred_pat1,'pred_pat2':pred_pat2,'sens_pat':sens_pat,'sens_pat1':sens_pat1,'pats_pat':pats_pat,'pats_pat1':pats_pat1,'f_pat':f_pat})
    else:
        return render(request, 'patientreport.html',{'patients':PatientData.objects.all()})


#Register Patient
@login_required
def registerpatient(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        # dob= request.POST.get('dob')
        age= request.POST.get('age')
        address= request.POST.get('address')
        contact= request.POST.get('contact')
        email= request.POST.get('email')
        pat = PatientData(name=name,  age=age, address=address, contact=contact, email=email)
        
        pat.save()
        messages.info(request, 'Patient Registered!')
        return redirect('myapp:registerpatient')
    else:
        return render(request, 'registerpatient.html')



#encoding
def ohe_enc(df):
    ohe_col=pickle.load(open('ohe_col1.pkl','rb'))
    # print("ohe_col: ",ohe_col)
    cat_columns=['gender','hypertension','heart_disease','ever_married','work_type','Residence_type','smoking_status']
    # print("cat_col: ",cat_columns)   
    df_processed= pandas.get_dummies(df, columns=cat_columns)
    # print("df_processed: ",df_processed)
    newdict={}
    for i in ohe_col:
        if i in df_processed.columns:
            newdict[i]=df_processed[i].values
        else:
            newdict[i]=0
      
    newdf=pandas.DataFrame(newdict) 
    # newdf.to_csv("/Users/macbookair/Desktop/e.csv")
    # print ("newdf: ",newdf)
    return newdf           


#predict from model
def strokePrediction(unit):

    model=pickle.load(open('model_pickled1.pkl','rb'))
    y_pred=model.predict(unit)
    newdf1=pandas.DataFrame(y_pred,columns=['Stroke Status : '])
    newdf1=newdf1.replace({0:'No Stroke Risk',1:'Stroke Risk'})

    return newdf1



#prediction form
@login_required
def predictionform(request):
    if request.method == 'POST':

        patname=request.POST.get('patname')
        
        patientname=PatientData.objects.get(name=patname)    
        # request.session['patname'] = patname
        gender= request.POST.get('gender')
        age= request.POST.get('age')
        hypertension= request.POST.get('hypertension')
        heart_disease= request.POST.get('heart_disease')
        ever_married= request.POST.get('ever_married')
        work_type= request.POST.get('work_type')
        Residence_type= request.POST.get('Residence_type')
        avg_glucose_level= request.POST.get('avg_glucose_level')
        heartrate= request.POST.get('heartrate')
        # bmi=35
        # heartrate=76
      
        smoking_status= request.POST.get('smoking_status')
        FormData.objects.create(
             name=patientname,gender=gender,age=age, hypertension=hypertension, heart_disease=heart_disease,ever_married=ever_married,work_type=work_type,Residence_type=Residence_type,avg_glucose_level=avg_glucose_level,smoking_status=smoking_status,heartrate=heartrate)
        global obesity
        #sensor data 
        # print("mv",valjson)
        # test(request)
        # queryset=SensorData.objects.all()

        # for object in queryset:
        #     if object.name == patientname:
        #        print(object.name)
        #        print(object.heart_rate)
        # heartrate=90
        height=ht
        weight=wt
        # print("mh",height)
        # print("mw",weight)
        SensorData.objects.create(name=patientname,height = height, weight=weight)
        # sensdat.save()
        # valjson={'heartrate':'90','weight':'89','height':'1.66'}
        # if(valjson):
        #   heartrate = valjson['heartrate']
        #   weight= valjson['weight1']
        #   height= valjson['height1']
        weight=float(weight)
        height=float(height)
        bmi=weight/((height)*(height))
        bmi=round(bmi,2)
        #   print(bmi)

        if bmi< 18.5:
            obesity= 'Underweight'
        elif bmi>=18.5 and bmi<=24.9:
            obesity='Normal'
        elif bmi>=25 and bmi<=29.9:
            obesity='Overweight'
        elif bmi>=30 and bmi<=34.9:
            obesity='Obesity I' 
        elif bmi>=35 and bmi<=39.9:
            obesity='Obesity II' 
        else :
            obesity='Severe Obesity'  
        #   print(obesity)
        bodyfat= (1.2*bmi)+(0.23*float(age))-1.62
        bodyfat=round(bodyfat,2)
        # print(bodyfat,"%")
        # print("mathi",hr)
        # heartrate=hr
        
        myDict=dict(gender=gender,age=age, hypertension=hypertension, heart_disease=heart_disease,ever_married=ever_married,work_type=work_type,Residence_type=Residence_type,avg_glucose_level=avg_glucose_level,bmi=bmi,heartrate=heartrate,smoking_status=smoking_status)
        
        # print(myDict['gender'])
        df=pandas.DataFrame(myDict,index=[0]) 
      
        answer=strokePrediction(ohe_enc(df))
        ans=answer.to_string(index=False,header=False)
        
        PredictedData.objects.create(name=patientname,bodyfat=bodyfat,ObesityLevel=obesity,StrokeStatus=ans)
        
        return render(request, 'results.html',{'patients':PatientData.objects.all(), 'answer':ans,'bodyfat':bodyfat,'height':height,'weight':weight,'bmi':bmi,'obesity':obesity})    
    else:
        return render(request, 'prediction.html',{'patients':PatientData.objects.all()})        

@csrf_exempt
def test(request):
    global ht,wt,valjson   
    if request.method=="POST":

        # print("jj",json.loads(request.body))
        # valjson={'height':'1.67','weight':'55'}
        w=request.body.decode('utf-8').replace("'",'"')
        # print("w--->>>>>   ",w) 
        valjson = json.loads(w)
        if(valjson):
            # print(type(valjson))
            # print(valjson)
            wt = valjson['weight']
            ht=valjson['height']
            print("test h",ht)
            print("test w",wt)
            ht=str(ht)
            wt=str(wt)
            # sensdat.save()
            # sensdat = SensorData.objects.create(height = ht, weight=wt)
            
            # return render(request,'test.html')
            # print(type(hr))

        else:
            ht='None'
            wt='None'
           
        
    return render(request,'test.html')
        # return HttpResponse(html)




def logout(request):
    logout(request)
    return redirect('loginpage')

# @login_required
def index(request):
    pdata = PredictedData.objects.all()
    fdata = FormData.objects.all()
    # sdata = SensorData.objects.all()
    # pdata_count = pdata.count()
    context = {
        'pdata': pdata,
        # 'pdata_count':pdata_count,
        'fdata': fdata,
        # 'sdata': sdata,
            }
    return render(request, 'index.html', context)