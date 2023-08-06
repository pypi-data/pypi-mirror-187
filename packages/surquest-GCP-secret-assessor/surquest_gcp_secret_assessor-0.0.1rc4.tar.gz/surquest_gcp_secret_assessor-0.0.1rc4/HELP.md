# Local development

Build docker image

```
docker build `
     --tag python/secret-manager/dev `
     --file package.base.dockerfile `
     --target base .
```

```
docker build `
     --tag python/secret-accessor/test `
     --file package.base.dockerfile `
     --target test .
```

```
docker run --rm -it `
 -v "${PWD}:/opt/project" `
 python/secret-accessor/test `
 pytest
```

```
docker run --rm -it `
 python 
```

```
python3 -m build
python3 -m twine upload --repository pypi dist/* 
```