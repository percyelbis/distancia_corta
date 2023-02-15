# variables
latitud = -11.0785
longitud = -77.3211
erp = 'erp'
id_erp = 'OBJECTID'

### -------- pyqgis ---------
erp = QgsProject.instance().mapLayersByName(erp)[0]

# Importar módulos necesarios
from qgis.core import QgsFeature, QgsGeometry, QgsPointXY, QgsVectorLayer

# Crear una geometría de punto
point = QgsPointXY(longitud, latitud)
geometry = QgsGeometry.fromPointXY(point)

# Crear una capa vectorial de puntos
layer_name = 'gnss'
layer = QgsVectorLayer('Point', layer_name, 'memory')
layer.startEditing()  # Iniciar edición de capa

# Crear un objeto de entidad y configurar su geometría
feature = QgsFeature()
feature.setGeometry(geometry)

# Agregar la entidad a la capa
layer.addFeature(feature)
layer.commitChanges()  # Guardar cambios en la capa

# Agregar la capa al proyecto
QgsProject.instance().addMapLayer(layer)
memory = QgsProject.instance().mapLayersByName('gnss')[0]

# distancia mas cercana
processing.runAndLoadResults("qgis:distancetonearesthublinetohub", 
                {'INPUT':memory,
                'HUBS':erp,
                'FIELD':id_erp,
                'UNIT':3, # kimlometros
                'OUTPUT':'TEMPORARY_OUTPUT'})
                
# simbologias
layer1 = QgsProject.instance().mapLayersByName("gnss")[0]
symbol = QgsMarkerSymbol()
symbol.setColor(QColor(12, 180, 120))
symbol.setSize(5)
renderer = QgsSingleSymbolRenderer(symbol)
layer1.setRenderer(renderer)                
# label
layer_settings  = QgsPalLayerSettings()
text_format = QgsTextFormat()

text_format.setFont(QFont("Arial", 12))
text_format.setSize(12)

buffer_settings = QgsTextBufferSettings()
buffer_settings.setEnabled(True)
buffer_settings.setSize(1)
buffer_settings.setColor(QColor("white"))

text_format.setBuffer(buffer_settings)
layer_settings.setFormat(text_format)

layer_settings.fieldName = "HubDist"
layer_settings.placement = 2

layer_settings.enabled = True

layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
my_layer = QgsProject.instance().mapLayersByName('Hub distance')[0]
my_layer.setLabelsEnabled(True)
my_layer.setLabeling(layer_settings)
my_layer.triggerRepaint()

symbol = QgsLineSymbol()
symbol.setColor(QColor(12, 180, 120))
symbol.setWidth(1)
renderer = QgsSingleSymbolRenderer(symbol)
my_layer.setRenderer(renderer)
# expresion

x = my_layer.getFeature(1).attribute(1)
minutos = 0.000022*x**3-0.007834*x**2 + 2.660074*x + 8.346236
# mensaje
from qgis.PyQt.QtWidgets import QMessageBox
# Calcular las horas, minutos
horas = minutos // 60
minutos_restantes = round(minutos % 60,0)

# Crear una ventana emergente con el resultado
mensaje = f"Tiempo de Lectura minima a la Estacion Activa más cercana es: {horas} hora con {minutos_restantes} minutos"
QMessageBox.information(None, "Tiempo de Lectura: ", mensaje)
iface.messageBar().pushMessage("qgis", "Fue todo un exito los calculos!!!", level=Qgis.Info, duration=3)
