from django.contrib import admin
from .models import Cliente
from .models import MarcaRepuesto
from .models import Estado
from .models import Marca
from .models import Tipo
from .models import Vehiculo
from .models import Trabajo
from .models import Repuesto
from .models import Tra_rep

admin.site.register(Cliente)
admin.site.register(MarcaRepuesto)
admin.site.register(Estado)
admin.site.register(Marca)
admin.site.register(Tipo)
admin.site.register(Vehiculo)
admin.site.register(Trabajo)
admin.site.register(Repuesto)
admin.site.register(Tra_rep)

