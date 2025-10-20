# Generador de Archivo ODS desde PDFs de Faltas

Herramienta para convertir automáticamente tus PDFs de control de asistencia en un único archivo de hoja de cálculo (ODS) con una pestaña por cada materia.

**¿Tienes 10 PDFs de faltas de diferentes materias?** Este programa los convierte automáticamente en un único archivo Excel/ODS.

## ✨ ¿Qué hace este programa?

Imagina que tienes estos PDFs:
- `faltas_matematicas.pdf`
- `faltas_lengua.pdf`
- `faltas_ingles.pdf`
- ... (y más)

El programa los lee todos y crea **un único archivo** llamado `faltas_consolidado.ods` con:
- Una pestaña llamada "Matemáticas" con los datos del primer PDF
- Una pestaña llamada "Lengua" con los datos del segundo PDF
- Una pestaña llamada "Inglés" con los datos del tercer PDF
- ... y así sucesivamente

**🔄 Funcionamiento incremental:** Si ejecutas el programa varias veces con PDFs de diferentes períodos:
- Si el archivo `faltas_consolidado.ods` ya existe, el programa lo actualizará
- Si el período del PDF ya existe en el archivo, sobrescribirá los datos
- Si es un período nuevo, añadirá 3 columnas nuevas (Justificadas, Injustificadas, Retrasos) para ese período
- Las columnas se reorganizarán automáticamente agrupadas por tipo (todas las Justificadas juntas, etc.)
- Las dos columnas TOTAL se actualizarán automáticamente: una suma Justificadas + Injustificadas, otra suma solo Retrasos

Puedes abrir el archivo generado con **Excel**, **LibreOffice Calc** o **Google Sheets**.

---

## 🎯 Tres formas de usar este programa

### **OPCIÓN 1: Usando ChatGPT Plus (LA MÁS FÁCIL - SIN INSTALAR NADA)** ⭐ Recomendado para docentes

Si tienes una suscripción a ChatGPT Plus, esta es la forma más sencilla:

#### Pasos:

1. **Ve a ChatGPT**: https://chat.openai.com
2. **Descarga el archivo del programa**:
   - Ve a: https://github.com/balejosg/conteo_faltas_desde_raices
   - Haz clic en `generar_faltas_ods.py`
   - Haz clic en el botón "Download raw file" (ícono de descarga)
   - Guárdalo en tu computadora
3. **En ChatGPT, haz clic en el ícono de clip 📎** (adjuntar archivos)
4. **Sube todos tus PDFs de faltas** (puedes seleccionar varios a la vez)
5. **Sube también el archivo** `generar_faltas_ods.py` que descargaste
6. **Escribe este mensaje**:
   ```
   Ejecuta el script generar_faltas_ods.py con los PDFs que he subido
   ```
7. **Espera unos segundos** mientras ChatGPT procesa los archivos
8. **Descarga el archivo** `faltas_consolidado.ods` que ChatGPT te genera
9. **Abre el archivo** con Excel, LibreOffice Calc o Google Sheets

**¡Listo!** No necesitas instalar nada en tu computadora.

---

### **OPCIÓN 2: Instalación en Windows** 🪟

#### Paso 1: Descargar e instalar Python

1. **Ve a**: https://www.python.org/downloads/
2. **Descarga Python** haciendo clic en el botón amarillo "Download Python"
3. **Ejecuta el instalador** que descargaste
4. **⚠️ MUY IMPORTANTE**: Marca la casilla que dice **"Add Python to PATH"** (está abajo en la primera pantalla)
5. Haz clic en **"Install Now"**
6. Espera a que termine la instalación
7. Haz clic en **"Close"**

#### Paso 2: Descargar este programa

1. **Ve a**: https://github.com/balejosg/conteo_faltas_desde_raices
2. **Haz clic en el botón verde** que dice **"Code"**
3. **Haz clic en "Download ZIP"**
4. **Guarda el archivo** en tu carpeta de Descargas
5. **Haz clic derecho sobre el archivo ZIP** → **"Extraer todo"**
6. Elige una carpeta donde extraerlo (por ejemplo, tu Escritorio)

#### Paso 3: Instalar las dependencias

1. **Abre la carpeta** donde extrajiste los archivos
2. **Haz doble clic** en el archivo `INSTALAR_WINDOWS.bat`
3. Se abrirá una ventana negra que instalará todo automáticamente
4. Espera a que termine (dirá "Presiona cualquier tecla para continuar...")
5. Presiona cualquier tecla para cerrar la ventana

#### Paso 4: Usar el programa

