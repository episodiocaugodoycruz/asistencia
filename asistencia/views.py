from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from .models import Estudiante, Asistencia, Curso, Usuario
from datetime import date
import json


# ─── LOGIN ───
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        error = 'Usuario o contraseña incorrectos'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── DASHBOARD ───
@login_required
def dashboard(request):
    if request.user.es_administrador:
        # Admin ve todos los cursos y estadísticas globales
        cursos = Curso.objects.all()
        total_estudiantes = Estudiante.objects.count()
        total_facilitadores = Usuario.objects.filter(rol='facilitador').count()
    else:
        # Facilitador ve solo sus cursos
        cursos = request.user.cursos_asignados.all()
        total_estudiantes = Estudiante.objects.filter(
            curso__in=cursos
        ).distinct().count()
        total_facilitadores = None

    return render(request, 'dashboard.html', {
        'cursos': cursos,
        'total_estudiantes': total_estudiantes,
        'total_facilitadores': total_facilitadores,
    })


# ─── ESTUDIANTES ───
@login_required
def buscar_estudiante(request):
    # Cursos según rol
    if request.user.es_administrador:
        cursos = Curso.objects.all()
    else:
        cursos = request.user.cursos_asignados.all()

    # Filtros
    curso_id  = request.GET.get('curso', '')
    q         = request.GET.get('q', '').strip()
    ver_id    = request.GET.get('ver', '')

    # Queryset base filtrado por cursos accesibles
    estudiantes_qs = Estudiante.objects.filter(curso__in=cursos).select_related('curso')

    # Filtro por curso específico
    curso_activo = None
    if curso_id:
        try:
            curso_activo = cursos.get(id=curso_id)
            estudiantes_qs = estudiantes_qs.filter(curso=curso_activo)
        except Curso.DoesNotExist:
            pass

    # Filtro por nombre o DNI
    if q:
        from django.db.models import Q
        estudiantes_qs = estudiantes_qs.filter(
            Q(nombre__icontains=q) |
            Q(apellido__icontains=q) |
            Q(dni__icontains=q)
        )

    # Agrupar por curso
    grupos = []
    cursos_en_lista = cursos.filter(
        id__in=estudiantes_qs.values_list('curso_id', flat=True).distinct()
    )
    for curso in cursos_en_lista:
        ests = [e for e in estudiantes_qs if e.curso_id == curso.id]
        if ests:
            grupos.append({'curso': curso, 'estudiantes': ests})

    # Detalle de un estudiante específico
    estudiante_detalle = None
    if ver_id:
        try:
            est = Estudiante.objects.get(id=ver_id, curso__in=cursos)
            estudiante_detalle = est
        except Estudiante.DoesNotExist:
            pass

    return render(request, 'estudiantes.html', {
        'cursos': cursos,
        'curso_activo': curso_activo,
        'q': q,
        'grupos': grupos,
        'estudiante_detalle': estudiante_detalle,
        'puede_editar': True,
        'puede_crear': request.user.es_administrador,
    })

@login_required
def crear_estudiante(request):
    # Solo admin puede crear estudiantes
    if not request.user.es_administrador:
        return HttpResponseForbidden('No tenés permiso para esta acción.')

    cursos = Curso.objects.all()
    error = None

    if request.method == 'POST':
        try:
            estudiante = Estudiante.objects.create(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                dni=request.POST.get('dni'),
                email=request.POST.get('email', ''),
                fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
                genero=request.POST.get('genero', ''),
                direccion=request.POST.get('direccion', ''),
                escuela=request.POST.get('escuela', ''),
                problemas_salud=request.POST.get('problemas_salud', ''),
                tutor_nombre=request.POST.get('tutor_nombre', ''),
                tutor_dni=request.POST.get('tutor_dni', ''),
                tutor_contacto=request.POST.get('tutor_contacto', ''),
                curso_id=request.POST.get('curso') or None,
            )
            return redirect('estudiantes')
        except Exception as e:
            error = str(e)

    return render(request, 'crear_estudiante.html', {
        'cursos': cursos,
        'error': error,
    })


