"""
    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole


class CiteRole(XRefRole):

    """Class for processing the :rst:role:`cite` role."""
    backend = find_plugin('pybtex.backends', 'docutils')()

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a citation reference,
        and note that the reference was cited.
        """
        keys = node['reftarget'].split(',')
        labels = [title.astext() for title in node.children]
        # Note that at this point, usually, env.bibtex_cache.bibfiles
        # is still empty because the bibliography directive may not
        # have been processed yet, so we cannot get the actual entry.
        # Instead, we simply fake an entry with the desired key, and
        # fix the label at doctree-resolved time. This happens in
        # process_citation_references.
        refnodes = [self.backend.citation_reference(
            _fake_entry(key, labels[i]),
            document,
            use_key_as_label = False
        ) for i, key in enumerate(keys)]
        for refnode in refnodes:
            refnode['classes'].append('bibtex')
        for key in keys:
            env.bibtex_cache.cited[env.docname].add(key)
        return refnodes, []


def _fake_entry(key, label):
    entry = pybtex.database.Entry(type_="")
    entry.key = key
    entry.label = label
    print(f'key: {entry.key}; label: {entry.label}')
    return entry
