## How to run?

### Install dependencies
```shell
pip3 install -r requirements.txt
```


### Init schemas
```shell
python main.py --init
```


### Start bot
```shell
python main.py
```

## Pybabel guide
> Create a new folder where the translation will be stored
```shell
mkdir locale
```

### Extract strings
> <b>PyBabel</b> automatically extracts all strings (values inside `gettext` function) from your source code

```shell
pybabel extract . -o locale/base.pot
```

### Create new translation
```shell
pybabel init -l en -i locale/base.pot -d locale
```

### Compile translations
```shell
pybabel compile -d locale
```

### Update translations
```shell
pybabel update -i locale/base.pot -d locale
```