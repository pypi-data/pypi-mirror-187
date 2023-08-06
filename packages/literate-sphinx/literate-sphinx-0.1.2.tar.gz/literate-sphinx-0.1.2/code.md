# Code

Here is the implementation of the extension.

## `literate-code` directive

First, we define the `literate-code` directive:

```{literate-code} classes
class LiterateCode(SphinxDirective):
    """Parse and mark up content of a literate code chunk.

    The argument is the chunk name
    """
    {{LiterateCode variables}}

    {{LiterateCode methods}}
```

The directive takes one argument, which is required, and may contain
whitespace.

```{literate-code} LiterateCode variables
required_arguments = 1
final_argument_whitespace = True
```

The options are as defined above.  The `directives.*` values below specify how
the option values are validated.

```{literate-code} LiterateCode variables
option_spec = {
    'class': directives.class_option,
    'file': directives.flag,
    'lang': directives.unchanged,
    'name': directives.unchanged,
}
```

Obviously, code chunks need to have content.

```{literate-code} LiterateCode variables
has_content = True
```

Directives need one method: a `run` method that outputs a list of docutils
nodes to insert into the document.  Our `run` method will have three phases:
options processing, creating the `literal_block` to contain the code, and
creating a `container` node around the `literal_block` to add a caption.

```{literate-code} LiterateCode methods
def run(self) -> list[nodes.Node]:
    {{process literate-code options}}

    {{create literal_block}}

    {{create container node}}
```

First, we do some standard options processing from docutils.
(`normalized_role_options` is imported from `docutils.parsers.rst.roles`).

```{literate-code} process literate-code options
options = normalized_role_options(self.options)
```

Next, we determine the language used for syntax highlighting.  If a `:lang:`
option is given, we will use that value.  Otherwise, we use the
`highlight_language` config option.

```{literate-code} process literate-code options
language = options['lang'] if 'lang' in options else \
    self.env.temp_data.get('highlight_language', self.config.highlight_language)
```

If the `file` option is given, then the chunk represents a file.

```{literate-code} process literate-code options
is_file = 'file' in options
```

The chunk name is the arguments given to the directive.

```{literate-code} process literate-code options
chunk_name = self.arguments[0]
```

The code is the contents given to the directive.  The contents are given as a
list of lines, so we join them together with `\n`.

```{literate-code} process literate-code options
code = '\n'.join(self.content)
```

The code will be displayed in a `literal_block` (a mono-spaced block), and we
will add some attributes to store the options that were given.  The
`code-chunk-name` and `code-chunk-is-file` attributes will be used for
tangling.  The `language` attribute is used for syntax highlighting, and the
`classes` attribute is used for rendering the document.

```{literate-code} create literal_block
literal_node = nodes.literal_block(code, code)

literal_node['code-chunk-name'] = chunk_name
if is_file:
    literal_node['code-chunk-is-file'] = True
literal_node['language'] = language
literal_node['classes'].append('literate-code') # allow special styling of literate blocks
if 'classes' in options:
    literal_node['classes'] += options['classes']
```

We also call `set_source_info` from the parent class to set the source file and
line number for the node.

```{literate-code} create literal_block
self.set_source_info(literal_node)
```

The `literal_block` will be placed in a `container` node, along with a
`caption`.  We will use the code chunk name, followed by a `:`, as the caption,
so that readers can see the name.  If the code chunk is a file, we make the
caption monospaced.  The following code is based on the source code of
`sphinx.directives.code.container_wrapper`.

```{literate-code} create container node
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
```

We will add the name given in the `name` option (if any) to the container node,
so that references will link there.

```{literate-code} create container node
self.add_name(container_node)
```

And finally, we return a list containing the container node, since that is the
node to be added to the document.

```{literate-code} create container node
return [container_node]
```

## `tangle` builder

We now create a Sphinx `Builder` to "tangle" the document, that is, extract the
code chunks and produce the computer-readable source files.

```{literate-code} classes
class TangleBuilder(Builder):
    {{TangleBuilder variables}}

    {{TangleBuilder methods}}
```

We give our builder the name `tangle`, so the tangling can be done by running
`make tangle`, or using `sphinx-build -b tangle ...`.

