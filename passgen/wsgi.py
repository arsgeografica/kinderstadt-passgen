import os
from passgen.app import factory


if 'PASSGEN_CONFIG_MODULE' not in os.environ:
    raise RuntimeError('No PASSGEN_CONFIG_MODULE environment set.')

application = factory(os.environ['PASSGEN_CONFIG_MODULE'])
