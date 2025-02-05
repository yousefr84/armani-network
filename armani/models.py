import bcrypt
from django.core.validators import RegexValidator
from neomodel import *
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


# Create your models here.
class EncryptedStringProperty(StringProperty):
    def set(self, instance, value):
        hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        super().set(instance, hashed.decode('utf-8'))

    def get(self, instance, owner):
        return super().get(instance, owner)

    def verify(self, instance, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), instance.password.encode('utf-8'))


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0


class Person(StructuredNode):
    username_validator = UnicodeUsernameValidator()
    username = StringProperty(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=False
    )
    password = EncryptedStringProperty(_("password"), null=False, )
    first_name = StringProperty()
    last_name = StringProperty()
    photo = StringProperty()
    resume = StringProperty()
    email = EmailProperty()
    phone_number = StringProperty(
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number.")]
    )
    is_admin = BooleanProperty(default=False)
    date_joined = DateTimeProperty(auto_now=True)

    work_at = Relationship('Company', 'work_at')
    Collaboration = Relationship('Project', 'collaboration')
    friendship = Relationship('Person', 'friendship')


class Company(StructuredNode):
    name = StringProperty()
    date_of_birth = DateProperty()
    license = ArrayProperty()
    resume = StringProperty()
    National_ID = StringProperty(
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10,11}$', message="Enter a valid National ID.")]
    )

    collaborations = Relationship('Project', 'collaboration')
    members = Relationship('Person', 'members')
    manager = Relationship('Person', 'manager')
    friendship = Relationship('Company', 'friendship')


class Project(StructuredNode):
    name = StringProperty()
    proposal = StringProperty()
    business_plan = StringProperty()
    feasibility_study = StringProperty()
    creation_date = DateTimeProperty(default_now=True)

    manager = Relationship('Person', 'manager')
    members = Relationship('Person', 'members')
    collaborating_companies = Relationship('Company', 'collaborating_companies')
