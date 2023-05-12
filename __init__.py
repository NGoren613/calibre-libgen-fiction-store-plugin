# -*- coding: utf-8 -*-
store_version = 1  # Needed for dynamic plugin loading

__license__ = "GPLv3"
__copyright__ = "diogovalentte"
__docformat__ = "restructuredtext en"

from calibre.customize import StoreBase


class LibGenStore(StoreBase):
    name = "Library Genesis Fiction"
    version = (1, 0, 3)
    description = "Searches for books on Library Genesis sites fiction section"
    author = "diogovalentte:NGoren613"
    drm_free_only = True
    actual_plugin = "calibre_plugins.store_libgen.libgen_plugin:LibGenFictionStorePlugin"
    formats = ["EPUB", "PDF"]