from datetime import date
from django.db import models
from django.contrib.auth.models import User


departments = [
    ("Cardiologie", "Cardiologie"),
    ("Dermatologie", "Dermatologie"),
    ("Médecine d'urgence", "Médecine d'urgence"),
    ("Allergologie/Immunologie", "Allergologie/Immunologie"),
    ("Anesthésiologistes", "Anesthésiologistes"),
    ("Chirurgie du côlon et du rectum", "Chirurgie du côlon et du rectum"),
]
departments_i = [
    ("Infirmier Urgentiste", "Infirmier Urgentiste"),
    ("Infirmier Polyvalent", "Infirmier Polyvalent"),
    ("Infirmier Anesthésiste", "Infirmier Anesthésiste"),
    ("Infirmier Néonatale", "Infirmier Néonatale"),
    ("Infirmier en Pédiatrie", "Infirmier en Pédiatrie"),
    ("Infirmier Psychiatrique", "Infirmier Psychiatrique"),
    ("Infirmier en Traumatologie", "Infirmier en Traumatologie"),
    ("Infirmier en soins gérés", "Infirmier en soins gérés"),
    ("Infirmière sage-femme", "Infirmière sage-femme"),
]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(
        max_length=50, choices=departments, default="Cardiologie"
    )
    status = models.BooleanField(default=False)
    presence = models.BooleanField(default=False)
    date = models.CharField(max_length=40, default="2021-12-12")
    horaire = models.CharField(max_length=40, default="00:00:00")

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


class Receptioniste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "Receptioniste : {}".format(self.user.first_name)


class Infirmier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(
        max_length=50, choices=departments_i, default="Cardiologist"
    )
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/PatientProfilePic/", null=True, blank=True
    )
    cin = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)
    isAffected = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.symptoms + ")"


class Appointment(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)


class PatientDischargeDetails(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40)
    assignedDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)

    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)

    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)


class Block(models.Model):
    blockName = models.CharField(
        max_length=50, choices=departments, default="Cardiologie"
    )

    def __str__(self):
        return "Block Number" + str(self.id) + " : " + self.blockName


class Room(models.Model):
    block = models.ForeignKey(Block, null=True, on_delete=models.SET_NULL)
    number = models.PositiveIntegerField(null=False)

    def __str__(self):
        return str(self.block.blockName) + " --  Room " + str(self.number)


class Bed(models.Model):
    CATEGORY = (
        ("occupied", "occupied"),
        ("free", "free"),
    )
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    number = models.PositiveIntegerField(null=False)
    status = models.CharField(
        max_length=200, null=True, choices=CATEGORY, default="free"
    )
    patientId = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (
            str(self.room.block.blockName)
            + " --  Room "
            + str(self.room.number)
            + " --  Bed "
            + str(self.number)
        )


class Fiche(models.Model):
    patientId = models.PositiveIntegerField(null=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date = models.DateField(auto_now=True)
    poids = models.CharField(max_length=10, default="")
