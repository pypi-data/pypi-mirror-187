# VR.Hercules

VR.Hercules is a configuration management system for Python projects.
Assuming your configuration to use YAML configuration files,
    you can define their structure and type by Python schema files.
That way, this project
    enables easy configuration with minimal syntax while
    providing software assistance for using configurations.

## Features

-   Python-based typed schema definition
-   Autocompletion within IDEs
-   Semi-automatic parsing of yaml files
-   Extensibility for custom types
-   Reconfiguration at runtime

## Problem Statement

Oftentimes, we build systems from configurable parts.
Ideally, the configuration would be structured like our system.
Therefore, we need a structuring configuration system.

## Approach

The de-facto standard configuration language is currently YAML.
The structure with the least syntax in Python are classes.
So, we choose YAML as configuration syntax and Python classes as parsing target.

## Mental Model

![Mental Model](https://gitlab.com/dfki/fb/ni/ol/iml/vr/vr.hercules/-/raw/main/_images/mental_model.png)

As shown on the left,
    a composed systems without a configuration management system
    might end up with different means of configuration.
As shown on the right,
    a composed system using this package
    can use a single means of configuration for all its components.
This helps
    with increasing development velocity
    because all components benefit from the features
    of the configuration management system.

## Status

[![pipeline status](https://gitlab.com/dfki/fb/ni/ol/iml/vr/vr.hercules/badges/main/pipeline.svg)](https://gitlab.com/dfki/fb/ni/ol/iml/vr/vr.hercules/-/pipelines/latest)
&nbsp;
[![coverage report](https://gitlab.com/dfki/fb/ni/ol/iml/vr/vr.hercules/badges/main/coverage.svg)](https://gitlab.com/dfki/fb/ni/ol/iml/vr/vr.hercules/-/jobs)
&nbsp;
[![PyPI Status](https://img.shields.io/pypi/status/vr_hercules)](https://pypi.org/project/vr-configuration/)
&nbsp;
[![PyPI Version](https://img.shields.io/pypi/v/vr_hercules)](https://pypi.org/project/vr-configuration/#history)
&nbsp;
[![PyPI License Badge](https://img.shields.io/pypi/l/vr_hercules)](https://pypi.org/project/vr-configuration/)
&nbsp;
[![Wheel Badge](https://img.shields.io/pypi/wheel/vr_hercules)](https://pypi.org/project/vr-configuration/#files)
&nbsp;
[![Python Versions](https://img.shields.io/pypi/pyversions/vr_hercules)](https://pypi.org/project/vr-configuration/)

## License

This package is not licensed. Therefore, it can only be used in the DFKI.

## Usage

This package originates from and is being used in production
    at the [VR.Backend](https://git.ni.dfki.de/iml/vr/image/vr.backend) project.
However,
    the VR.Backend project is currently internal to the DFKI.

## Demo

This package enables parsing configuration files according to a schema:

```python
class Config:
    greeting: str
    greetee: str


Config: type = parse_config(
    config_file_path='config.yaml',
)
```

## Tutorial

For more detailed instructions on using this project,
  see the [tutorial](README_BASIC.md).

## Development

For development and maintenance of this project,
  see the [development documentation](README_DEVELOPERS.md).

## Documentation

For more complete documentation,
    see our [dedicated documentation pages](https://dfki.gitlab.io/fb/ni/ol/iml/vr/vr.hercules/).

## Support

Please refer to the issue tracker for any inquiry.

## Name

VR.Hercules is simpler than [Facebook's Hydra][Facebook's-Hydra] and it *slays*.

[Facebook's-Hydra]: https://github.com/facebookresearch/hydra
