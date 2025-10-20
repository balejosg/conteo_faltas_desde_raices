# Generador de Archivo ODS desde PDFs de Faltas

Script de Python para convertir múltiples PDFs de control de asistencia (faltas) en un único archivo de hoja de cálculo ODS con múltiples pestañas, una por cada materia.

## Características

- ✅ Procesa múltiples PDFs automáticamente
- ✅ Genera un único archivo ODS con una hoja por materia
- ✅ Extrae automáticamente el nombre de cada materia
- ✅ Las columnas numéricas (FJ, FI, R) se tratan como números para permitir cálculos
- ✅ Compatible con LibreOffice Calc, Excel y otras hojas de cálculo
- ✅ **Compatible con ChatGPT Plus y otros chatbots con Code Interpreter**

## Requisitos

### Opción 1: Instalación local

- Python 3.7 o superior
- Librería `pdfplumber`

### Opción 2: Usar en ChatGPT Plus (sin instalación)

No necesitas instalar nada, solo sube los PDFs y el script a ChatGPT Plus.

## Instalación (para uso local)

### 1. Clona este repositorio

```bash
git clone https://github.com/balejosg/conteo_faltas_desde_raices.git
cd conteo_faltas_desde_raices
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

o manualmente:

```bash
pip install pdfplumber
```

## Uso

### Opción A: Uso Local

1. **Coloca todos tus PDFs de faltas en el mismo directorio** que el script `generar_faltas_ods.py`

2. **Ejecuta el script:**

```bash
python3 generar_faltas_ods.py
```

3. **Resultado:** Se generará un archivo llamado `faltas_consolidado.ods` con todas las materias.

### Opción B: Uso en ChatGPT Plus (Code Interpreter)

1. Abre ChatGPT Plus y activa el modo Code Interpreter
2. Sube todos tus PDFs de faltas
3. Sube el script `generar_faltas_ods.py`
4. Escribe: "Ejecuta el script generar_faltas_ods.py con los PDFs que he subido"
5. ChatGPT instalará automáticamente las dependencias, procesará los PDFs y te permitirá descargar el archivo ODS generado

## Formato de los PDFs

El script espera PDFs con el siguiente formato:

- Una tabla con columnas: **Alumno/a**, **[Nombre de Materia]**, **FJ**, **FI**, **R**, **TOTAL**
- El nombre de la materia debe estar entre las palabras "Alumno/a" y "TOTAL" en la cabecera
- Cada fila debe contener: Nombre del alumno/a seguido de números separados por espacios

### Ejemplo de estructura esperada:

```
Alumno/a    Programación de servicios y procesos    FJ  FI  R  TOTAL
---------------------------------------------------------------
García López, María                                  0   2   1   3
Martínez Pérez, Juan                                 1   0   0   1
```

## Columnas en el archivo ODS generado

Cada hoja del archivo ODS contendrá:

- **Alumno/a**: Nombre del estudiante (texto)
- **FJ**: Faltas Justificadas (número)
- **FI**: Faltas Injustificadas (número)
- **R**: Retrasos (número)

Las columnas numéricas permiten realizar operaciones matemáticas directamente en la hoja de cálculo.

## Configuración

Puedes modificar el nombre del archivo de salida editando la variable en el script:

```python
NOMBRE_SALIDA = "faltas_consolidado.ods"
```

## Solución de problemas

### "No se encontraron archivos PDF"
- Asegúrate de que los PDFs están en el mismo directorio que el script
- Verifica que los archivos tengan extensión `.pdf`

### "No se pudo encontrar el nombre de la materia"
- Verifica que el PDF tiene el formato esperado
- Revisa que la línea de cabecera contenga "Alumno/a" y "TOTAL"

### "No se encontraron datos"
- Verifica que el PDF contiene una tabla con datos de alumnos
- Asegúrate de que cada línea de alumno tiene el formato: `Nombre + números`

### Error de instalación de pdfplumber
Si tienes problemas con "externally-managed-environment":

```bash
pip install --break-system-packages pdfplumber
```

o usa un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pdfplumber
```

## Privacidad y Seguridad

⚠️ **IMPORTANTE**: Este repositorio NO incluye PDFs de ejemplo con datos reales de estudiantes para proteger su privacidad. Los PDFs con información personal deben mantenerse privados y no compartirse públicamente.

Al usar este script:
- Mantén los PDFs originales en un lugar seguro
- No compartas los archivos generados públicamente si contienen información personal
- Cumple con las normativas de protección de datos de tu institución educativa

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Bruno Alejos García
- GitHub: [@balejosg](https://github.com/balejosg)

## Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un [issue](https://github.com/balejosg/conteo_faltas_desde_raices/issues) en GitHub.
