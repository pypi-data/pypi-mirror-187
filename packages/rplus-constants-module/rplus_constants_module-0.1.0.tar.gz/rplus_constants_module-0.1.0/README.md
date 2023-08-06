# Rplus constant module

## To install requirements to virtual environment

```shell
    make pip
```

## Activate virtualenv
```shell
  poetry env use $(which python)
```

## Install dependencies
```shell
  make install
```

## Update dependencies
```shell
  make update
```

## To build package
```shell
  make build
```

## To publish package
```shell
  make publish
```

## Register private url MNC
```shell
  poetry config repositories.mnc ${privateUrl}
```

## setting username and password for publishing
```shell
    poetry config http-basic.mnc ${username} ${password}
```