@login_required
def editar_estudiante(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)

    # Facilitador solo puede editar estudiantes de sus cursos
    if request.user.es_facilitador:
        mis_cursos = request.user.cursos_asignados.all()
        if estudiante.curso not in mis_cursos:
            return HttpResponseForbidden('No tenés permiso para editar este estudiante.')

    cursos = Curso.objects.all() if request.user.es_administrador else request.user.cursos_asignados.all()
    error = None

    if request.method == 'POST':
        try:
            estudiante.nombre = request.POST.get('nombre')
            estudiante.apellido = request.POST.get('apellido')
            estudiante.dni = request.POST.get('dni')
            estudiante.email = request.POST.get('email', '')
            estudiante.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
            estudiante.genero = request.POST.get('genero', '')
            estudiante.direccion = request.POST.get('direccion', '')
            estudiante.escuela = request.POST.get('escuela', '')
            estudiante.problemas_salud = request.POST.get('problemas_salud', '')
            estudiante.tutor_nombre = request.POST.get('tutor_nombre', '')
            estudiante.tutor_dni = request.POST.get('tutor_dni', '')
            estudiante.tutor_contacto = request.POST.get('tutor_contacto', '')
            if request.user.es_administrador:
                estudiante.curso_id = request.POST.get('curso') or None
            estudiante.save()
            return redirect('estudiantes')
        except Exception as e:
            error = str(e)

    return render(request, 'editar_estudiante.html', {
        'estudiante': estudiante,
        'cursos': cursos,
        'error': error,
    })


# ─── TOMA DE ASISTENCIA ───
@login_required
def toma_asistencia(request):
    # Facilitador ve solo sus cursos, admin ve todos
    if request.user.es_administrador:
        cursos = Curso.objects.all()
    else:
        cursos = request.user.cursos_asignados.all()

    curso_id = request.GET.get('curso')
    fecha = request.GET.get('fecha', date.today().isoformat())
    estudiantes = []
    curso_seleccionado = None

    if curso_id:
        curso_seleccionado = get_object_or_404(Curso, id=curso_id)

        # Verificar que el facilitador tenga acceso a ese curso
        if request.user.es_facilitador and curso_seleccionado not in cursos:
            return HttpResponseForbidden('No tenés permiso para este curso.')

        asistencias_existentes = Asistencia.objects.filter(
            curso=curso_seleccionado,
            fecha=fecha
        ).select_related('estudiante')

        asistencias_dict = {a.estudiante_id: a for a in asistencias_existentes}

        estudiantes_con_estado = []
        for est in curso_seleccionado.estudiantes.all():
            asistencia = asistencias_dict.get(est.id)
            estudiantes_con_estado.append({
                'estudiante': est,
                'estado': asistencia.estado if asistencia else '',
                'observaciones': asistencia.observaciones if asistencia else '',
            })
        estudiantes = estudiantes_con_estado

    return render(request, 'asistencia.html', {
        'cursos': cursos,
        'curso_seleccionado': curso_seleccionado,
        'estudiantes': estudiantes,
        'fecha': fecha,
    })


@login_required
@require_POST
def guardar_asistencia(request):
    data = json.loads(request.body)
    curso_id = data.get('curso_id')
    fecha = data.get('fecha')
    registros = data.get('registros', [])

    curso = get_object_or_404(Curso, id=curso_id)

    # Verificar que el facilitador tenga acceso a ese curso
    if request.user.es_facilitador:
        mis_cursos = request.user.cursos_asignados.all()
        if curso not in mis_cursos:
            return JsonResponse({'ok': False, 'error': 'Sin permiso'}, status=403)

    for reg in registros:
        estudiante = get_object_or_404(Estudiante, id=reg['estudiante_id'])
        Asistencia.objects.update_or_create(
            estudiante=estudiante,
            curso=curso,
            fecha=fecha,
            defaults={
                'estado': reg['estado'],
                'observaciones': reg.get('observaciones', ''),
                'facilitador': request.user,
            }
        )

    return JsonResponse({'ok': True, 'mensaje': 'Asistencia guardada'})


# ─── HISTORIAL ───
@login_required
def historial(request):
    # Admin ve todos los cursos, facilitador solo los suyos
    if request.user.es_administrador:
        cursos = Curso.objects.all()
    else:
        cursos = request.user.cursos_asignados.all()

    curso_id = request.GET.get('curso')
    fecha = request.GET.get('fecha')

    asistencias = Asistencia.objects.select_related(
        'estudiante', 'facilitador', 'curso'
    ).order_by('-fecha')

    # Facilitador solo ve asistencias de sus cursos
    if request.user.es_facilitador:
        asistencias = asistencias.filter(curso__in=cursos)

    if curso_id:
        asistencias = asistencias.filter(curso_id=curso_id)
    if fecha:
        asistencias = asistencias.filter(fecha=fecha)

    asistencias = asistencias[:100]

    return render(request, 'historial.html', {
        'asistencias': asistencias,
        'cursos': cursos,
    })


# ─── GESTIÓN DE FACILITADORES (solo admin) ───
@login_required
def gestionar_facilitadores(request):
    if not request.user.es_administrador:
        return HttpResponseForbidden('No tenés permiso para esta sección.')

    facilitadores = Usuario.objects.filter(rol='facilitador')
    return render(request, 'admin_facilitadores.html', {
        'facilitadores': facilitadores,
    })


