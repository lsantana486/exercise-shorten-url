# Ejercicio de Short URLs

## Pre requisitos
- Instalar [Podman](https://podman.io/getting-started/installation.html) ejecutor de contenedores daemonless (misma interfaz que docker)
- Instalar Poetry [link](https://python-poetry.org/docs/#installation) manejador de dependencias y entornos virtuales


## Ejecucion local
- Instalar dependencias
```shell
poetry install
```

- Ejecutar comando como CLI
```shell
poetry run short-url-cli --urls-file ./examples/urls.txt
```

## Ejecucion en contenedor
- Construir imagen
```shell
# Standard
podman build --tag short-url-cli:v$(poetry version -s) -f container/Containerfile .

# Minimal
podman build --tag short-url-cli:v$(poetry version -s) -f container/alpine.Containerfile .
```

- Ejecutar contenedor con imagen construida
```shell
podman run -it --rm -v $(pwd)/examples:/tmp short-url-cli:v$(poetry version -s) --urls-file /tmp/urls.txt
```

