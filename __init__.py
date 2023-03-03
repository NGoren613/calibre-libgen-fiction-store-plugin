# -*- coding: utf-8 -*-
store_version = 1  # Needed for dynamic plugin loading

__license__ = "GPLv3"
__copyright__ = "diogovalentte"
__docformat__ = "restructuredtext en"

from calibre.customize import StoreBase


class LibGenStore(StoreBase):
    name = "Library Genesis"
    version = (1, 0, 0)
    description = "Searches for books on Library Genesis sites"
    author = "diogovalentte"
    drm_free_only = True
    actual_plugin = "calibre_plugins.store_libgen.libgen_plugin:LibGenStorePlugin"
    formats = ["EPUB", "PDF"]