# ─── GESTIÓN DE CURSOS ───
@login_required
def gestionar_cursos(request):
    if request.user.es_administrador:
        cursos = Curso.objects.all().prefetch_related('facilitadores')
    else:
        cursos = request.user.cursos_asignados.all().prefetch_related('facilitadores')

    return render(request, 'admin_cursos.html', {
        'cursos': cursos,
    })


# ─── API: Búsqueda por DNI (JSON) ───
@login_required
def api_estudiante_dni(request, dni):
    try:
        est = Estudiante.objects.get(dni=dni)

        # Facilitador solo puede ver estudiantes de sus cursos
        if request.user.es_facilitador:
            mis_cursos = request.user.cursos_asignados.all()
            if est.curso not in mis_cursos:
                return JsonResponse({'encontrado': False})

        return JsonResponse({
            'encontrado': True,
            'id': est.id,
            'nombre': est.nombre,
            'apellido': est.apellido,
            'dni': est.dni,
            'email': est.email,
            'direccion': est.direccion,
            'escuela': est.escuela,
            'curso': str(est.curso) if est.curso else '',
            'problemas_salud': est.problemas_salud,
            'tutor_nombre': est.tutor_nombre,
            'tutor_contacto': est.tutor_contacto,
            'fecha_nacimiento': str(est.fecha_nacimiento) if est.fecha_nacimiento else '',
        })
    except Estudiante.DoesNotExist:
        return JsonResponse({'encontrado': False})


# ─── CREAR CURSO ───
@login_required
def crear_curso(request):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    facilitadores = Usuario.objects.filter(rol='facilitador')
    error = None
    if request.method == 'POST':
        try:
            curso = Curso.objects.create(
                nombre=request.POST.get('nombre'),
                anio=request.POST.get('anio'),
                division=request.POST.get('division'),
            )
            curso.facilitadores.set(request.POST.getlist('facilitadores'))
            return redirect('admin_cursos')
        except Exception as e:
            error = str(e)
    return render(request, 'crear_curso.html', {'facilitadores': facilitadores, 'error': error})


# ─── ELIMINAR CURSO ───
@login_required
def eliminar_curso(request, curso_id):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    curso = get_object_or_404(Curso, id=curso_id)
    if request.method == 'POST':
        curso.delete()
    return redirect('admin_cursos')


# ─── CREAR FACILITADOR ───
@login_required
def crear_facilitador(request):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    error = None
    if request.method == 'POST':
        try:
            user = Usuario.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email', ''),
                dni=request.POST.get('dni'),
                rol='facilitador',
                fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
            )
            return redirect('admin_facilitadores')
        except Exception as e:
            error = str(e)
    return render(request, 'crear_facilitador.html', {'error': error})


# ─── ELIMINAR FACILITADOR ───
@login_required
def eliminar_facilitador(request, facilitador_id):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    facilitador = get_object_or_404(Usuario, id=facilitador_id, rol='facilitador')
    if request.method == 'POST':
        facilitador.delete()
    return redirect('admin_facilitadores')


# ─── EDITAR CURSO ───
@login_required
def editar_curso(request, curso_id):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    curso = get_object_or_404(Curso, id=curso_id)
    facilitadores = Usuario.objects.filter(rol='facilitador')
    error = None
    if request.method == 'POST':
        try:
            curso.nombre = request.POST.get('nombre')
            curso.anio = request.POST.get('anio')
            curso.division = request.POST.get('division')
            curso.facilitadores.set(request.POST.getlist('facilitadores'))
            curso.save()
            return redirect('admin_cursos')
        except Exception as e:
            error = str(e)
    return render(request, 'editar_curso.html', {
        'curso': curso,
        'facilitadores': facilitadores,
        'error': error,
    })


# ─── EDITAR FACILITADOR ───
@login_required
def editar_facilitador(request, facilitador_id):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    facilitador = get_object_or_404(Usuario, id=facilitador_id, rol='facilitador')
    error = None
    if request.method == 'POST':
        try:
            facilitador.first_name = request.POST.get('first_name')
            facilitador.last_name = request.POST.get('last_name')
            facilitador.email = request.POST.get('email', '')
            facilitador.dni = request.POST.get('dni')
            facilitador.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
            password = request.POST.get('password')
            if password:
                facilitador.set_password(password)
            facilitador.save()
            return redirect('admin_facilitadores')
        except Exception as e:
            error = str(e)
    return render(request, 'editar_facilitador.html', {
        'facilitador': facilitador,
        'error': error,
    })

@login_required
def eliminar_estudiante(request, estudiante_id):
    if not request.user.es_administrador:
        return HttpResponseForbidden()
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    if request.method == 'POST':
        estudiante.delete()
    return redirect('estudiantes')