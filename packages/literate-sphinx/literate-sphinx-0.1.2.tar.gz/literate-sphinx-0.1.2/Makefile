# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

src:
	@$(SPHINXBUILD) -M tangle "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp _build/tangle/literate_sphinx.py .

public:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" public $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -b annotated-tangle "$(SOURCEDIR)" public/_annotated $(SPHINXOPTS) $(O)

.PHONY: help Makefile src public

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
