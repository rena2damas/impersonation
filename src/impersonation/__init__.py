try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # python<=3.7
from .core import impersonate

__all__ = (impersonate,)
__version__ = metadata.version("impersonation")
