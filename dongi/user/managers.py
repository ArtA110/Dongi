from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, first_name,last_name, email, password=None, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        if not first_name:
            raise ValueError('The First Name field must be set')
        if not last_name:
            raise ValueError('The Last Name field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,first_name=first_name,last_name=last_name **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email,  password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not first_name:
            raise ValueError('The First Name field must be set')
        if not last_name:
            raise ValueError('The Last Name field must be set')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        email = self.normalize_email(email)
        user = self.model(
            email=email,first_name=first_name,last_name=last_name **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
