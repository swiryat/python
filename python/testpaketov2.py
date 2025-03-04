packages = [
    "CacheControl", "Deprecated", "Django", "Flask", "GitPython", "Jinja2", "Mako",
    "Markdown", "MarkupSafe", "PyAudio", "PyPDF2", "PySocks", "PyYAML", "Pygments",
    "SQLAlchemy-Utils", "SQLAlchemy", "Send2Trash", "SimpleCV", "Werkzeug", "absl-py",
    "aiohappyeyeballs", "aiohttp", "aiosignal", "albucore", "albumentations", "alembic",
    "altair", "aniso8601", "annotated-types", "anyio", "argon2-cffi-bindings", "argon2-cffi",
    "arrow", "asgiref", "asttokens", "astunparse", "async-lru", "attrs", "babel", "beautifulsoup4",
    "bleach", "blinker", "blis", "boolean.py", "cachetools", "catalogue", "certifi", "cffi", "chardet",
    "charset-normalizer", "click", "cloudpathlib", "cloudpickle", "colorama", "comm", "comtypes", "confection",
    "contourpy", "cryptography", "cycler", "cyclonedx-python-lib", "cymem", "databricks-sdk", "datasets", "debugpy",
    "decorator", "defusedxml", "dill", "distlib", "distro", "djangorestframework", "docker", "docx", "dparse", "et_xmlfile",
    "eval_type_backport", "executing", "fastai", "fastapi", "fastcore", "fastdownload", "fastjsonschema", "fastprogress",
    "filelock", "flatbuffers", "fonttools", "fqdn", "frozenlist", "fsspec", "gTTS", "gast", "gitdb", "google-auth",
    "google-pasta", "graphene", "graphql-core", "graphql-relay", "graphviz", "greenlet", "grpcio", "h11", "h5py",
    "html5lib", "httpcore", "httpx", "huggingface-hub", "idna", "imageio-ffmpeg", "imageio", "importlib_metadata",
    "ipykernel", "ipython", "ipywidgets", "isoduration", "itsdangerous", "jedi", "jiter", "joblib", "json5",
    "jsonpickle", "jsonpointer", "jsonschema-specifications", "jsonschema", "jupyter-console", "jupyter-events",
    "jupyter-lsp", "jupyter", "jupyter_client", "jupyter_core", "jupyter_server", "jupyter_server_terminals",
    "jupyterlab", "jupyterlab_pygments", "jupyterlab_server", "jupyterlab_widgets", "keras", "kiwisolver", "langcodes",
    "language_data", "lazy_loader", "libclang", "license-expression", "lief", "lightgbm", "lxml", "marisa-trie",
    "markdown-it-py", "marshmallow", "matplotlib-inline", "matplotlib", "mdurl", "mistune", "ml-dtypes", "mlflow-skinny",
    "mlflow", "more-itertools", "moviepy", "mpmath", "msgpack", "multidict", "multiprocess", "murmurhash", "music21",
    "namex", "narwhals", "nbclient", "nbconvert", "nbformat", "nest-asyncio", "networkx", "nltk", "noisereduce", "notebook",
    "notebook_shim", "numpy", "openai", "opencv-python-headless", "opencv-python", "openpyxl", "opentelemetry-api",
    "opentelemetry-sdk", "opentelemetry-semantic-conventions", "opt_einsum", "optree", "outcome", "overrides", "packageurl-python",
    "packaging", "pandas", "pandocfilters", "parso", "patsy", "pdf2image", "pillow", "pip-api", "pip-autoremove",
    "pip-requirements-parser", "pip", "pip_audit", "pipdeptree", "pipenv", "platformdirs", "playsound", "plotly",
    "preshed", "proglog", "prometheus_client", "prompt-toolkit"
]

for package in packages:
    try:
        __import__(package)
        print(f"{package} installed")
    except ImportError:
        print(f"{package} NOT installed")
