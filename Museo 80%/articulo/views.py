from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import PiezasForm, ImagenForm, UserForm, DonanteForm, ArtesanoForm, EstadoConservacionForm, DatosTecnicosForm, ReferenciasForm, DonantePiezaForm, SolicitudForm, PrestatarioForm, PrestamoForm
from .models import Piezas, Imagen, Donante, Bitacora, Artesano, EstadoConservacion, Referencias, DatosTecnicos, Donante_pieza, Solicitud, Prestatario, Prestamo
@login_required
def create_user(request):
    # Esta vista permite al superusuario crear nuevos usuarios.
    # Solo se puede acceder a esta vista si el usuario está autenticado.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if request.user.is_superuser:  # Solo permitir al superusuario crear nuevos usuarios
            User.objects.create_user(username=username, password=password, email=email)
            return HttpResponse('Usuario creado exitosamente')
        else:
            return HttpResponse('No tienes permiso para crear usuarios')
    else:
        form = UserForm()  # Crea una instancia del formulario
    return render(request, 'crear_usuario.html', {'form': form})

def vista_principal(request):
    # Esta es la vista de la aplicación.
    # Cuando un usuario visita tu sitio, esta es la primera página que verá.
    return render(request, 'pantalla_principal.html')

@login_required
def agregar_pieza(request):
    # Esta vista permite a los usuarios agregar nuevas piezas a la base de datos.
    # Si la solicitud es POST, se valida el formulario y se guarda la nueva pieza.
    # Si la solicitud es GET, se muestra el formulario para agregar una nueva pieza.
    if request.method == 'POST':
        form = PiezasForm(request.POST)
        if form.is_valid():
            pieza = form.save(commit=False)
            pieza.user = request.user
            pieza.save()
            for file in request.FILES.getlist('imagenes'):
                Imagen.objects.create(imagen=file, pieza=pieza)
            return redirect('consultar_piezas')
    else:
        form = PiezasForm()

    return render(request, 'agregar_pieza.html', {'form': form})

def consultar_piezas(request):
    # Esta vista muestra todas las piezas en la base de datos.
    # Se obtienen todas las piezas con Piezas.objects.all() y luego se pasan al template.
    piezas = Piezas.objects.all()
    return render(request, 'consultar_piezas.html', {'piezas': piezas})

def editar_piezas(request, id_pieza):
    pieza = get_object_or_404(Piezas, Cod_pieza=id_pieza)
    if request.method == 'POST':
        form = PiezasForm(request.POST, instance=pieza)
        if form.is_valid():
            form.save()
            return redirect('consultar_piezas')
    else:
        form = PiezasForm(instance=pieza)

    return render(request, 'editar_piezas.html', {'form': form})


def eliminar_piezas(request, id_pieza):
    # Esta vista permite a los usuarios eliminar piezas existentes.
    # Si la solicitud es POST, se elimina la pieza.
    # Si la solicitud es GET, se redirige al usuario a la página de consulta de piezas.
    pieza = get_object_or_404(Piezas, Cod_pieza=id_pieza)
    if request.method == 'POST':
        pieza.delete()
        return redirect('consultar_piezas')  # Redirige a la página de consulta de piezas
    # Si no es una solicitud POST, simplemente redirige sin confirmación
    return redirect('consultar_piezas')

def vista_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Aquí creamos el registro en la bitácora
            Bitacora.objects.create(user=user, action='inició sesión')
            return redirect('vista_principal')
    return render(request, 'login.html')

def logout_view(request):
    # Antes de cerrar la sesión, creamos el registro en la bitácora
    Bitacora.objects.create(user=request.user, action='cerró sesión')
    logout(request)
    return redirect('login')

@login_required
def registrar_donante(request):
    if request.method == 'POST':
        form = DonanteForm(request.POST)
        if form.is_valid():
            donante = form.save(commit=False)
            donante.user = request.user
            donante.save()
            return redirect('listar_donantes')
    else:
        form = DonanteForm()
    return render(request, 'registrar_donante.html', {'form': form})

def listar_donantes(request):
    donantes = Donante.objects.all()
    return render(request, 'listar_donantes.html', {'donantes': donantes})

def editar_donante(request, numero_identidad):
    donante = get_object_or_404(Donante, numero_identidad=numero_identidad)
    if request.method == 'POST':
        form = DonanteForm(request.POST, instance=donante)
        if form.is_valid():
            form.save()
            return redirect('listar_donantes')
    else:
        form = DonanteForm(instance=donante)
    return render(request, 'editar_donante.html', {'form': form})

