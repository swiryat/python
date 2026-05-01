import sys
print("Python version:", sys.version)

try:
    import CacheControl
    print("CacheControl installed")
except ImportError:
    print("CacheControl NOT installed")

try:
    import Deprecated
    print("Deprecated installed")
except ImportError:
    print("Deprecated NOT installed")

try:
    import django
    print("Django installed, version:", django.get_version())
except ImportError:
    print("Django NOT installed")

try:
    import flask
    print("Flask installed, version:", flask.__version__)
except ImportError:
    print("Flask NOT installed")

try:
    import git
    print("GitPython installed")
except ImportError:
    print("GitPython NOT installed")

try:
    import jinja2
    print("Jinja2 installed")
except ImportError:
    print("Jinja2 NOT installed")

try:
    import mako
    print("Mako installed")
except ImportError:
    print("Mako NOT installed")

try:
    import markdown
    print("Markdown installed")
except ImportError:
    print("Markdown NOT installed")

try:
    import markupsafe
    print("MarkupSafe installed")
except ImportError:
    print("MarkupSafe NOT installed")

try:
    import pyaudio
    print("PyAudio installed")
except ImportError:
    print("PyAudio NOT installed")

try:
    import socks
    print("PySocks installed")
except ImportError:
    print("PySocks NOT installed")

try:
    import yaml
    print("PyYAML installed")
except ImportError:
    print("PyYAML NOT installed")

try:
    import pygments
    print("Pygments installed")
except ImportError:
    print("Pygments NOT installed")

try:
    import sqlalchemy_utils
    print("SQLAlchemy-Utils installed")
except ImportError:
    print("SQLAlchemy-Utils NOT installed")

try:
    import sqlalchemy
    print("SQLAlchemy installed")
except ImportError:
    print("SQLAlchemy NOT installed")

try:
    import send2trash
    print("Send2Trash installed")
except ImportError:
    print("Send2Trash NOT installed")
