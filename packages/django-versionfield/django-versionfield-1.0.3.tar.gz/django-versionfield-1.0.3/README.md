# django-versionfield

[![PyPI version](https://badge.fury.io/py/django-versionfield.svg)](https://badge.fury.io/py/django-versionfield)
[![PyPi downloads](https://pypip.in/d/django-versionfield/badge.png)](https://crate.io/packages/django-versionfield/)

## Installation
   * Install `django-versionfield`
```shell script
	pip install django-versionfield
```
   * Add to `INSTALLED_APPS`
```python
    INSTALLED_APPS = [ 
    ...
    'versionfield',
    ...    
    ]   
```
    
## Usage:
```python
    from versionfield import VersionField

    class SomeModel(models.Model):
        version = VersionField()
```

## Sample Queries:
```python
    SomeModel.objects.filter(version__gt="1.0.0")
    SomeModel.objects.filter(version__gt="1.0")
```

## Widget
```python
    from versionfield.widgets import VersionWidget
    
    class SomeForm(ModelForm):
        some_field = VersionField(widget = VersionWidget)

```