@login_required
def eliminar_donante(request, numero_identidad):
    donante = Donante.objects.get(numero_identidad=numero_identidad)
    if request.method == 'POST':
        Bitacora.objects.filter(user=donante.user).delete()
        donante.delete()
        if request.user.is_authenticated:
            Bitacora.objects.create(user=request.user, action='eliminó un donante')
        return redirect('listar_donantes')
    return render(request, 'eliminar_donante.html', {'donante': donante})

def bitacora_view(request):
    bitacora = Bitacora.objects.all().order_by('-timestamp')
    return render(request, 'bitacora.html', {'bitacora': bitacora})

def crear_artesano(request):
    if request.method == 'POST':
        form = ArtesanoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vista_principal')
    else:
        form = ArtesanoForm()
    return render(request, 'crear_artesano.html', {'form': form})

def listar_artesanos(request):
    artesanos = Artesano.objects.all()
    return render(request, 'listar_artesanos.html', {'artesanos': artesanos})

def nueva_referencia(request):
    if request.method == "POST":
        form = ReferenciasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referencias')
    else:
        form = ReferenciasForm()
    return render(request, 'nueva_referencia.html', {'form': form})

def editar_referencia(request, pk):
    referencia = get_object_or_404(Referencias, pk=pk)
    if request.method == "POST":
        form = ReferenciasForm(request.POST, instance=referencia)
        if form.is_valid():
            form.save()
            return redirect('referencias')
    else:
        form = ReferenciasForm(instance=referencia)
    return render(request, 'editar_referencia.html', {'form': form})

def eliminar_referencia(request, pk):
    referencia = get_object_or_404(Referencias, pk=pk)
    if request.method == "POST":
        referencia.delete()
        return redirect('referencias')
    return render(request, 'eliminar_referencia.html', {'object': referencia})

def listar_referencias(request):
    referencias = Referencias.objects.all()
    return render(request, 'listar_referencias.html', {'referencias': referencias})

def nuevo_dato_tecnico(request):
    if request.method == "POST":
        form = DatosTecnicosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datostecnicos')
    else:
        form = DatosTecnicosForm()
    return render(request, 'nuevo_dato_tecnico.html', {'form': form})

def editar_dato_tecnico(request, pk):
    dato_tecnico = get_object_or_404(DatosTecnicos, pk=pk)
    if request.method == "POST":
        form = DatosTecnicosForm(request.POST, instance=dato_tecnico)
        if form.is_valid():
            form.save()
            return redirect('datostecnicos')
    else:
        form = DatosTecnicosForm(instance=dato_tecnico)
    return render(request, 'editar_dato_tecnico.html', {'form': form})

def eliminar_dato_tecnico(request, pk):
    dato_tecnico = get_object_or_404(DatosTecnicos, pk=pk)
    if request.method == "POST":
        dato_tecnico.delete()
        return redirect('datostecnicos')
    return render(request, 'eliminar_dato_tecnico.html', {'object': dato_tecnico})

def listar_datos_tecnicos(request):
    datos_tecnicos = DatosTecnicos.objects.all()
    return render(request, 'listar_datos_tecnicos.html', {'datos_tecnicos': datos_tecnicos})

def nuevo_estado_conservacion(request):
    if request.method == "POST":
        form = EstadoConservacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estadoconservacion')
    else:
        form = EstadoConservacionForm()
    return render(request, 'nuevo_estado_conservacion.html', {'form': form})

def editar_estado_conservacion(request, pk):
    estado_conservacion = get_object_or_404(EstadoConservacion, pk=pk)
    if request.method == "POST":
        form = EstadoConservacionForm(request.POST, instance=estado_conservacion)
        if form.is_valid():
            form.save()
            return redirect('estadoconservacion')
    else:
        form = EstadoConservacionForm(instance=estado_conservacion)
    return render(request, 'editar_estado_conservacion.html', {'form': form})

def eliminar_estado_conservacion(request, pk):
    estado_conservacion = get_object_or_404(EstadoConservacion, pk=pk)
    if request.method == "POST":
        estado_conservacion.delete()
        return redirect('estadoconservacion')
    return render(request, 'eliminar_estado_conservacion.html', {'object': estado_conservacion})

def listar_estados_conservacion(request):
    estados_conservacion = EstadoConservacion.objects.all()
    return render(request, 'listar_estados_conservacion.html', {'estados_conservacion': estados_conservacion})

def mostrar_web(request):
    piezas = Piezas.objects.all()
    return render(request, 'web.html', {'piezas': piezas})

def solicitar_prestamo(request):
    if request.method == 'POST':
        form = SolicitudPrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mostrar_web')
    else:
        form = SolicitudPrestamoForm()
    return render(request, 'solicitar_prestamo.html', {'form': form})

