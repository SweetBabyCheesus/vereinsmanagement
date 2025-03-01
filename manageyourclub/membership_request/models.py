from django.db import models
from sqlalchemy import JSON, false

from django_form_builder.dynamic_fields import get_fields_types
from django_form_builder.models import DynamicFieldMap
from django_form_builder.models import SavedFormContent
from django.db.models import Max

from members.models import Membership
from clubs.models import ClubModel

class FieldsListModel(DynamicFieldMap):
    # Übernommen von Django-Form-Builder
    # Angepasst von Max Rosemeier

    # if you want to integrate dynamic fields with your own,
    # define a new file that import all 'dynamic_fields' and defines others new and
    # then pass it as param to get_fields_types(class_name=my_custom_fields_file)

    club = models.ForeignKey(ClubModel, on_delete=models.CASCADE)
    DynamicFieldMap._meta.get_field('field_type').choices = get_fields_types()

    
    @staticmethod
    def create(club,name,type,value,required,help_text,preText,ordering):
        #Autor: Max
        #Methode zum hinzufügen von Formularfeldern. Kann mit FieldsListModel.addFormField(club=...) angesprochen werden
        if not FieldsListModel.objects.filter(club=club,name=name,field_type=type,value=value,is_required=required,help_text=help_text,pre_text=preText,ordering=ordering).exists():
            #Ist die gewählte Stelle des Feldes im Formular schon besetzt, werden die restlichen felder nach hinten verschoben  
            if FieldsListModel.objects.filter(club=club,ordering=ordering).exists():
                ordering__max = FieldsListModel.objects.latest('ordering').ordering

                for i in range(ordering__max, ordering-1, -1):
                    FieldsListModel.objects.filter(club=club,ordering=i).update(ordering=i+1)

            newField  = FieldsListModel.objects.create(club=club,name=name,field_type=type,value=value,is_required=required,help_text=help_text,pre_text=preText,ordering=ordering)
            newField.save()
            return newField
        return None




class CustomMembershipData(SavedFormContent):
    #Autor: Max Rosemeier
    #Speicherung der Custom Membership Daten

    membership = models.OneToOneField(Membership, on_delete=models.PROTECT)

    @staticmethod
    def get_or_create(membership, json):

        newCustomData, created = CustomMembershipData.objects.get_or_create(membership=membership, json=json)
        if created:
            newCustomData.save()
        
        return newCustomData
        
