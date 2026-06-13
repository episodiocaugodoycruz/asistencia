from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Estudiantes
    path('estudiantes/', views.buscar_estudiante, name='estudiantes'),

    # Asistencia
    path('asistencia/', views.toma_asistencia, name='asistencia'),
    path('asistencia/guardar/', views.guardar_asistencia, name='guardar_asistencia'),

    # Historial
    path('historial/', views.historial, name='historial'),

    # Admin
    path('admin-facilitadores/', views.gestionar_facilitadores, name='admin_facilitadores'),
    path('admin-cursos/', views.gestionar_cursos, name='admin_cursos'),

    # API
    path('api/estudiante/<str:dni>/', views.api_estudiante_dni, name='api_estudiante_dni'),

path('cursos/nuevo/', views.crear_curso, name='crear_curso'),
path('cursos/<int:curso_id>/editar/', views.editar_curso, name='editar_curso'),
path('cursos/<int:curso_id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
path('facilitadores/nuevo/', views.crear_facilitador, name='crear_facilitador'),
path('facilitadores/<int:facilitador_id>/editar/', views.editar_facilitador, name='editar_facilitador'),
path('facilitadores/<int:facilitador_id>/eliminar/', views.eliminar_facilitador, name='eliminar_facilitador'),

path('estudiantes/nuevo/', views.crear_estudiante, name='crear_estudiante'),
path('estudiantes/<int:estudiante_id>/editar/', views.editar_estudiante, name='editar_estudiante'),
path('estudiantes/<int:estudiante_id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),
]
