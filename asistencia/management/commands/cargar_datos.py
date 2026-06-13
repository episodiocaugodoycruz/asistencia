from django.core.management.base import BaseCommand
from asistencia.models import Usuario, Curso, Estudiante, Asistencia
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Carga datos iniciales de prueba'

    def handle(self, *args, **options):

        # ── Administrador ──
        admin, _ = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Sonia',
                'last_name': 'Guevara',
                'dni': '20345678',
                'email': 'sonia@conectados.edu.ar',
                'rol': 'administrador',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin.set_password('admin123')
        admin.save()

        # ── Facilitadores (3, cada uno con cursos distintos) ──
        facilitadores_data = [
            {
                'username': 'marta.g',
                'first_name': 'Marta',
                'last_name': 'González',
                'dni': '25678901',
                'email': 'marta.g@conectados.edu.ar',
            },
            {
                'username': 'luciano.g',
                'first_name': 'Luciano',
                'last_name': 'Godoy',
                'dni': '30123456',
                'email': 'luciano.g@conectados.edu.ar',
            },
            {
                'username': 'ana.l',
                'first_name': 'Ana',
                'last_name': 'López',
                'dni': '28456789',
                'email': 'ana.l@conectados.edu.ar',
            },
        ]

        facilitadores = []
        for fd in facilitadores_data:
            f, _ = Usuario.objects.get_or_create(
                username=fd['username'],
                defaults={
                    'first_name': fd['first_name'],
                    'last_name': fd['last_name'],
                    'dni': fd['dni'],
                    'email': fd['email'],
                    'rol': 'facilitador',
                }
            )
            f.set_password('1234')
            f.save()
            facilitadores.append(f)

        marta, luciano, ana = facilitadores

        # ── Cursos (6, asignados específicamente a cada facilitador) ──
        # Marta tiene: Programación Web 2do A y Diseño UX/UI 2do B
        # Luciano tiene: Programación Web 3ro A y Python 3ro B
        # Ana tiene: Base de Datos 2do A y JavaScript 2do B

        cursos_data = [
            {'nombre': 'Programación Web', 'anio': '2do', 'division': 'A', 'facilitador': marta},
            {'nombre': 'Diseño UX/UI',     'anio': '2do', 'division': 'B', 'facilitador': marta},
            {'nombre': 'Programación Web', 'anio': '3ro', 'division': 'A', 'facilitador': luciano},
            {'nombre': 'Python',           'anio': '3ro', 'division': 'B', 'facilitador': luciano},
            {'nombre': 'Base de Datos',    'anio': '2do', 'division': 'A', 'facilitador': ana},
            {'nombre': 'JavaScript',       'anio': '2do', 'division': 'B', 'facilitador': ana},
        ]

        cursos = []
        for cd in cursos_data:
            c, _ = Curso.objects.get_or_create(
                nombre=cd['nombre'],
                anio=cd['anio'],
                division=cd['division'],
            )
            c.facilitadores.set([cd['facilitador']])
            cursos.append(c)

        prog_web_2, diseno_2, prog_web_3, python_3, bd_2, js_2 = cursos

        # ── Estudiantes (18, 3 por curso) ──
        estudiantes_data = [
            # Programación Web 2do A (Marta)
            {'nombre': 'María',     'apellido': 'González',  'dni': '50123456', 'email': 'mgonzalez@mail.com',  'escuela': 'Escuela Técnica Mendoza', 'direccion': 'San Martín 1250',  'tutor_nombre': 'Carlos González',  'tutor_contacto': '2615551001', 'tutor_dni': '27001001', 'curso': prog_web_2},
            {'nombre': 'Lucas',     'apellido': 'Pereyra',   'dni': '50234567', 'email': 'lpereyra@mail.com',   'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Belgrano 430',     'tutor_nombre': 'Ana Pereyra',      'tutor_contacto': '2615551002', 'tutor_dni': '27001002', 'curso': prog_web_2},
            {'nombre': 'Valentina', 'apellido': 'Romero',    'dni': '50345678', 'email': 'vromero@mail.com',    'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Las Heras 890',    'tutor_nombre': 'Pedro Romero',     'tutor_contacto': '2615551003', 'tutor_dni': '27001003', 'curso': prog_web_2},

            # Diseño UX/UI 2do B (Marta)
            {'nombre': 'Agustín',   'apellido': 'Molina',    'dni': '50456789', 'email': 'amolina@mail.com',    'escuela': 'Colegio Nacional',        'direccion': 'Rivadavia 1500',   'tutor_nombre': 'Laura Molina',     'tutor_contacto': '2615551004', 'tutor_dni': '27001004', 'curso': diseno_2},
            {'nombre': 'Florencia', 'apellido': 'Castillo',  'dni': '50567890', 'email': 'fcastillo@mail.com',  'escuela': 'Colegio Nacional',        'direccion': 'Córdoba 220',      'tutor_nombre': 'Silvia Castillo',  'tutor_contacto': '2615551005', 'tutor_dni': '27001005', 'curso': diseno_2},
            {'nombre': 'Mateo',     'apellido': 'Vargas',    'dni': '50678901', 'email': 'mvargas@mail.com',    'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Godoy Cruz 340',   'tutor_nombre': 'Jorge Vargas',     'tutor_contacto': '2615551006', 'tutor_dni': '27001006', 'curso': diseno_2},

            # Programación Web 3ro A (Luciano)
            {'nombre': 'Camila',    'apellido': 'Díaz',      'dni': '50789012', 'email': 'cdiaz@mail.com',      'escuela': 'Colegio Nacional',        'direccion': 'Necochea 150',     'tutor_nombre': 'María Díaz',       'tutor_contacto': '2615551007', 'tutor_dni': '27001007', 'curso': prog_web_3},
            {'nombre': 'Bruno',     'apellido': 'Fernández', 'dni': '50890123', 'email': 'bfernandez@mail.com', 'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Colón 880',        'tutor_nombre': 'Roberto Fernández','tutor_contacto': '2615551008', 'tutor_dni': '27001008', 'curso': prog_web_3},
            {'nombre': 'Sofía',     'apellido': 'Herrera',   'dni': '50901234', 'email': 'sherrera@mail.com',   'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Sarmiento 450',    'tutor_nombre': 'Elena Herrera',    'tutor_contacto': '2615551009', 'tutor_dni': '27001009', 'curso': prog_web_3},

            # Python 3ro B (Luciano)
            {'nombre': 'Tomás',     'apellido': 'Ruiz',      'dni': '51012345', 'email': 'truiz@mail.com',      'escuela': 'Colegio Nacional',        'direccion': 'Mitre 670',        'tutor_nombre': 'Carlos Ruiz',      'tutor_contacto': '2615551010', 'tutor_dni': '27001010', 'curso': python_3},
            {'nombre': 'Julieta',   'apellido': 'Álvarez',   'dni': '51123456', 'email': 'jalvarez@mail.com',   'escuela': 'Colegio Nacional',        'direccion': 'Paso de los Andes 90','tutor_nombre': 'Marta Álvarez', 'tutor_contacto': '2615551011', 'tutor_dni': '27001011', 'curso': python_3},
            {'nombre': 'Nicolás',   'apellido': 'Torres',    'dni': '51234567', 'email': 'ntorres@mail.com',    'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Alem 1200',        'tutor_nombre': 'Patricia Torres',  'tutor_contacto': '2615551012', 'tutor_dni': '27001012', 'curso': python_3},

            # Base de Datos 2do A (Ana)
            {'nombre': 'Lucía',     'apellido': 'Pérez',     'dni': '51345678', 'email': 'lperez@mail.com',     'escuela': 'Escuela Técnica Mendoza', 'direccion': 'España 320',       'tutor_nombre': 'Diego Pérez',      'tutor_contacto': '2615551013', 'tutor_dni': '27001013', 'curso': bd_2},
            {'nombre': 'Santiago',  'apellido': 'Morales',   'dni': '51456789', 'email': 'smorales@mail.com',   'escuela': 'Colegio Nacional',        'direccion': 'Chile 780',        'tutor_nombre': 'Graciela Morales', 'tutor_contacto': '2615551014', 'tutor_dni': '27001014', 'curso': bd_2},
            {'nombre': 'Antonella', 'apellido': 'Sosa',      'dni': '51567890', 'email': 'asosa@mail.com',      'escuela': 'Colegio Nacional',        'direccion': 'Perú 410',         'tutor_nombre': 'Hugo Sosa',        'tutor_contacto': '2615551015', 'tutor_dni': '27001015', 'curso': bd_2},

            # JavaScript 2do B (Ana)
            {'nombre': 'Ignacio',   'apellido': 'Luna',      'dni': '51678901', 'email': 'iluna@mail.com',      'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Lavalle 560',      'tutor_nombre': 'Susana Luna',      'tutor_contacto': '2615551016', 'tutor_dni': '27001016', 'curso': js_2},
            {'nombre': 'Micaela',   'apellido': 'Ibáñez',    'dni': '51789012', 'email': 'mibanez@mail.com',    'escuela': 'Escuela Técnica Mendoza', 'direccion': 'Rivadavia 890',    'tutor_nombre': 'Fernando Ibáñez',  'tutor_contacto': '2615551017', 'tutor_dni': '27001017', 'curso': js_2},
            {'nombre': 'Rodrigo',   'apellido': 'Vega',      'dni': '51890123', 'email': 'rvega@mail.com',      'escuela': 'Colegio Nacional',        'direccion': 'Garibaldi 230',    'tutor_nombre': 'Claudia Vega',     'tutor_contacto': '2615551018', 'tutor_dni': '27001018', 'curso': js_2},
        ]

        # Algunos con problemas de salud para probar esa funcionalidad
        problemas_salud = {
            '50123456': 'Alergia estacional leve. Trae antihistamínico.',
            '50567890': 'Asma leve. Trae inhalador en la mochila.',
            '51123456': 'Celíaca. No puede comer gluten.',
        }

        estudiantes = []
        for ed in estudiantes_data:
            est, _ = Estudiante.objects.get_or_create(
                dni=ed['dni'],
                defaults={
                    'nombre': ed['nombre'],
                    'apellido': ed['apellido'],
                    'email': ed['email'],
                    'escuela': ed['escuela'],
                    'direccion': ed['direccion'],
                    'tutor_nombre': ed['tutor_nombre'],
                    'tutor_contacto': ed['tutor_contacto'],
                    'tutor_dni': ed['tutor_dni'],
                    'problemas_salud': problemas_salud.get(ed['dni'], ''),
                    'fecha_nacimiento': date(2010, random.randint(1, 12), random.randint(1, 28)),
                    'curso': ed['curso'],
                }
            )
            estudiantes.append(est)

        # ── Asistencias de prueba (últimos 7 días) ──
        estados = ['presente', 'presente', 'presente', 'presente', 'ausente', 'ausente_justificado']
        hoy = date.today()

        for dia in range(7):
            fecha = hoy - timedelta(days=dia)
            for est in estudiantes:
                # El facilitador del curso marca la asistencia
                facilitador_del_curso = est.curso.facilitadores.first()
                Asistencia.objects.get_or_create(
                    estudiante=est,
                    curso=est.curso,
                    fecha=fecha,
                    defaults={
                        'estado': random.choice(estados),
                        'facilitador': facilitador_del_curso,
                    }
                )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Datos cargados correctamente:\n'
            f'\n👤 ADMINISTRADOR\n'
            f'   admin / admin123\n'
            f'\n👥 FACILITADORES (contraseña: 1234)\n'
            f'   marta.g  → Programación Web 2do A + Diseño UX/UI 2do B\n'
            f'   luciano.g → Programación Web 3ro A + Python 3ro B\n'
            f'   ana.l    → Base de Datos 2do A + JavaScript 2do B\n'
            f'\n📚 CURSOS: {len(cursos)}\n'
            f'📋 ESTUDIANTES: {len(estudiantes)} (3 por curso)\n'
            f'📅 ASISTENCIAS: últimos 7 días\n'
        ))