```{literate-code} TangleBuilder variables
name = 'tangle'
```

When the builder completes, we will tell the user where the tangled files can
be found.

```{literate-code} TangleBuilder variables
epilog = 'The tangled files are in %(outdir)s.'
```

Builders need to implement several methods, some of which do not really apply
to us.

Since the output files don't correspond to input files, we tell Sphinx to read
all the inputs.

```{literate-code} TangleBuilder methods
def get_outdated_docs(self) -> str:
    return 'all documents'
```

We don't need to worry about generating URIs for our documents, since we will
not be creating references, so we just return an empty string.

```{literate-code} TangleBuilder methods
def get_target_uri(self, docname: str, typ: str = None) -> str:
    return ''
```

Now, we need a method that will give us the entire document as a single tree.
This function is taken from `sphinx.builders.singlehtml.SingleFileHTMLBuilder`.

```{literate-code} TangleBuilder methods
def assemble_doctree(self) -> nodes.document:
    master = self.config.root_doc
    tree = self.env.get_doctree(master)
    tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
    return tree
```

With this, we define the method that will write the source files.  This method
would normally be called with several arguments, but they are irrelevant to us,
so we will ignore them.  First, we will walk the document tree, looking for all
the code chunks.  We will record the chunks with their names, and if they
represent files, record their names in a list.  After all the chunks are
recorded, we will go through the list of files and write the files, expanding
the code chunk references as necessary.

```{literate-code} TangleBuilder methods
def write(self, *ignored: Any) -> None:
    chunks = {} # dict of chunk name to list of chunks defined by that name
    files = [] # the list of files

    doctree = self.assemble_doctree()

    {{find code chunks in document}}

    {{write files}}
```

To look for code chunks, we walk the document tree, and find any
`literal_block` nodes that have a `code-chunk-name` attribute.  If the node
also has a `code-chunk-is-file` attribute, then we record the chunk name in the
`files` list.

```{literate-code} find code chunks in document
for node in doctree.findall(nodes.literal_block):
    if 'code-chunk-name' in node:
        name = node['code-chunk-name']
        chunks.setdefault(name, []).append(node)
        if 'code-chunk-is-file' in node:
            files.append(name)
```

Before we write the part of the function that will write out the files, we need
two extra pieces.  The first is a class that we will use for abstracting out
the writing of a file.  We will create a base version here, and extend the
class when for the [annotated tangler](#annotated-tangling).  This will allow
us to reuse much of our tangling code.  This class has methods to write out a
line of code, to let it know when we are about to expand a code chunk reference
and when we're done expanding it, and to let it know when we're about to start
processing a new code chunk and when we're done processing it.

The second thing that we will need is a function that will process a single
line from a code chunk and write it out to a file, using our writer class.  If
the line contains a reference to another code chunk, the function will expand
the reference, otherwise it will write the line with any necessary prefix or
suffix.  We will first define our writer function, and then we will define our
writer class.

The function will be passed the writer object, the line to write, the
dictionary of chunks, the prefix and suffix to add to the line, and the left
and right delimiters used to enclose code chunk references.

```{literate-code} functions
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
```

Now we define our writer class.  In addition to writing files, we will also use
our writer class to handle some bookkeeping.  This bookkeeping could be done in
our writer function, which may be better in terms of making our class only
responsible for one thing, but putting it in the class avoids needing to pass
more parameters into the writer function.

The first bookkeeping task that we will do is keeping track of what chunk names
have been used.  Or rather, what chunk names have been unused up to now.  At
the beginning of the tangling process, the builder creates a `set` called
`unused`, which is set of all the chunk names, and when we use a chunk, we will
remove it from the set.  This will allow us to report on chunks that have been
defined, but not used.

The second bookkeeping task is to check for loops in chunk references.  We do
this by creating a `list` called `path`, which gives the path of chunk names,
from the root file, to the current chunk that is being processed.  When we
process a chunk, we first check if the chunk name is already on the path, and
if so, a loop has been detected.  Otherwise, we push the chunk name onto `path`
before processing the referenced chunk.  After we have processed the chunk, we
will pop the chunk name from the list.

Our class constructor will be passed the file name as given in the document,
the output directory, the `unused` set created by the builder, and a suffix to
add to the file name.  For normal tangling, this will be empty, but it will be
used with the annotated tangling defined later on.  The constructor will do
some basic sanity checking on the file name, to ensure that it won't overwrite
files outside of the output directory, and then create the file to be written.

```{literate-code} classes
class TangleWriter:
    {{TangleWriter methods}}
```

```{literate-code} TangleWriter methods
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
```

We need to close the file once we are done, so we define a method to do that.

```{literate-code} TangleWriter methods
def close(self) -> None:
    self.f.close()
```

And we create the `__enter__` and `__exit__` methods needed to use our class
with the `with` statement.

```{literate-code} TangleWriter methods
def __enter__(self) -> 'TangleWriter':
    return self

def __exit__(self, *ignored: Any) -> None:
    self.close()
```

The rest of the class is fairly straightforward.  As mentioned above, we need
methods to write out a line of code (here, we simply write the line to the
file, along with a newline ), to let it know when we are about to expand a code
chunk reference and when we're done expanding it (here, we just need to perform
our bookkeeping tasks), and to let it know when we're about to start processing
a new code chunk and when we're done processing it (here, we don't need to do
anything).

