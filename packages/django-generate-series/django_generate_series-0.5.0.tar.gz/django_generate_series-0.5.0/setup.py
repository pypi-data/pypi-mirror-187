# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_generate_series']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2']

setup_kwargs = {
    'name': 'django-generate-series',
    'version': '0.5.0',
    'description': "Use Postgres' generate_series to create sequences with Django's ORM",
    'long_description': '# django-generate-series\n\nUse Postgres\' generate_series to create sequences with Django\'s ORM\n\nhttps://django-generate-series.readthedocs.io/\n\n## Goals\n\nWhen using Postgres, the set-returning functions allow us to easily create sequences of numbers, dates, datetimes, etc. Unfortunately, this functionality is not currently available within the Django ORM.\n\nThis project makes it possible to create such sequences, which can then be used with Django QuerySets. For instance, assuming you have an Order model, you can create a set of sequential dates and then annotate each with the number of orders placed on that date. This will ensure you have no date gaps in the resulting QuerySet. To get the same effect without this package, additional post-processing of the QuerySet with Python would be required.\n\n## Terminology\n\nAlthough this packages is named django-generate-series based on Postgres\' [`generate_series` set-returning function](https://www.postgresql.org/docs/current/functions-srf.html), mathematically we are creating a [sequence](https://en.wikipedia.org/wiki/Sequence) rather than a [series](https://en.wikipedia.org/wiki/Series_(mathematics)).\n\n- **sequence**: Formally, "a list of objects (or events) which have been ordered in a sequential fashion; such that each member either comes before, or after, every other member."\n\n    In django-generate-series, we can generate sequences of integers, decimals, dates, datetimes, as well as the equivalent ranges of each of these types.\n\n- **term**: The *n*th item in the sequence, where \'*n*th\' can be found using the id of the model instance.\n\n    This is the name of the field in the model which contains the term value.\n\n## API\n\nThe package includes a `generate_series` function from which you can create your own series-generating QuerySets. The field type passed into the function as `output_field` determines the resulting type of series that can be created. (Thanks, [@adamchainz](https://twitter.com/adamchainz) for the format suggestion!)\n\n### generate_series arguments\n\n- ***start*** - The value at which the sequence should begin (required)\n- ***stop*** - The value at which the sequence should end. For range types, this is the lower value of the final term (required)\n- ***step*** - How many values to step from one term to the next. For range types, this is the step from the lower value of one term to the next. (required for non-integer types)\n- ***span*** - For range types other than date and datetime, this determines the span of the lower value of a term and its upper value (optional, defaults to 1 if neeeded in the query)\n- ***output_field*** - A django model field class, one of BigIntegerField, IntegerField, DecimalField, DateField, DateTimeField, BigIntegerRangeField, IntegerRangeField, DecimalRangeField, DateRangeField, or DateTimeRangeField. (required)\n- ***include_id*** - If set to True, an auto-incrementing `id` field will be added to the QuerySet.\n- ***max_digits*** - For decimal types, specifies the maximum digits\n- ***decimal_places*** - For decimal types, specifies the number of decimal places\n- ***default_bounds*** - In Django 4.1+, allows specifying bounds for list and tuple inputs. See [Django docs](https://docs.djangoproject.com/en/dev/releases/4.1/#django-contrib-postgres)\n\n## Basic Examples\n\n```python\n# Create a bunch of sequential integers\ninteger_sequence_queryset = generate_series(\n    0, 1000, output_field=models.IntegerField,\n)\n\nfor item in integer_sequence_queryset:\n    print(item.term)\n```\n\nResult:\n\n    term\n    ----\n    0\n    1\n    2\n    3\n    4\n    5\n    6\n    7\n    8\n    9\n    10\n    ...\n    1000\n\n```python\n# Create a sequence of dates from now until a year from now\nnow = timezone.now().date()\nlater = (now + timezone.timedelta(days=365))\n\ndate_sequence_queryset = generate_series(\n    now, later, "1 days", output_field=models.DateField,\n)\n\nfor item in date_sequence_queryset:\n    print(item.term)\n```\n\nResult:\n\n    term\n    ----\n    2022-04-27\n    2022-04-28\n    2022-04-29\n    2022-04-30\n    2022-05-01\n    2022-05-02\n    2022-05-03\n    ...\n    2023-04-27\n\n*Note: See [the docs](https://django-generate-series.readthedocs.io/en/latest/usage_examples.html) and the example project in the tests directory for further examples of usage.*\n\n## Usage with partial\n\nIf you often need sequences of a given field type or with certain args, you can use [partial](https://docs.python.org/3/library/functools.html#functools.partial).\n\nExample with default `include_id` and `output_field` values:\n\n```python\nfrom functools import partial\n\nint_and_id_series = partial(generate_series, include_id=True, output_field=BigIntegerField)\n\nqs = int_and_id_series(1, 100)\n```\n',
    'author': 'Jack Linke',
    'author_email': 'jack@watervize.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jacklinke/django-generate-series/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