1. **Copia todos tus PDFs de faltas** en la carpeta del programa (donde está el archivo `generar_faltas_ods.py`)
2. **Haz doble clic** en el archivo `EJECUTAR_WINDOWS.bat`
3. Se abrirá una ventana que mostrará el progreso
4. Cuando termine, encontrarás un archivo nuevo llamado **`faltas_consolidado.ods`**
5. **Abre ese archivo** con Excel o LibreOffice Calc

---

### **OPCIÓN 3: Instalación en Mac** 🍎

#### Paso 1: Verificar si tienes Python instalado

1. **Abre la aplicación "Terminal"**:
   - Presiona `Cmd + Espacio`
   - Escribe "Terminal"
   - Presiona Enter
2. **Escribe** este comando y presiona Enter:
   ```bash
   python3 --version
   ```
3. Si aparece algo como "Python 3.x.x", ya tienes Python instalado ✅
4. Si dice "command not found", necesitas instalar Python:
   - Ve a: https://www.python.org/downloads/
   - Descarga Python
   - Abre el instalador y sigue las instrucciones

#### Paso 2: Descargar este programa

1. **Ve a**: https://github.com/balejosg/conteo_faltas_desde_raices
2. **Haz clic en el botón verde** que dice **"Code"**
3. **Haz clic en "Download ZIP"**
4. **Abre el archivo ZIP** (normalmente se abre automáticamente)
5. **Arrastra la carpeta** a tu Escritorio o donde prefieras

#### Paso 3: Instalar las dependencias

1. **Abre la aplicación "Terminal"** (si la cerraste):
   - Presiona `Cmd + Espacio`
   - Escribe "Terminal"
   - Presiona Enter
2. **Ve a la carpeta del programa**. Escribe:
   ```bash
   cd
   ```
   (¡No presiones Enter todavía!)
3. **Arrastra la carpeta del programa** desde el Finder hasta la ventana de Terminal
4. **Ahora sí presiona Enter**
5. **Escribe** este comando y presiona Enter:
   ```bash
   sh INSTALAR_MAC.sh
   ```
6. Espera a que termine la instalación

#### Paso 4: Usar el programa

1. **Copia todos tus PDFs de faltas** en la carpeta del programa
2. **En Terminal, asegúrate de estar en la carpeta del programa** (repite el paso 2 y 3 de arriba si cerraste Terminal)
3. **Escribe** este comando y presiona Enter:
   ```bash
   sh EJECUTAR_MAC.sh
   ```
4. El programa procesará todos los PDFs
5. Cuando termine, encontrarás un archivo nuevo llamado **`faltas_consolidado.ods`**
6. **Abre ese archivo** con Excel, Numbers o LibreOffice Calc

---

## 📋 Formato de los PDFs

El programa funciona con PDFs que tengan este formato:

```
Alumno/a    [Nombre de tu materia]    FJ  FI  R  TOTAL
--------------------------------------------------------
García López, María                    0   2   1   3
Martínez Pérez, Juan                   1   0   0   1
```

**Requisitos:**
- Debe tener una tabla con columnas
- La cabecera debe contener "Alumno/a" y "TOTAL"
- Entre "Alumno/a" y "TOTAL" debe estar el nombre de la materia
- El PDF debe incluir una línea con "Periodo: (DD/MM/YYYY - DD/MM/YYYY)"
- Cada fila debe tener: Nombre del alumno + números

**Nota:** El programa:
- Extrae automáticamente el período del PDF y lo añade a las columnas
- Convierte las abreviaturas FJ, FI, R en "Justificadas", "Injustificadas" y "Retrasos"
- Organiza las columnas agrupadas por tipo (todas las Justificadas juntas, todas las Injustificadas juntas, todos los Retrasos juntos)
- Añade dos columnas TOTAL con fórmulas: una que suma Justificadas + Injustificadas, otra que suma solo Retrasos

---

## 🔄 Uso incremental: Múltiples períodos

El programa está diseñado para trabajar con múltiples períodos de forma acumulativa:

### Primera ejecución
Coloca los PDFs del primer período (ejemplo: septiembre-octubre) en la carpeta y ejecuta el programa. Se creará `faltas_consolidado.ods` con los datos de ese período.

### Segunda ejecución (período nuevo)
1. Coloca los PDFs del segundo período (ejemplo: noviembre-diciembre) en la carpeta
2. Ejecuta el programa de nuevo
3. El programa:
   - Detectará el archivo existente
   - Añadirá 3 columnas nuevas para el nuevo período en cada hoja (una Justificadas, una Injustificadas, una Retrasos)
   - Las columnas se reorganizarán automáticamente agrupadas por tipo
   - Actualizará las fórmulas de los dos TOTAL para sumar todos los períodos
