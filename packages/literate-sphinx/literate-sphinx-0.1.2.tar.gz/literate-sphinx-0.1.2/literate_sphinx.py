# Copyright Hubert Chathi <hubert@uhoreg.ca>
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# SPDX-License-Identifier: BSD-2-Clause

'''A literate programming extension for Sphinx'''

__version__ = '0.1.2'

from hashlib import sha256
import html
import io
import os
import posixpath
import re
from typing import Any, Iterator

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import normalized_role_options
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.errors import ExtensionError
from sphinx.util import logging
from sphinx.util.console import darkgreen  # type: ignore
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import inline_all_toctrees


logger = logging.getLogger(__name__)

class LiterateCode(SphinxDirective):
    """Parse and mark up content of a literate code chunk.

    The argument is the chunk name
    """
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        'file': directives.flag,
        'lang': directives.unchanged,
        'name': directives.unchanged,
    }
    has_content = True

    def run(self) -> list[nodes.Node]:
        options = normalized_role_options(self.options)
        language = options['lang'] if 'lang' in options else \
            self.env.temp_data.get('highlight_language', self.config.highlight_language)
        is_file = 'file' in options
        chunk_name = self.arguments[0]
        code = '\n'.join(self.content)
    
        literal_node = nodes.literal_block(code, code)
        
        literal_node['code-chunk-name'] = chunk_name
        if is_file:
            literal_node['code-chunk-is-file'] = True
        literal_node['language'] = language
        literal_node['classes'].append('literate-code') # allow special styling of literate blocks
        if 'classes' in options:
            literal_node['classes'] += options['classes']
        self.set_source_info(literal_node)
    
        container_node = nodes.container(
            '', literal_block=True,
            classes=['literal-block-wrapper', 'literate-code-wrapper']
        )
        
        if is_file:
            caption_node = nodes.caption(
                chunk_name + ':',
                '',
                nodes.literal(chunk_name, chunk_name),
                nodes.Text(':'),
            )
        else:
            caption_node = nodes.caption(chunk_name + ':', chunk_name + ':')
        
        self.set_source_info(caption_node)
        
        container_node += caption_node
        container_node += literal_node
        self.add_name(container_node)
        return [container_node]
class TangleBuilder(Builder):
    name = 'tangle'
    epilog = 'The tangled files are in %(outdir)s.'

    def get_outdated_docs(self) -> str:
        return 'all documents'
    def get_target_uri(self, docname: str, typ: str = None) -> str:
        return ''
    def assemble_doctree(self) -> nodes.document:
        master = self.config.root_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
        return tree
    def write(self, *ignored: Any) -> None:
        chunks = {} # dict of chunk name to list of chunks defined by that name
        files = [] # the list of files
    
        doctree = self.assemble_doctree()
    
        for node in doctree.findall(nodes.literal_block):
            if 'code-chunk-name' in node:
                name = node['code-chunk-name']
                chunks.setdefault(name, []).append(node)
                if 'code-chunk-is-file' in node:
                    files.append(name)
    
        # get the delimiters from the config
        (ldelim, rdelim) = self.config.literate_delimiters
        
        # get all the chunk names; initially, all chunks are unused
        unused = {name for name in chunks}
        
        for filename in files:
            with self.writer(filename, unused) as writer:
                writer.enter_expansion(filename, True)
                for chunk in chunks[filename]:
                    writer.enter_chunk(chunk)
                    for line in chunk.astext().splitlines():
                        _write_line(writer, line, chunks, '', '', ldelim, rdelim)
                    writer.exit_chunk()
                writer.exit_expansion()
        for chunk_name in unused:
            for chunk in chunks[chunk_name]:
                logger.warning(
                    '{0.source}:{0.line}: Code chunk "{1}" defined but not used'
                        .format(chunk, chunk_name)
                )
    def writer(self, filename: str, unused: set[str]) -> 'TangleWriter':
        return TangleWriter(filename, self.outdir, unused)
