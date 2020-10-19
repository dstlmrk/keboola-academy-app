# Keboola Academy App

## Deployment

Via Travis CI

Docs: https://developers.keboola.com/extend/component/deployment/

## How to build

```
docker build -t keboola-app .
```

## How to run

```
docker run -it --rm \
  -v '/home/dstlmrk/projekty/dev/keboola-academy-app/src/:/code/src/' \
  -v '/home/dstlmrk/projekty/dev/keboola-academy-app/data/:/code/data/' \
  keboola-app
```
