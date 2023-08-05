# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyckish', 'pyckish.exceptions', 'pyckish.http_elements']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'pyckish',
    'version': '0.1.0',
    'description': 'Pyckish is a micro framework to easily extract/validate/parse AWS Event when using AWS Lambdas.',
    'long_description': '# Pyckish\n### AWS Lambda Event extractor/parser/validator" \nPyckish is an "extract, parse and validate" solution to allow ease of use when dealing with AWS Lambdas. It aims\nto make using Lambdas to handle HTTP requests an alternative that works similarly to other frameworks for back-end\napplications, like FastAPI.\n\nCurrently, it can be used to extract HTTP data that comes in the event dictionary. It extracts from the dictionary,\nparses it and validates it. It relies heavily on Pydantic, and will make your life simpler if you only like to deal with validated and\ncorrectly typed data.\n\n#### Instead of doing this:\n```python\ndef lambda_handler(event: dict, context: dict) -> float:\n    auth = event[\'headers\'][\'authorization_token\']\n    store = event[\'pathParameters\'][\'store\']\n    item = event[\'body\']\n    \n    user = get_user(auth)\n    price = get_price(item, store, user)\n    return price\n```\n\n#### Do this:\n```python\nimport pyckish\nfrom pyckish.http_elements import Body, Header, PathParameter\nfrom my_models import Item\n\n@pyckish.AWSEventExtractor()\ndef lambda_handler(\n        auth: str = Header(alias=\'authorization_token\'),\n        store: str = PathParameter(default=\'my_store\'),\n        item: Item = Body()\n) -> float:\n    user = get_user(auth)\n    price = get_price(item.dict(), store, user)\n    return price\n```\n\nAnd get validation and parsing free of trouble thanks to integration with Pydantic. Enjoy the advantages of a much\nmore robust codebase, leaving behind having to extract and manage issues related to missing/wrong values.\n\n\n# Motivation\n\nToday, together with AWS API Gateway, it is possible to use only AWS Lambdas as back-end for your application.\nThe problem is, unlike modern Frameworks, like FastAPI and Starlite, using only AWS Lambdas requires you to develop\nyour own solutions for extracting, parsing, validating as well as creating error handling for the inputs of your code.\nThere are solutions that allow you to use ASGI Frameworks with AWS Lambdas, like Mangum. But it is yet another \ntechnology that sits above your bulky framework. Personally, I think that the problem could be solved in a more \nsimple and direct manner. Pyckish aims to be that solution.\n\nUsing tools like Serverless Framework with its integration with CloudFormation, many AWS Lambdas can be deployed\nfrom a single repository. Those "monorepos" solutions could also make heavy use of Pyckish in order to handle its\ninputs.\n\nRight now, Pyckish is a tiny baby, and I\'m not sure of its future. Weather it will become a full Framework with more\ncapabilities than Chalice, or it is going to remain as a simple "extractor/parser/validator" I do not know.\n\nBut I encourage you to try, simplicity and types will seduce you into it.',
    'author': 'Pedro Dardengo',
    'author_email': 'pedrodardengo@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
