from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Curso, Estudiante, Asistencia


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'dni', 'rol', 'email']
    list_filter = ['rol']
    search_fields = ['first_name', 'last_name', 'dni', 'username']

    fieldsets = UserAdmin.fieldsets + (
        ('Datos de Conectados', {
            'fields': ('dni', 'rol', 'fecha_nacimiento')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos de Conectados', {
            'fields': ('dni', 'rol', 'fecha_nacimiento')
        }),
    )


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['municipio', 'episodio', 'sede', 'dias', 'horario', 'cantidad_estudiantes']
    list_filter = ['municipio', 'episodio']
    filter_horizontal = ['facilitadores']


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'email', 'curso', 'activo']
    list_filter = ['activo', 'curso']
    search_fields = ['nombre', 'apellido', 'dni']


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'fecha', 'estado', 'facilitador', 'curso']
    list_filter = ['estado', 'fecha', 'curso']
    search_fields = ['estudiante__nombre', 'estudiante__apellido', 'estudiante__dni']
    date_hierarchy = 'fecha'