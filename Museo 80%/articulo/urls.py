from django.urls import path
from . import views
from .views import listar_artesanos, crear_artesano, mostrar_web, solicitar_prestamo, solicitudes_prestamos, prestatario_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('prestamo/', views.prestamo_list, name='prestamo_list'),
    path('prestamo/<int:pk>/', views.prestamo_detail, name='prestamo_detail'),
    path('prestamo/new/', views.prestamo_new, name='prestamo_new'),
    path('prestamo/<int:pk>/edit/', views.prestamo_edit, name='prestamo_edit'),
    path('prestamo/<int:pk>/delete/', views.prestamo_delete, name='prestamo_delete'),
    path('prestatario/', views.prestatario_list, name='prestatario_list'),
    path('prestatario/<int:pk>/', views.prestatario_detail, name='prestatario_detail'),
    path('prestatario/new/', views.prestatario_new, name='prestatario_new'),
    path('prestatario/<int:pk>/edit/', views.prestatario_edit, name='prestatario_edit'),
    path('prestatario/<int:pk>/delete/', views.prestatario_delete, name='prestatario_delete'),
    path('solicitud/', views.solicitud_list, name='solicitud_list'),
    path('solicitud/<int:pk>/', views.solicitud_detail, name='solicitud_detail'),
    path('solicitud/new/', views.solicitud_new, name='solicitud_new'),
    path('solicitud/<int:pk>/edit/', views.solicitud_edit, name='solicitud_edit'),
    path('solicitud/<int:pk>/delete/', views.solicitud_delete, name='solicitud_delete'),
    path('web/', mostrar_web, name='mostrar_web'),
    path('web/solicitar_prestamo', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('web/solicitudes_prestamos', solicitudes_prestamos, name='solicitudes_prestamos'),
    path('web/consultar/', views.consultar_piezas, name='consultar_piezas'),
    path('referencias/new/', views.nueva_referencia, name='nueva_referencia'),
    path('referencias/', views.listar_referencias, name='referencias'),
    path('referencias/editar/<int:pk>/', views.editar_referencia, name='editar_referencia'),
    path('referencias/eliminar/<int:pk>/', views.eliminar_referencia, name='eliminar_referencia'),
    path('referencias/', views.listar_referencias, name='listar_referencias'),
    path('datostecnicos/new/', views.nuevo_dato_tecnico, name='nuevo_dato_tecnico'),
    path('datostecnicos/', views.listar_datos_tecnicos, name='datostecnicos'),
    path('datostecnicos/editar/<int:pk>/', views.editar_dato_tecnico, name='editar_dato_tecnico'),
    path('datostecnicos/eliminar/<int:pk>/', views.eliminar_dato_tecnico, name='eliminar_dato_tecnico'),
    path('datostecnicos/', views.listar_datos_tecnicos, name='listar_datos_tecnicos'),
    path('estadoconservacion/new/', views.nuevo_estado_conservacion, name='nuevo_estado_conservacion'),
    path('estadoconservacion/', views.listar_estados_conservacion, name='estadoconservacion'),
    path('estadoconservacion/editar/<int:pk>/', views.editar_estado_conservacion, name='editar_estado_conservacion'),
    path('estadoconservacion/eliminar/<int:pk>/', views.eliminar_estado_conservacion, name='eliminar_estado_conservacion'),
    path('estadoconservacion/', views.listar_estados_conservacion, name='listar_estados_conservacion'),
    path('crear_artesano/', crear_artesano, name='crear_artesano'),
    path('artesanos/', listar_artesanos, name='listar_artesanos'),
    path('', views.vista_login, name='login'), # La URL raíz de tu sitio redirige a la vista de inicio de sesión.
    path('crear_usuario/', views.create_user, name='create_user'), # Esta URL lleva a la vista para crear un nuevo usuario.
    path('pantalla_principal/', views.vista_principal, name='pantalla_principal'), # Esta URL lleva a la vista principal de tu aplicación.
    path('agregar-pieza/', views.agregar_pieza, name='agregar_pieza'), # Esta URL lleva a la vista para agregar una nueva pieza.
    path('consultar/', views.consultar_piezas, name='consultar_piezas'), # Esta URL lleva a la vista para consultar todas las piezas.
    path('vista_principal/', views.vista_principal, name='vista_principal'), # Esta URL lleva a la vista para editar una pieza existente. Se necesita el ID de la pieza en la URL.
    path('editar/<int:id_pieza>/', views.editar_piezas, name='editar_piezas'), # Esta URL lleva a la vista para eliminar una pieza existente. Se necesita el ID de la pieza en la URL.
    path('eliminar/<int:id_pieza>/', views.eliminar_piezas, name='eliminar_piezas'), # Esta URL lleva a la vista para cerrar la sesión del usuario.
    path('logout/', views.logout_view, name='logout'), # Esta URL lleva a la vista para cerrar la sesión del usuario.
    path('accounts/login/', views.vista_login, name='login'), # Esta URL también lleva a la vista de inicio de sesión.
    path('registrar_donante/', views.registrar_donante, name='registrar_donante'),
    path('listar_donantes/', views.listar_donantes, name='listar_donantes'),
    path('editar_donante/<str:numero_identidad>/', views.editar_donante, name='editar_donante'),
    path('eliminar_donante/<str:numero_identidad>/', views.eliminar_donante, name='eliminar_donante'),
    path('bitacora/', views.bitacora_view, name='bitacora'),
]

if settings.DEBUG:
    # En modo de depuración, Django servirá los archivos multimedia desde MEDIA_ROOT.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 