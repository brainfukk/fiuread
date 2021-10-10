from django.contrib.auth.models import UserManager

from src.apps.user.models import UserPurse, UserUnitRelation, Event, EventItemType
from src.apps.unit.models import Unit


class FIUReadUserManager(UserManager):
    def create_user_purse(self, user):
        return UserPurse.objects.get_or_create(user=user, defaults={
            "user": user
        })

    def create_user_unit_relations(self, user):
        units = Unit.objects.all()
        data = []
        for unit in units:
            dt = {
                "user": user,
                "unit": unit,
            }
            data.append(UserUnitRelation(**dt))
        return UserUnitRelation.objects.bulk_create(data)

    def create_user_base_events(self, user):
        return Event.objects.create(
            user=user,
            type=EventItemType.NOTIFICATION,
            message="Вы зарегистрировали аккаунт! {}".format(user.date_joined)
        )

    def confirm_email(self, username):
        user = self.get_by_natural_key(username)
        user.is_email_confirmed = True
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self._create_user(username, email, password, **extra_fields)
        self.create_user_purse(user=user)
        self.create_user_unit_relations(user=user)
        self.create_user_base_events(user=user)
        return user
