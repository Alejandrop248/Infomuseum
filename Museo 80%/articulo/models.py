from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

class Piezas(models.Model):
    Cod_pieza = models.IntegerField(primary_key=True, default=0)
    Cod_artesano = models.ForeignKey('Artesano', on_delete=models.CASCADE, null=True)
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Nombre_pieza = models.CharField(max_length=45, default='')
    Composicion_pieza = models.CharField(max_length=45, default='')
    Dimension_pieza = models.CharField(max_length=45, default='')
    Soporte_tecnico_pieza = models.CharField(max_length=45, default='')
    Fecha_pieza = models.DateField()
    Marca_registro_pieza = models.CharField(max_length=45, default='')


class Imagen(models.Model):
    pieza = models.ForeignKey(Piezas, related_name='imagenes', on_delete=models.CASCADE)  # Este es un enlace a la pieza a la que pertenece esta imagen. Si la pieza se elimina, también se eliminará esta imagen.
    imagen = models.ImageField(upload_to='piezas/', null=True, blank=True)  # Este es el campo de la imagen. Las imágenes se subirán al directorio 'piezas/'. Este campo puede estar vacío.


class Donante(models.Model):
    TIPO_ID = [
        ('V', 'VENEZOLANO'),
        ('E', 'EXTRANJERO'),
        ('P', 'RIF PERSONAL'),
        ('J', 'RIF JURIDICO'),
    ]

    tipo_identidad = models.CharField(max_length=1, choices=TIPO_ID, default='V')  # Tipo de identidad del donante
    numero_identidad = models.CharField(max_length=10, unique=True, default='0000000000')
    nombre_apellido = models.CharField(max_length=200)  # Nombre y apellido del donante
    numero_telefono = models.CharField(max_length=15)  # Número de contacto del donante
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.tipo_identidad} {self.numero_identidad} - {self.nombre_apellido}'

@receiver(post_save, sender=Donante)
def log_donante_save(sender, instance, created, **kwargs):
    action = 'creó' if created else 'actualizó'
    Bitacora.objects.create(user=instance.user, action=f'{action} un donante')

@receiver(pre_delete, sender=Donante)
def log_donante_delete(sender, instance, **kwargs):
    Bitacora.objects.create(user=instance.user, action='va a eliminar un donante')

class Bitacora(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username if self.user else "Usuario desconocido"} {self.action} at {self.timestamp}'

@receiver(post_save, sender=Piezas)
def log_pieza_save(sender, instance, created, **kwargs):
    action = 'creó' if created else 'actualizó'
    Bitacora.objects.create(user=instance.user, action=f'{action} una pieza')

@receiver(post_delete, sender=Piezas)
def log_pieza_delete(sender, instance, **kwargs):
    Bitacora.objects.create(action='eliminó una pieza')

# Registra la señal para la eliminación de una pieza
post_delete.connect(log_pieza_delete, sender=Piezas)

class Artesano(models.Model):
    codigo = models.CharField(max_length=100, primary_key=True)
    nombre_y_apellido = models.CharField(max_length=200)
    biografia = models.TextField()

class Referencias(models.Model):
    Codigo_de_Referencia = models.AutoField(primary_key=True)
    Exposiciones = models.CharField(max_length=200)
    Tratamiento = models.CharField(max_length=200)
    Ubicacion_Deposito = models.CharField(max_length=200)

class DatosTecnicos(models.Model):
    Codigo_de_Datos_Tecnicos = models.AutoField(primary_key=True)
    Procedencia = models.CharField(max_length=200)
    Cultura = models.CharField(max_length=200)
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    Propetario_Original = models.CharField(max_length=200)

class EstadoConservacion(models.Model):
    Codigo_de_Estado_de_Conservacion = models.AutoField(primary_key=True)
    Condicion = models.CharField(max_length=200)
    Integridad = models.CharField(max_length=200)

class Prestamo(models.Model):
    Cod_prestamo = models.IntegerField(primary_key=True)
    Fecha_prestamo = models.DateField(editable=True)
    Fecha_entrega = models.DateField(editable=True)
    Confirmacion = models.CharField(max_length=2)
    Observacion_general = models.CharField(max_length=45, blank=True, null=True)
    Fecha_devolucion = models.DateField(blank=True, null=True)
    Estatus = models.CharField(max_length=45)

class Donante_pieza(models.Model):
    Cod_pieza = models.ForeignKey('Piezas', on_delete=models.CASCADE)
    Cod_ced_rif = models.IntegerField(primary_key=True)
    Fecha_Donacion_Hora = models.DateTimeField()

class Solicitud(models.Model):
    Cod_solicitud = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=45)
    Direccion = models.CharField(max_length=45)
    Telefono = models.CharField(max_length=45)
    Email = models.EmailField(max_length=45)
    Fecha_solicitud_prestamo = models.DateTimeField(auto_now_add=True)
    Prestatario_Cod_rif = models.ForeignKey('Prestatario', on_delete=models.CASCADE)
    Prestamo_Cod_prestamo = models.ForeignKey('Prestamo', on_delete=models.CASCADE)

class Prestatario(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    Email = models.EmailField(max_length=45)
    Telefono = models.CharField(max_length=45)

