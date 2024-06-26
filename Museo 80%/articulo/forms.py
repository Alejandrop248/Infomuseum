from django import forms
from .models import Piezas, Imagen, Donante, Artesano, EstadoConservacion, DatosTecnicos, Referencias, Solicitud, Donante_pieza, Prestamo, Prestatario
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    # Este formulario se utiliza para crear un nuevo usuario.
    # El formulario incluye los campos 'username', 'email' y 'password'.
    # La contraseña se guarda de forma segura utilizando el método set_password().
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class PiezasForm(forms.ModelForm):
    # Este formulario se utiliza para crear o editar una pieza.
    # El formulario incluye los campos 'nombre', 'ficha_historica', 'fecha_de_ingreso' y 'personal_ingresante'.
    # La fecha de ingreso se selecciona a través de un widget de selección de fecha.
    fecha_de_ingreso = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1980, 2030))
    )

    class Meta:
        model = Piezas
        fields = ['Usuario', 'Cod_pieza', 'Cod_artesano', 'Nombre_pieza', 'Composicion_pieza', 'Dimension_pieza', 'Soporte_tecnico_pieza', 'Fecha_pieza', 'Marca_registro_pieza']

class ImagenForm(forms.ModelForm):
    # Este formulario se utiliza para subir una imagen.
    # El formulario incluye el campo 'imagen'.
    class Meta:
        model = Imagen
        fields = ['imagen']

class DonanteForm(forms.ModelForm):
    class Meta:
        model = Donante
        fields = ['tipo_identidad', 'numero_identidad', 'nombre_apellido', 'numero_telefono']

class ArtesanoForm(forms.ModelForm):
    class Meta:
        model = Artesano
        fields = ['codigo', 'nombre_y_apellido', 'biografia']

class ReferenciasForm(forms.ModelForm):
    class Meta:
        model = Referencias
        fields = ['Exposiciones', 'Tratamiento', 'Ubicacion_Deposito']

class DatosTecnicosForm(forms.ModelForm):
    class Meta:
        model = DatosTecnicos
        fields = ['Procedencia', 'Cultura', 'Valor', 'Propetario_Original']

class EstadoConservacionForm(forms.ModelForm):
    class Meta:
        model = EstadoConservacion
        fields = ['Condicion', 'Integridad']

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['Cod_solicitud', 'Nombre', 'Direccion', 'Telefono', 'Email', 'Fecha_solicitud_prestamo', 'Prestatario_Cod_rif', 'Prestamo_Cod_prestamo']
        exclude = ['Fecha_solicitud_prestamo']

class DonantePiezaForm(forms.ModelForm):
    class Meta:
        model = Donante_pieza
        fields = ['Cod_pieza', 'Cod_ced_rif', 'Fecha_Donacion_Hora']

class PrestamoForm(forms.ModelForm):
    ESTATUS_CHOICES = [
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
        # Agrega aquí más opciones según tus necesidades
    ]

    Estatus = forms.ChoiceField(choices=ESTATUS_CHOICES)

    class Meta:
        model = Prestamo
        fields = ['Fecha_prestamo', 'Fecha_entrega','Observacion_general', 'Fecha_devolucion', 'Estatus']

class PrestatarioForm(forms.ModelForm):
    class Meta:
        model = Prestatario
        fields = ['nombre', 'direccion']