4. Ahora tendrás 6 columnas de datos + 2 TOTAL (3 columnas × 2 períodos + 2 totales)

### Segunda ejecución (mismo período, datos corregidos)
Si ejecutas el programa con PDFs del mismo período que ya existe:
- Los datos del período se **sobrescribirán** con los nuevos valores
- Útil si hubo algún error en los PDFs originales y necesitas corregir

### Alumnos nuevos o que se dan de baja
- Si un alumno aparece en un período posterior, se añadirá al final de la lista
- Si un alumno no aparece en un PDF, las celdas de ese período quedarán vacías para ese alumno

---

## ❓ Problemas comunes y soluciones

### "No se encontraron archivos PDF"
**Solución:** Asegúrate de que los PDFs están en la misma carpeta que el programa `generar_faltas_ods.py`

### "No se pudo encontrar el nombre de la materia"
**Solución:** Verifica que tu PDF tiene una línea con "Alumno/a" [nombre materia] "TOTAL"

### En Windows: "python no se reconoce como un comando"
**Solución:** No marcaste la casilla "Add Python to PATH" durante la instalación. Desinstala Python y vuelve a instalarlo, asegurándote de marcar esa casilla.

### En Mac: "permission denied"
**Solución:** Escribe `chmod +x INSTALAR_MAC.sh EJECUTAR_MAC.sh` en Terminal y vuelve a intentar

---

## 🔒 Privacidad y Seguridad

⚠️ **IMPORTANTE**:
- Este repositorio NO incluye PDFs de ejemplo con datos reales para proteger la privacidad de los estudiantes
- Los PDFs que proceses quedan en tu computadora (o en ChatGPT temporalmente)
- No compartas los archivos generados si contienen información personal
- Cumple con las normativas de protección de datos de tu institución

---

## 📊 ¿Qué columnas tiene el archivo generado?

Cada hoja del archivo ODS tendrá estas columnas organizadas **por tipo de falta**:

- **Alumno/a**: Nombre completo del estudiante
- **Justificadas (período)**: Una columna por cada período con las faltas justificadas (número)
- **Injustificadas (período)**: Una columna por cada período con las faltas injustificadas (número)
- **Retrasos (período)**: Una columna por cada período con los retrasos (número)
- **TOTAL Justificadas y Injustificadas**: Suma automática de TODAS las Justificadas + TODAS las Injustificadas de todos los períodos (fórmula)
- **TOTAL Retrasos**: Suma automática de TODOS los Retrasos de todos los períodos (fórmula)

**Ejemplo con un solo período:**
```
Alumno/a | Justificadas (10/09/2025 - 11/09/2025) | Injustificadas (10/09/2025 - 11/09/2025) | Retrasos (10/09/2025 - 11/09/2025) | TOTAL Justificadas y Injustificadas | TOTAL Retrasos
```

**Ejemplo con múltiples períodos (columnas agrupadas por tipo):**
```
Alumno/a | Justificadas (10/09 - 11/09) | Justificadas (12/11 - 12/12) | Injustificadas (10/09 - 11/09) | Injustificadas (12/11 - 12/12) | Retrasos (10/09 - 11/09) | Retrasos (12/11 - 12/12) | TOTAL Justificadas y Injustificadas | TOTAL Retrasos
```

**Ventajas de esta organización:**
- **Fácil comparación entre períodos**: Todas las faltas justificadas están juntas, todas las injustificadas juntas, etc.
- **Dos totales separados**: El TOTAL de Retrasos se mantiene separado del TOTAL de Justificadas e Injustificadas
- **Columnas numéricas**: Funcionan como números reales, así que puedes hacer sumas, promedios y otros cálculos directamente en Excel o LibreOffice
- **Fórmulas automáticas**: Los totales se calculan mediante fórmulas y se actualizan automáticamente si modificas cualquier valor

---

## 🆘 ¿Necesitas ayuda?

Si tienes problemas:
1. Lee la sección "Problemas comunes y soluciones" arriba
2. Si no encuentras solución, abre un ticket en: https://github.com/balejosg/conteo_faltas_desde_raices/issues
3. Describe tu problema y qué sistema operativo usas (Windows/Mac)

---

## 👨‍💻 Autor

**Bruno Alejos Gómez**
- GitHub: [@balejosg](https://github.com/balejosg)

---

## 📄 Licencia

Este proyecto es de código abierto y gratuito (Licencia MIT).