def solicitudes_prestamos(request):
    solicitudes = Prestamo.objects.all() # Obtén todas las solicitudes de préstamo
    return render(request, 'solicitudes_prestamos.html', {'solicitudes': solicitudes})

def donante_pieza_list(request):
    donantes = Donante_pieza.objects.all()
    return render(request, 'donante_pieza_list.html', {'donantes': donantes})

def donante_pieza_detail(request, pk):
    donante = get_object_or_404(Donante_pieza, pk=pk)
    return render(request, 'app/donante_pieza_detail.html', {'donante': donante})

def donante_pieza_new(request):
    if request.method == "POST":
        form = DonantePiezaForm(request.POST)
        if form.is_valid():
            donante = form.save(commit=False)
            donante.save()
            return redirect('donante_pieza_detail', pk=donante.pk)
    else:
        form = DonantePiezaForm()
    return render(request, 'donante_pieza_edit.html', {'form': form})

def donante_pieza_edit(request, pk):
    donante = get_object_or_404(Donante_pieza, pk=pk)
    if request.method == "POST":
        form = DonantePiezaForm(request.POST, instance=donante)
        if form.is_valid():
            donante = form.save(commit=False)
            donante.save()
            return redirect('donante_pieza_detail', pk=donante.pk)
    else:
        form = DonantePiezaForm(instance=donante)
    return render(request, 'donante_pieza_edit.html', {'form': form})

def donante_pieza_delete(request, pk):
    donante = get_object_or_404(Donante_pieza, pk=pk)
    if request.method == "POST":
        donante.delete()
        return redirect('donante_pieza_list')
    return render(request, 'donante_pieza_confirm_delete.html', {'donante': donante})

def solicitud_list(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'solicitud_list.html', {'solicitudes': solicitudes})

def solicitud_detail(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    return render(request, 'solicitud_detail.html', {'solicitud': solicitud})

def solicitud_new(request):
    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.save()
            return redirect('solicitud_detail', pk=solicitud.pk)
    else:
        form = SolicitudForm()
    return render(request, 'solicitud_edit.html', {'form': form})

def solicitud_edit(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.save()
            return redirect('solicitud_detail', pk=solicitud.pk)
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'solicitud_edit.html', {'form': form})

def solicitud_delete(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        solicitud.delete()
        return redirect('solicitud_list')
    return render(request, 'solicitud_confirm_delete.html', {'solicitud': solicitud})

def prestatario_list(request):
    prestatarios = Prestatario.objects.all()
    return render(request, 'prestatario_list.html', {'prestatarios': prestatarios})

def prestatario_detail(request, pk):
    prestatario = get_object_or_404(Prestatario, pk=pk)
    return render(request, 'prestatario_detail.html', {'prestatario': prestatario})

def prestatario_new(request):
    if request.method == "POST":
        form = PrestatarioForm(request.POST)
        if form.is_valid():
            prestatario = form.save(commit=False)
            prestatario.save()
            return redirect('prestatario_detail', pk=prestatario.pk)
    else:
        form = PrestatarioForm()
    return render(request, 'prestatario_edit.html', {'form': form})

def prestatario_edit(request, pk):
    prestatario = get_object_or_404(Prestatario, pk=pk)
    if request.method == "POST":
        form = PrestatarioForm(request.POST, instance=prestatario)
        if form.is_valid():
            prestatario = form.save(commit=False)
            prestatario.save()
            return redirect('prestatario_detail', pk=prestatario.pk)
    else:
        form = PrestatarioForm(instance=prestatario)
    return render(request, 'prestatario_edit.html', {'form': form})

def prestatario_delete(request, pk):
    prestatario = get_object_or_404(Prestatario, pk=pk)
    if request.method == "POST":
        prestatario.delete()
        return redirect('prestatario_list')
    return render(request, 'prestatario_confirm_delete.html', {'prestatario': prestatario})

def prestamo_list(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'prestamo_list.html', {'prestamos': prestamos})

def prestamo_detail(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    return render(request, 'prestamo_detail.html', {'prestamo': prestamo})

def prestamo_new(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.save()
            return redirect('prestamo_detail', pk=prestamo.pk)
    else:
        form = PrestamoForm()
    return render(request, 'prestamo_edit.html', {'form': form})

def prestamo_edit(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == "POST":
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.save()
            return redirect('prestamo_detail', pk=prestamo.pk)
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'prestamo_edit.html', {'form': form})

def prestamo_delete(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == "POST":
        prestamo.delete()
        return redirect('prestamo_list')
    return render(request, 'prestamo_confirm_delete.html', {'prestamo': prestamo})
