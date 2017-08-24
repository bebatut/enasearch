try:
    from enasearch import cli
except ImportError:
    from . import cli

cli.cli()
