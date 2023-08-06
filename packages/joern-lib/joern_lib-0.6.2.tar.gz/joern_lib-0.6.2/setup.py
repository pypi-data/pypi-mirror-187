# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['joern_lib', 'joern_lib.detectors']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.23.1,<0.24.0',
 'orjson>=3.8.3,<4.0.0',
 'rich>=12.6.0,<13.0.0',
 'uvloop>=0.17.0,<0.18.0',
 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'joern-lib',
    'version': '0.6.2',
    'description': 'Python library to interact with Joern server',
    'long_description': '# Introduction\n\nHigh level python library to interact with a Joern [server](https://docs.joern.io/server).\n\n```\npip install joern-lib\n```\n\nThe repository includes docker compose configuration to interactively query the joern server with polynote notebooks.\n\n![polynote interface](docs/note1.jpg)\n\n![polynote interface](docs/note2.jpg)\n\n![polynote interface](docs/note3.jpg)\n\n![polynote interface](docs/note4.jpg)\n\n## Usage\n\nRun joern server and polynote locally.\n\n```\ngit clone https://github.com/appthreat/joern-lib.git\n# Edit docker-compose.yml to set sources directory\ndocker compose up -d\n```\n\nNavigate to http://localhost:8192 for an interactive polynote notebook. You could open one of the sample notebooks from the [contrib](./contrib/polynote/notebooks/joern-notes/) directory to learn about Joern server and this library.\n\n### Common steps\n\n```\npython -m asyncio\n```\n\nExecute single query\n\n```\nfrom joern_lib import client, workspace\nfrom joern_lib.detectors import common as cpg\n\nconnection = await client.get("http://localhost:9000", "admin", "admin")\n\n# connection = await client.get("http://localhost:9000")\n\nres = await client.q(connection, "val a=1");\n\n# {\'response\': \'a: Int = 1\\n\'}\n```\n\nExecute bulk query\n\n```\nres = await client.bulk_query(connection, ["val a=1", "val b=2", "val c=a+b"]);\n# [{\'response\': \'a: Int = 1\\n\'}, {\'response\': \'b: Int = 2\\n\'}, {\'response\': \'c: Int = 3\\n\'}]\n```\n\n### Workspace\n\nList workspaces\n\n```\nres = await workspace.list(connection)\n```\n\nGet workspace path\n\n```\nres = await workspace.get_path(connection)\n# /workspace (Response would be parsed)\n```\n\nCheck if cpg exists\n\n```\nawait workspace.cpg_exists(connection, "NodeGoat")\n```\n\nImport code for analysis\n\n```\nres = await workspace.import_code(connection, "/app", "NodeGoat")\n# True\n```\n\n### CPG core\n\nList files\n\n```\nres = await cpg.list_files(connection)\n# list of files\n```\n\n### JavaScript specific\n\n```\nfrom joern_lib.detectors import js\n```\n\nList http routes\n\n```\nawait js.list_http_routes(connection)\n```\n\nName of the variable containing express()\n\n```\nawait js.get_express_appvar(connection)\n```\n\nList of require statements\n\n```\nawait js.list_requires(connection)\n```\n\nList of import statements\n\n```\nawait js.list_imports(connection)\n```\n\nList of NoSQL DB collection names\n\n```\nawait js.list_nosql_collections(connection)\n```\n\nGet HTTP sources\n\n```\nawait js.get_http_sources(connection)\nawait js.get_http_sinks(connection)\n```\n\n### AWS\n\nRequires TypeScript project\n\n```\nawait js.list_aws_modules(connection)\n```\n\n## Troubleshooting\n\n### No response from server\n\nIf Joern server stops responding after a while restart docker.\n\n```\ndocker compose down\ndocker compose up -d\n```\n',
    'author': 'Team AppThreat',
    'author_email': 'cloud@appthreat.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AppThreat/joern-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
