from django.db import models

class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    blood_Group = models.CharField(max_length=3, choices=BLOOD_GROUPS)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"
    

class Partners(models.Model):
    Hospital_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    Contact = models.CharField(max_length=15)
    address = models.TextField()
    Facility = models.TextField()
    L_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.Hospital_name
    
class Donoation_history(models.Model):
    donor_id= models.ForeignKey(Donor, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    date = models.DateField()
    total_donations = models.PositiveIntegerField()
    reliability_score = models.FloatField()
    member_tag = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.donor.name} donated to {self.partner.Hospital_name} on {self.date}"
    
class Raised_request(models.Model):
    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    hospital_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    attenders_name = models.CharField(max_length=100)
    attender_phone_number = models.CharField(max_length=15)
    id_type = models.CharField(max_length=50)
    id_no = models.CharField(max_length=50)
    letter_head = models.CharField(max_length=100)
    patient_photo = models.ImageField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.partner.Hospital_name} raised a request for {self.quantity} units of {self.blood_group} blood on {self.date}"
    
class stock(models.Model):
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.partner.Hospital_name} has {self.quantity} units of {self.blood_group} blood in stock"