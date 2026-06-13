from django.db import models
from django.contrib.auth.models import AbstractUser


MUNICIPIOS_MENDOZA = [
    ('capital', 'Capital'),
    ('godoy_cruz', 'Godoy Cruz'),
    ('guaymallen', 'Guaymallén'),
    ('las_heras', 'Las Heras'),
    ('maipu', 'Maipú'),
    ('lujan', 'Luján de Cuyo'),
    ('san_martin', 'San Martín'),
    ('rivadavia', 'Rivadavia'),
    ('junin', 'Junín'),
    ('san_rafael', 'San Rafael'),
    ('general_alvear', 'General Alvear'),
    ('malargue', 'Malargüe'),
    ('lavalle', 'Lavalle'),
    ('san_carlos', 'San Carlos'),
    ('tupungato', 'Tupungato'),
    ('tunuyan', 'Tunuyán'),
    ('la_paz', 'La Paz'),
    ('santa_rosa', 'Santa Rosa'),
    ('general_san_martin', 'General San Martín'),
    ('otro', 'Otro'),
]

EPISODIOS = [
    ('EP1', 'Episodio 1'),
    ('EP2', 'Episodio 2'),
    ('EP3', 'Episodio 3'),
    ('EP4', 'Episodio 4'),
]

DIAS_SEMANA = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
    ('lunes_miercoles', 'Lunes y Miércoles'),
    ('martes_jueves', 'Martes y Jueves'),
    ('otro', 'Otro'),
]


class Usuario(AbstractUser):
    ROLES = [
        ('facilitador', 'Facilitador'),
        ('administrador', 'Administrador'),
    ]

    dni = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='DNI',
    )
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='facilitador',
        verbose_name='Rol',
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Nacimiento',
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def nombre_completo(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def es_administrador(self):
        return self.rol == 'administrador'

    @property
    def es_facilitador(self):
        return self.rol == 'facilitador'


class Curso(models.Model):
    municipio = models.CharField(
        max_length=50,
        choices=MUNICIPIOS_MENDOZA,
        verbose_name='Municipio',
    )
    episodio = models.CharField(
        max_length=10,
        choices=EPISODIOS,
        verbose_name='Episodio',
    )
    sede = models.CharField(
        max_length=100,
        verbose_name='Sede',
        help_text='Ej: CAU, Club Vecinal, Escuela N°123',
    )
    dias = models.CharField(
        max_length=30,
        choices=DIAS_SEMANA,
        verbose_name='Días',
        blank=True,
    )
    horario = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Horario',
        help_text='Ej: 9:00 a 13:00',
    )
    fecha_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Inicio',
    )
    facilitadores = models.ManyToManyField(
        Usuario,
        related_name='cursos_asignados',
        blank=True,
        verbose_name='Facilitadores',
        limit_choices_to={'rol': 'facilitador'},
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['municipio', 'episodio', 'sede']
        unique_together = ['municipio', 'episodio', 'sede']

    def __str__(self):
        return f'{self.get_episodio_display()} — {self.sede} ({self.get_municipio_display()})'

    @property
    def nombre_completo(self):
        return self.__str__()

    @property
    def cantidad_estudiantes(self):
        return self.estudiantes.filter(activo=True).count()


class Estudiante(models.Model):
    GENEROS = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
        ('no_especifica', 'No especifica'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    dni = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='DNI',
    )
    email = models.EmailField(blank=True, verbose_name='Email')
    fecha_nacimiento = models.DateField(
        null=True, blank=True,
        verbose_name='Fecha de Nacimiento',
    )
    genero = models.CharField(
        max_length=20,
        blank=True,
        choices=GENEROS,
        verbose_name='Género',
    )
    direccion = models.CharField(
        max_length=200, blank=True,
        verbose_name='Dirección',
    )
    escuela = models.CharField(
        max_length=150, blank=True,
        verbose_name='Escuela',
    )
    problemas_salud = models.TextField(
        blank=True,
        verbose_name='Problemas de Salud',
        help_text='Alergias, condiciones médicas, etc.',
    )
    tutor_nombre = models.CharField(
        max_length=150, blank=True,
        verbose_name='Nombre del Tutor',
    )
    tutor_dni = models.CharField(
        max_length=15, blank=True,
        verbose_name='DNI del Tutor',
    )
    tutor_contacto = models.CharField(
        max_length=50, blank=True,
        verbose_name='Contacto del Tutor',
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='estudiantes',
        verbose_name='Curso',
    )
    # ── Estado activo/baja ──
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Desactivar para dar de baja sin eliminar el historial',
    )
    fecha_baja = models.DateField(
        null=True, blank=True,
        verbose_name='Fecha de Baja',
    )
    motivo_baja = models.CharField(
        max_length=200, blank=True,
        verbose_name='Motivo de Baja',
        help_text='Ej: OTRO, cambio de domicilio, etc.',
    )

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'


class Asistencia(models.Model):
    ESTADOS = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('ausente_justificado', 'Ausente Justificado'),
    ]

    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name='asistencias',
        verbose_name='Estudiante',
    )
    facilitador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asistencias_marcadas',
        verbose_name='Facilitador',
        limit_choices_to={'rol': 'facilitador'},
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asistencias',
        verbose_name='Curso',
    )
    fecha = models.DateField(verbose_name='Fecha')
    estado = models.CharField(
        max_length=25,
        choices=ESTADOS,
        verbose_name='Estado',
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registrado',
    )

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha', 'estudiante__apellido']
        unique_together = ['estudiante', 'curso', 'fecha']

    def __str__(self):
        return f'{self.estudiante} - {self.fecha} - {self.get_estado_display()}'