```{literate-code} TangleWriter methods
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
```

We add a method to our builder that returns an instance of our writer class.
For other types of tangling, we can override this method to return a different
type of writer.

```{literate-code} TangleBuilder methods
def writer(self, filename: str, unused: set[str]) -> 'TangleWriter':
    return TangleWriter(filename, self.outdir, unused)
```

We can now finish off our `write` function.  For each output file, we create
the file, look up the code chunks for the file, get the contents of each chunk,
split into lines, and use our function above to write the lines.

```{literate-code} write files
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
```

After we've written all the files, we emit a warning for every unused chunk,
giving the file name and line where the chunk is defined.

```{literate-code} write files
for chunk_name in unused:
    for chunk in chunks[chunk_name]:
        logger.warning(
            '{0.source}:{0.line}: Code chunk "{1}" defined but not used'
                .format(chunk, chunk_name)
        )
```

## Annotated tangling

In literate programming, the document is intended to be viewed by people, and
the tangled source code is meant mainly for computers.  However, some times
people need or want to look at the tangled code.  If a program emits an error,
it may include a line number indicating where the error occurred; to debug, a
person would need to look at the code and determine how to fix it.  Some times,
a person may simply want to see how a code chunk fits in the context of other
chunks.

For this, we create a modified tangle builder that will create a tangled
source, annotated with the chunks that the code comes from.  To see this in
action, you can view the <a href="_annotated/literate_sphinx.py.html">annotated
tangling of this document</a>.

We will create a builder and a writer, based off of the basic tangle builder
and writer.  We need to change the name of the builder, make it use our
modified writer, and write out a CSS file.  We will discuss the details of
writing out the CSS file later on, but for now, we note that we will need to
know the maximum depth of the chunks.  We will keep track of this in our
writer, so we will pass a our writer a reference to `self` so that it can
update the maximum depth.

```{literate-code} classes
class AnnotatedTangleBuilder(TangleBuilder):
    name = 'annotated-tangle'

    def writer(self, filename: str, unused: set[str]) -> TangleWriter:
        return AnnotatedTangleWriter(filename, self.outdir, unused, self)

    def write(self, *opts: Any) -> None:
        self.max_depth = 1

        super().write(*opts)

        self.write_css()

    {{AnnotatedTangleBuilder methods}}

class AnnotatedTangleWriter(TangleWriter):
    {{AnnotatedTangleWriter methods}}
```

We will write the files as HTML, so our constructor will call the parent
constructor, giving it a `.html` suffix.  We will add line numbers to our
output, so we initialize our line number counter.  We will also keep track of
the nodes on the path from the root of the file to our current chunk; this will
be used to generate a unique ID for each path, which we will explain below.

```{literate-code} AnnotatedTangleWriter methods
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
```

Writing out a line is fairly straghtforward.  We will output a `<div>` with an
`id` indicating the line number, allowing users to reference individual lines.
Inside the `<div>`, we will write the line number (making it a link to that
line, and with an appropriate class so that it can be styled separately from
the code), and the line of code itself.  Once we're done writing
the line, we increment the line number.