class TangleWriter:
    def __init__(
            self,
            filename: str,
            outdir: str,
            unused: set[str],
            filename_suffix: str = ''
    ):
        self.unused = unused
        self.path = []
    
        # some basic sanity checking for the file name
        if '..' in filename or os.path.isabs(filename):
            raise ExtensionError(
                "Chunk name is invalid file name: {}".format(filename),
                modname=__name__,
            )
        # determine the full path, and make sure the directory exists before
        # creating the file
        fullpath = os.path.join(outdir, filename)
        dirname = os.path.dirname(fullpath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
    
        self.filename = filename
    
        self.f = open(fullpath + filename_suffix, 'w')
    def close(self) -> None:
        self.f.close()
    def __enter__(self) -> 'TangleWriter':
        return self
    
    def __exit__(self, *ignored: Any) -> None:
        self.close()
    def write_line(self, line: str) -> None:
        self.f.write(line + '\n')
    
    def enter_expansion(self, chunk_name: str, is_file: bool = False) -> None:
        # update bookeeping variables
        self.unused.discard(chunk_name)
        if chunk_name in self.path:
            self.path.append(chunk_name)
            raise ExtensionError(
                'Loop found in chunks: {}'.format(' -> '.join(self.path)),
                modname = __name__,
            )
        self.path.append(chunk_name)
    
    def exit_expansion(self) -> None:
        self.path.pop()
    
    def enter_chunk(self, chunk_node: nodes.Node) -> None:
        pass
    
    def exit_chunk(self) -> None:
        pass
class AnnotatedTangleBuilder(TangleBuilder):
    name = 'annotated-tangle'

    def writer(self, filename: str, unused: set[str]) -> TangleWriter:
        return AnnotatedTangleWriter(filename, self.outdir, unused, self)

    def write(self, *opts: Any) -> None:
        self.max_depth = 1

        super().write(*opts)

        self.write_css()

    def write_css(self) -> None:
        os.makedirs(os.path.join(self.outdir, '_static'), exist_ok=True)
        with open(os.path.join(self.outdir, '_static/annotated.css'), 'w') as f:
            f.write('''
    html {
      background: white;
      color: black;
    }
    
    /* don't indent the first ul, but indent subsequent ones */
    ul {
      padding: 0;
      margin: 0;
    }
    
    ul ul {
      padding-left: 1.5rem;
      margin-left: 0;
    }
    
    li {
      border: 1px solid gray;
      margin-right: -1px;
      margin-left: -1px;
      padding-left: 0.5rem;
      list-style: none;
    }
    
    /* avoid doubling up borders for adjacent chunks */
    li + li {
      border-top: 0px none;
    }
    
    pre {
      margin: 0.5rem 0 0 0;
      padding: 0;
      background: LightGray;
    }
    
    pre .lineno {
      color: black;
      display: inline-block;
      width: 4em;
      text-align: right;
      border-right: 3px solid gray;
      padding-right: 0.5rem;
      margin-right: 0.5rem;
      background: white;
      user-select: none;
      -webkit-user-select: text;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
    }
    
    /* highlight the target */
    /* if the target is a line number */
    pre div:target {
      background: orange;
    }
    
    /* if the target is a chunk */
    li:target {
      border: 3px solid orange;
      margin-right: -3px;
      margin-left: -3px;
    }
    
    li:target > .chunkname{
      font-weight: bold;
    }
    
    li:target pre {
      background: orange;
    }
    ''')
    
            for depth in range(0, self.max_depth):
                f.write('''
    ul {}pre {{
      margin-left: {}rem;
    }}
    '''.format('ul ' * depth, 2 * (self.max_depth - depth)))

class AnnotatedTangleWriter(TangleWriter):
    def __init__(
            self,
            filename: str,
            outdir: str,
            unused: set[str],
            builder: AnnotatedTangleBuilder,
    ):
        super().__init__(filename, outdir, unused, '.html')
        self.lineno = 1
        self.node_path = []
        self.builder = builder
    def write_line(self, line: str) -> None:
        self.f.write('<div id="L{0}"><a class="lineno" href="#L{0}">{0}</a>{1}</div>'.format(self.lineno, html.escape(line)))
        self.lineno = self.lineno + 1
    def enter_chunk(self, chunk_node: nodes.Node) -> None:
        super().enter_chunk(chunk_node)
    
        self.node_path.append(chunk_node)
        hash = sha256(':'.join(['{0.source}:{0.line}'.format(c) for c in self.node_path]).encode('utf-8')).hexdigest()
    
        chunk_name = chunk_node['code-chunk-name']
        if 'code-chunk-is-file' in chunk_node:
            self.f.write('<li id="{}"><span class="chunkname"><code>{}</code></span><pre>'.format(hash, html.escape(chunk_name)))
        else:
            self.f.write('<li id="{}"><span class="chunkname">{}</span><pre>'.format(hash, html.escape(chunk_name)))
    
    def exit_chunk(self) -> None:
        self.f.write('</pre></li>')
        self.node_path.pop()
        super().exit_chunk()
    def enter_expansion(self, chunk_name: str, is_file: bool = False) -> None:
        super().enter_expansion(chunk_name, is_file)
        if len(self.path) > self.builder.max_depth:
            self.builder.max_depth = len(self.path)
    
        if is_file:
            self.f.write('<html><head><title>{}</title>'.format(html.escape(chunk_name)))
            css_file = posixpath.relpath('_static/annotated.css', posixpath.dirname(self.filename))
            css_file = html.escape(css_file)
            self.f.write('<link rel="stylesheet" type="text/css" href="{}" />'.format(css_file))
            self.f.write('</head><body><ul>')
        else:
            self.f.write('</pre><ul>')
    
    def exit_expansion(self) -> None:
        if len(self.path) == 1:
            self.f.write('</ul></body></html>')
        else:
            self.f.write('</ul><pre>')
        super().exit_expansion()

def _write_line(
        writer: TangleWriter,
        line: str,
        chunks: dict[str, Any],
        prefix: str,
        suffix: str,
        ldelim: str,
        rdelim: str,
) -> None:
    # check if the line contains the left and right delimiter
    s1 = line.split(ldelim, 1)
    if len(s1) == 2:
        s2 = s1[1].rsplit(rdelim, 1)
        if len(s2) == 2:
            # delimiters found, so get the chunk name
            chunk_name = s2[0].strip()

            # write the chunks associated with the name
            try:
                ref_chunks = chunks[chunk_name]
            except KeyError:
                raise ExtensionError(
                    'Unknown chunk name: {}'.format(chunk_name),
                    modname = __name__,
                )
            writer.enter_expansion(chunk_name)
            for ins_chunk in ref_chunks:
                writer.enter_chunk(ins_chunk)
                for ins_line in ins_chunk.astext().splitlines():
                    # recursively call this function with each line of the
                    # referenced code chunks
                    _write_line(
                        writer,
                        ins_line,
                        chunks,
                        prefix + s1[0],
                        s2[1] + suffix,
                        ldelim,
                        rdelim,
                    )
                writer.exit_chunk()
            writer.exit_expansion()

            return

    # delimiters not found, so just write the line
    writer.write_line(prefix + line + suffix)
def setup(app: Sphinx) -> dict[str, Any]:
    app.add_directive('literate-code', LiterateCode)

    app.add_builder(TangleBuilder)
    app.add_builder(AnnotatedTangleBuilder)

    app.add_config_value(
        'literate_delimiters',
        ('{{', # need to split this across two lines, or else when we tangle
        '}}'), # this file, it will think it's a code chunk reference
        'env',
        [tuple[str, str]],
    )

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
