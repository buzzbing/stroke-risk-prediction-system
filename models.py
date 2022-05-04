from django.db import models
from django.utils import timezone


class PatientData(models.Model):
    name=models.CharField(max_length=200,null=True)
    age=models.IntegerField(null=True)
    address=models.CharField(max_length=200,null=True)
    contact=models.CharField(max_length=10,null=True)
    email=models.EmailField(max_length=200,null=True)
    registered_date=models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    def detail(self):
        return f" Name: {self.name} "
    def detail1(self):    
        return f"Age: {self.age} yrs "

class FormData(models.Model):

    GENDER_CHOICES=(
        ('Male','Male'),('Female','Female')
    )
    HT_CHOICES=(
        ('Yes','Yes'),('No','No')
    )
    HD_CHOICES=(
        ('Yes','Yes'),('No','No')
    )
    EM_CHOICES=(
        ('Yes','Yes'),('No','No')
    )
    WT_CHOICES=(
        ('Government Job','Government Job'),('Self-employed','Self-employed'),('Private','Private'),('children','children'),('Never_worked','Never_worked')
    )
    RESIDENCE_CHOICES=(
        ('Rural','Rural'),('Urban','Urban')
    )
    SMOKING_CHOICES=(
        ('never smoked','never smoked'),('smokes','smokes'),('formerly smoked','formerly smoked'),('Unknown','Unknown')
    )
    name=models.ForeignKey(PatientData, verbose_name="Patient Name", on_delete=models.RESTRICT,default=None)  
    gender=models.CharField(max_length=6,default=None,choices=GENDER_CHOICES)
    age=models.IntegerField( null=True)
    hypertension=models.CharField(max_length=3,default=None,choices=HT_CHOICES)
    heart_disease=models.CharField(max_length=3,default=None,choices=HD_CHOICES)
    ever_married=models.CharField(max_length=3,default=None,choices=EM_CHOICES)
    work_type=models.CharField(max_length=20,default=None,choices=WT_CHOICES)
    Residence_type=models.CharField(max_length=5,default=None,choices=RESIDENCE_CHOICES)
    avg_glucose_level=models.DecimalField(max_digits=5,decimal_places=2)
    smoking_status=models.CharField(max_length=20,default=None,choices=SMOKING_CHOICES)
    heartrate=models.CharField(null=True, default=None, max_length=20)
    prediction_date=models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.name)
    def detail(self):
        return f"Heart Rate: {self.heartrate} bpm  "


class SensorData(models.Model):
    # name=models.CharField(null=True, default=None, max_length=200)
    name = models.ForeignKey(PatientData, on_delete=models.RESTRICT,default=None,null=True)
    height=models.FloatField(null=True)
    weight=models.FloatField(null=True)
    
    
    def __str__(self):
        return str(self.name)
    def detail(self):
        return f"Height: {self.height}m  " 
    def detail1(self):    
        return f"Weight: {self.weight}m  "   

class PredictedData(models.Model):
    # name=models.CharField(null=True, default=None, max_length=200)
    name=models.ForeignKey(PatientData, on_delete=models.RESTRICT,default=None,null=True)
    FormDataID=models.ForeignKey(FormData, on_delete=models.RESTRICT,default=None,null=True )
    SensorDataID=models.ForeignKey(SensorData, on_delete=models.RESTRICT,default=None,null=True )
    bodyfat=models.FloatField(null=True)
    ObesityLevel=models.CharField(max_length = 20, default=None,null=True)
    StrokeStatus=models.CharField(max_length = 20, default = None,null=True)
    
    def __str__(self):
        return str(self.name)
    def detail(self):
        return f"  Obesity Level: {self.ObesityLevel}"
    def detail1(self):
        return f"  Body Fat Percentage: {self.bodyfat} %" 
    def detail2(self):
        return f"  Stroke Status: {self.StrokeStatus}"      
    
        
        
        
        

  


  