try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # python<=3.7

__version__ = metadata.version("impersonation")
