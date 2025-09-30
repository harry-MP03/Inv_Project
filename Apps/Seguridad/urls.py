from django.urls import path, include

urlpatterns = [
    path('Usuarios/', include('Apps.Seguridad.Usuarios.urls')),
]
