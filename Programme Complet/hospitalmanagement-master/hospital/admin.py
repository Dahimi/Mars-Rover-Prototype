from django.contrib import admin
from .models import (
    Bed,
    Block,
    Doctor,
    Patient,
    Appointment,
    PatientDischargeDetails,
    Receptioniste,
    Room,
    Fiche,
    Infirmier,
)

# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Doctor, DoctorAdmin)


class ReceptionisteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Receptioniste, DoctorAdmin)


class PatientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Patient, PatientAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Appointment, AppointmentAdmin)


class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)


class BlockAdmin(admin.ModelAdmin):
    pass


admin.site.register(Block, BlockAdmin)


class RoomAdmin(admin.ModelAdmin):
    pass


admin.site.register(Room, RoomAdmin)


class BedAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bed, BedAdmin)


class FicheAdmin(admin.ModelAdmin):
    pass


admin.site.register(Fiche, FicheAdmin)

class InfirmierAdmin(admin.ModelAdmin):
    pass


admin.site.register(Infirmier, InfirmierAdmin)