```{literate-code} AnnotatedTangleWriter methods
def write_line(self, line: str) -> None:
    self.f.write('<div id="L{0}"><a class="lineno" href="#L{0}">{0}</a>{1}</div>'.format(self.lineno, html.escape(line)))
    self.lineno = self.lineno + 1
```

Now we need to consider how our HTML file will be structured.  For each chunk
name that we expand, we will create a `<ul>`.  Each chunk associated with that
name will get a `<li>` that contains the chunk name and a `<pre>` that will
contain the code.

We will start from the inside out.  We've already written the function for
writing the code lines.  Now we write the functions for entering and exiting
the code chunks.

We want to assign each chunk a unique ID so that it can be referenced.  One
possibility would be use the source file and line that it came from.  However,
each chunk can be used multiple times, so this may not be unique.  A better way
is to track the full path from the root to the current node, and create an ID
base on that.  We will use a SHA256 hash of the source files and lines for the
nodes.

When we enter the node, then, we create our `<li>` element with the generated
ID, create a `<span>` to put the chunk name in (which we will make monospace if
the chunk name is a file name), and then open a `<pre>` element so that we can
write the code.  When we exit the chunk, we close the `<pre>` and the `<li>`.

We also ensure that we call the super-class implementations of the functions.
They currently don't do anything, but we will do that in case they do something
in the future.

```{literate-code} AnnotatedTangleWriter methods
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
```

Now we write the methods that are called when we are ready to expand a code
chunk name, and when we are done expanding.  There are two cases that we will
handle.  The first case is when we are dealing with the top-level file chunks.
In this case, we simply write an appropriate HTML header, open the `<body>`
tag, and open a `<ul>` tag before we expand the chunks, and we close the `<ul>`
and the `<body>` after we are done expanding the chunks.

If we are not dealing with the top-level file chunks, then `enter_expansion`
will be called when there is a `<pre>` element open, since we're waiting to
write a line of code.  So we must close the `<pre>` before opening the `<ul>`
element.  Conversely, after expanding, we close the `<ul>` that we opened, and
open a new `<pre>` so that we are ready again to write code lines.

This may produce empty `<pre></pre>` elements, but they don't cause a problem.

```{literate-code} AnnotatedTangleWriter methods
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
```

### Writing CSS

To write the CSS, we first start with a base style to set up the basic
structure.  Then, we add indentation to the `<pre>` elements.  We want the code
lines to be aligned vertically, so code from chunks that are more nested should
be less indented than code from chunks that are less nested.  Each `<ul>` is
indented 2rem in from the previous `<ul>`, so we will indent code chunks by
2rem less for each level that it is indented.  So we create CSS rules that
match on `ul ...(times the number of levels) pre`, and set the left margin to 2
times (the maximum depth minus the number of levels).  And the number of such
rules that we need to make is equal to the maximum depth.

```{literate-code} AnnotatedTangleBuilder methods
def write_css(self) -> None:
    os.makedirs(os.path.join(self.outdir, '_static'), exist_ok=True)
    with open(os.path.join(self.outdir, '_static/annotated.css'), 'w') as f:
        f.write('''
{{base annotations css}}
''')

        for depth in range(0, self.max_depth):
            f.write('''
ul {}pre {{
  margin-left: {}rem;
}}
'''.format('ul ' * depth, 2 * (self.max_depth - depth)))
```

```{literate-code} base annotations css
:lang: css

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
```

## Wrapping up

Now we need to tell Sphinx about our new directive, our builders, and our
configuration option, as well as some information about the extension.

```{literate-code} functions
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
```

And we put it all together in a Python file.

```{literate-code} literate_sphinx.py
:file:

# {{copyright license}}

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

{{classes}}

{{functions}}
```

## Future plans

- link code chunks together
  - link to where code chunks are used
  - link to code chunk definitions
  - link to continued/previous definitions
- link between doc and annotated tangle
- syntax highlight annotated tangle
- make style for annotated tangle configurable
- format code chunk references better (e.g. avoid syntax highlighting)
- allow multiple single-line chunks on a line
- add file names/line numbers in tangled files (when possible, for supported
  languages)

