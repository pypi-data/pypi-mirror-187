# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antarctic']

package_data = \
{'': ['*']}

install_requires = \
['fastparquet', 'mongoengine', 'pandas', 'pyarrow', 'setuptools']

setup_kwargs = {
    'name': 'antarctic',
    'version': '0.5.0',
    'description': '...',
    'long_description': '# Antarctic\n\n[![Release](https://github.com/tschm/antarctic/workflows/Release/badge.svg)](https://github.com/tschm/antarctic/actions/)\n[![DeepSource](https://deepsource.io/gh/tschm/antarctic.svg/?label=active+issues&show_trend=true&token=Ap44D1XBPLUb19JqC763UIWf)](https://deepsource.io/gh/tschm/antarctic/?ref=repository-badge)\n\nProject to persist Pandas data structures in a MongoDB database. \n\n## Installation\n```python\npip install antarctic\n```\n\n##  Usage\nThis project (unless the popular arctic project which I admire) is based on top of [MongoEngine](https://pypi.org/project/mongoengine/).\nMongoEngine is an ORM for MongoDB. MongoDB stores documents. We introduce a new field and extend the Document class \nto make Antarctic a convenient choice for storing Pandas (time series) data. \n\n### Fields\nWe introduce first a new field --- the PandasField.\n\n```python\nfrom mongoengine import Document, connect\nfrom antarctic.pandas_fields import PandasField\n\n# connect with your existing MongoDB (here I am using a popular interface mocking a MongoDB)\nclient = connect(db="test", host="mongomock://localhost")\n\n\n# Define the blueprint for a portfolio document\nclass Portfolio(Document):\n\tnav = PandasField()\n\tweights = PandasField()\n\tprices = PandasField()\n```\n\nThe portfolio objects works exactly the way you think it works\n\n```python\n\np = Portfolio()\np.nav = pd.Series(...)\np.prices = pd.DataFrame(...)\np.save()\n\nprint(p.nav)\nprint(p.prices)\n```\n\nBehind the scenes we convert the both Series and Frame objects into parquet bytestreams and\nstore them in a MongoDB database.\n\nThe format should also be readable by R. \n\n#### Documents\n\nIn most cases we have copies of very similar documents, e.g. we store Portfolios and Symbols rather than just a Portfolio or a Symbol.\nFor this purpose we have developed the abstract `XDocument` class relying on the Document class of MongoEngine.\nIt provides some convenient tools to simplify looping over all or a subset of Documents of the same type, e.g.\n\n```python\nfrom antarctic.document import XDocument\nfrom antarctic.pandas_fields import PandasField\n\nclient = connect(db="test", host="mongodb://localhost")\n\n\nclass Symbol(XDocument):\n\tprice = PandasField()\n```\nWe define a bunch of symbols and assign a price for each (or some of it):\n\n```python\ns1 = Symbol(name="A", price=pd.Series(...)).save()\ns2 = Symbol(name="B", price=pd.Series(...)).save()\n\n# We can access subsets like\nfor symbol in Symbol.subset(names=["B"]):\n\tprint(symbol)\n\n# often we need a dictionary of Symbols:\nSymbol.to_dict(objects=[s1, s2])\n\n# Each XDocument also provides a field for reference data:\ns1.reference["MyProp1"] = "ABC"\ns2.reference["MyProp2"] = "BCD"\n\n# You can loop over (subsets) of Symbols and extract reference and/or series data\nprint(Symbol.reference_frame(objects=[s1, s2]))\nprint(Symbol.series(series="price"))\nprint(Symbol.apply(func=lambda x: x.price.mean(), default=np.nan))\n```\n\nThe XDocument class is exposing DataFrames both for reference and time series data.\nThere is an `apply` method for using a function on (subset) of documents. \n\n\n\n### Database vs. Datastore\n\nStoring json or bytestream representations of Pandas objects is not exactly a database. Appending is rather expensive as one would have\nto extract the original Pandas object, append to it and convert the new object back into a json or bytestream representation.\nClever sharding can mitigate such effects but at the end of the day you shouldn\'t update such objects too often. Often practitioners\nuse a small database for recording (e.g. over the last 24h) and update the MongoDB database once a day. It\'s extremely fast to read the Pandas objects\nout of such a construction.\n\nOften such concepts are called DataStores.\n',
    'author': 'Thomas Schmelzer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tschm/antarctic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0',
}


setup(**setup_kwargs)
