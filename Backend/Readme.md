## Configuración para el entorno de Desarrollo
1. Clona el Repositorio en tu ordenador
2. Debes crear un entorno virtual de Desarrollo para utilizar flask
    * Linux/MacOS
        ```bash
        cd Backend
        python3 -m venv .venv
        . venv/bin/activate
        ```
    * Windows:
        ```bash
        cd Backend
        py -m venv .venv
        .venv\Scripts\activate
        ```
3. Instala Flask, el siguiente comando es despues de hacer lo anterior sin importar el sistema operativo
    ```bash
    pip install Flask
    ```
4. Deberia haberte descargado unas dependencias parecidas a las del archivo "requirements.txt"
5. Para correr la aplicacion es necesario ejecutar el siguiente comando con en entorno activo
    ```bash
    flask -app main run
    ```