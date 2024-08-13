from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    is_email_verified = models.BooleanField(default=False)
    forum_messages = models.PositiveIntegerField(default=0)  # New field added

    # Subscription details
    SUBSCRIPTION_STATUS_ACTIVE = 'active'
    SUBSCRIPTION_STATUS_INACTIVE = 'inactive'
    SUBSCRIPTION_STATUS_TRIAL = 'trial'
    SUBSCRIPTION_STATUS_CHOICES = [
        (SUBSCRIPTION_STATUS_ACTIVE, 'Active'),
        (SUBSCRIPTION_STATUS_INACTIVE, 'Inactive'),
        (SUBSCRIPTION_STATUS_TRIAL, 'Trial'),
    ]
    subscription_status = models.CharField(
        choices=SUBSCRIPTION_STATUS_CHOICES, 
        default=SUBSCRIPTION_STATUS_INACTIVE
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    is_trial_used = models.BooleanField(default=False)
    is_auto_renewal = models.BooleanField(default=False)

    # Stripe integration
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=50, blank=True, null=True)

    # Profile information
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    city = models.CharField(blank=True, null=True, max_length=255)
    bio = models.TextField(blank=True, null=True, max_length=500)

    # Educational status
    ESTUDIANTE_MIR_PRIMERA = 1
    ESTUDIANTE_MIR_TIENE = 2
    ESTUDIANTE_MEDICINA = 3
    OTRO = 4
    EDUCATIONAL_STATUS_CHOICES = [
        (ESTUDIANTE_MIR_PRIMERA, 'Estudiante MIR para una primera especialidad'),
        (ESTUDIANTE_MIR_TIENE, 'Estudiante MIR que ya tiene alguna especialidad'),
        (ESTUDIANTE_MEDICINA, 'Estudiante de Medicina'),
        (OTRO, 'Ninguna de las anteriores'),
    ]
    educational_status = models.IntegerField(choices=EDUCATIONAL_STATUS_CHOICES, null=True, blank=True)

    # Desired specialty
    ALERGOLOGIA = 1
    ANALISIS_CLINICOS = 2
    ANATOMIA_PATOLOGICA = 3
    ANESTESIOLOGIA = 4
    ANGIOLOGIA = 5
    APARATO_DIGESTIVO = 6
    BIOQUIMICA_CLINICA = 7
    CARDIOLOGIA = 8
    CIRUGIA_CARDIOVASCULAR = 9
    CIRUGIA_GENERAL_DIGESTIVO = 10
    CIRUGIA_ORAL_MAXILOFACIAL = 11
    CIRUGIA_ORTOPEDICA_TRAUMATOLOGIA = 12
    CIRUGIA_PEDIATRICA = 13
    CIRUGIA_PLASTICA_ESTETICA = 14
    CIRUGIA_TORACICA = 15
    DERMATOLOGIA = 16
    ENDOCRINOLOGIA = 17
    GINECOLOGIA = 18
    GERIATRIA = 19
    HEMATOLOGIA = 20
    INMUNOLOGIA = 21
    MEDICINA_TRABAJO = 22
    MEDICINA_FAMILIAR_COMUNITARIA = 23
    MEDICINA_FISICA_REHABILITACION = 24
    MEDICINA_INTENSIVA = 25
    MEDICINA_INTERNA = 26
    MEDICINA_LEGAL_FORENSE = 27
    MEDICINA_NUCLEAR = 28
    MEDICINA_PREVENTIVA = 29
    MICROBIOLOGIA = 30
    NEFROLOGIA = 31
    NEUMOLOGIA = 32
    NEUROCIRUGIA = 33
    NEUROFISIOLOGIA = 34
    NEUROLOGIA = 35
    OBSTETRICIA_GINECOLOGIA = 36
    OFTALMOLOGIA = 37
    ONCOLOGIA_MEDICA = 38
    ONCOLOGIA_RADIOTERAPICA = 39
    OTORRINOLARINGOLOGIA = 40
    PEDIATRIA = 41
    PSIQUIATRIA = 42
    RADIODIAGNOSTICO = 43
    REUMATOLOGIA = 44
    URGENCIAS_EMERGENCIAS = 45
    UROLOGIA = 46
    DESIRED_SPECIALTY_CHOICES = [
        (ALERGOLOGIA, 'Alergología'),
        (ANALISIS_CLINICOS, 'Análisis Clínicos'),
        (ANATOMIA_PATOLOGICA, 'Anatomía Patológica'),
        (ANESTESIOLOGIA, 'Anestesiología y Reanimación'),
        (ANGIOLOGIA, 'Angiología y Cirugía Vascular'),
        (APARATO_DIGESTIVO, 'Aparato Digestivo'),
        (BIOQUIMICA_CLINICA, 'Bioquímica Clínica'),
        (CARDIOLOGIA, 'Cardiología'),
        (CIRUGIA_CARDIOVASCULAR, 'Cirugía Cardiovascular'),
        (CIRUGIA_GENERAL_DIGESTIVO, 'Cirugía Gral. y del A.Digestivo'),
        (CIRUGIA_ORAL_MAXILOFACIAL, 'Cirugía Oral y Maxilofacial'),
        (CIRUGIA_ORTOPEDICA_TRAUMATOLOGIA, 'Cirugía Ortopédica y Traumatología'),
        (CIRUGIA_PEDIATRICA, 'Cirugía Pediátrica'),
        (CIRUGIA_PLASTICA_ESTETICA, 'Cirugía Plástica Estética y Reparadora'),
        (CIRUGIA_TORACICA, 'Cirugía Torácica'),
        (DERMATOLOGIA, 'Dermatología Médico-Quirúrgica y V.'),
        (ENDOCRINOLOGIA, 'Endocrinología y Nutrición'),
        (GINECOLOGIA, 'Ginecología'),
        (GERIATRIA, 'Geriatría'),
        (HEMATOLOGIA, 'Hematología y Hemoterapia'),
        (INMUNOLOGIA, 'Inmunología'),
        (MEDICINA_TRABAJO, 'Medicina del Trabajo'),
        (MEDICINA_FAMILIAR_COMUNITARIA, 'Medicina Familiar y Comunitaria'),
        (MEDICINA_FISICA_REHABILITACION, 'Medicina Física y Rehabilitación'),
        (MEDICINA_INTENSIVA, 'Medicina Intensiva'),
        (MEDICINA_INTERNA, 'Medicina Interna'),
        (MEDICINA_LEGAL_FORENSE, 'Medicina Legal y Forense'),
        (MEDICINA_NUCLEAR, 'Medicina Nuclear'),
        (MEDICINA_PREVENTIVA, 'Medicina Preventiva y Salud Pública'),
        (MICROBIOLOGIA, 'Microbiología y Parasitología'),
        (NEFROLOGIA, 'Nefrología'),
        (NEUMOLOGIA, 'Neumología'),
        (NEUROCIRUGIA, 'Neurocirugía'),
        (NEUROFISIOLOGIA, 'Neurofisiología Clínica'),
        (NEUROLOGIA, 'Neurología'),
        (OBSTETRICIA_GINECOLOGIA, 'Obstetricia y Ginecología'),
        (OFTALMOLOGIA, 'Oftalmología'),
        (ONCOLOGIA_MEDICA, 'Oncología Médica'),
        (ONCOLOGIA_RADIOTERAPICA, 'Oncología Radioterápica'),
        (OTORRINOLARINGOLOGIA, 'Otorrinolaringología'),
        (PEDIATRIA, 'Pediatría'),
        (PSIQUIATRIA, 'Psiquiatría'),
        (RADIODIAGNOSTICO, 'Radiodiagnóstico'),
        (REUMATOLOGIA, 'Reumatología'),
        (URGENCIAS_EMERGENCIAS, 'Urgencias y Emergencias'),
        (UROLOGIA, 'Urología'),
    ]
    desired_specialty = models.IntegerField(choices=DESIRED_SPECIALTY_CHOICES, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'custom user'
        verbose_name_plural = 'custom users'
