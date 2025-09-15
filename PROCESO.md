### Pre-Requisitos:
En caso de linux:
python3 -m venv venv
source venv/bin/activate

En caso de Windows:
python -m venv venv
source venv/Scripts/activate

pip install -r requirements.txt



### Proceso:

Dentro de la carpeta automatizacion-web se ejecuta el script main, el cual hace lo siguiente:

- Ejecuta Google Chrome por defecto en una ventana nueva sin perfil, esto se hace así para evitar tener que cerrar las ventanas disponibles para la ejecución

- Busca la dirección asignada en la constante URL

- Ejecuta distintos métodos y validaciones, en resumen, busca los botones que incluyan "download" en su id, esto está pensado para que sea escalable en caso de que en el futuro haya mas botones, después presiona los botones y verifica si se inició una descarga o hace falta loguearse para ingresa

- Vuelve a ejecutar y busca nuevamente los botones de descarga, para el caso 2 verifico si está en "disabled" si lo está, ejecuta todos los checks y vuelve a comprobar si cambió el estado del botón

- Una vez descargado todos los archivos los guarda en la carpeta "downloads"

- Después cargo y limpio los datos, eliminando mayúsculas, minúsculas y símbolos

- Al final se envían al endpoint definido

=======================================

- Para la ejecución de programas en local lo que hice fue desarrollar un script para ejecutar el navegador web e introducir una ecuación simple en el navegador

=======================================

- Para el apartado de n8n no llegué a realizar un esquema, pero la manera de automatizarlo propondría lo siguiente:

- Flujo de trabajo "on_click" -> al hacer click en comenzar, empezar el proceso

- El proceso empieza haciendo las descargas de los archivos correspondientes

- Sube los procesos a un flujo de n8n, este flujo intermedio es el que se encargaría de recibir y limpiar/preparar los datos para enviar a la API

- Si recibe respuesta, abrir el link correspondiente con la respuesta, descargar el archivo y enviarselo a un cliente o listado de clientes
