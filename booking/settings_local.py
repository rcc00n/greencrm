"""Local override shim.

Legacy deployments reference ``booking.settings_local`` as the Django settings
module.  We keep the module around and simply reuse the unified admin-only
settings so platform configs don't need to change.
"""
from .settings import *  # noqa
