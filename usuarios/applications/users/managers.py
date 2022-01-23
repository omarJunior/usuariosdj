from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    #Metodo privado
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active= is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        return user

    #Usuario normal
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)

    #Super usuario
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)

    def cod_validation(self, id_user, cod_registro):
        if self.filter(pk = id_user, codregistro = cod_registro).exists():
            return True 
        return False





