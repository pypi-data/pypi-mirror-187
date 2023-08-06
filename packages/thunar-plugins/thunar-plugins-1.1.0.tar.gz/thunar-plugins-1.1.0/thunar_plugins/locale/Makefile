msgmerge_bin=msgmerge
msgfmt_bin=msgfmt
msgcat_bin=msgcat
xgettext_bin=xgettext

package_name = $(shell perl -ne 'print $$1 if m/^\s*name\s*=\s*(\S+)\s*$$/g' ../../setup.cfg)

potfile = $(package_name).pot
pofiles = $(wildcard *.po)
target_pofiles = $(subst .,/LC_MESSAGES/$(package_name).,$(pofiles))
target_mofiles = $(target_pofiles:.po=.mo)
target_mofile_dirs = $(dir $(target_mofiles))

pythonfiles = $(shell find .. -type f -iname '*.py')
gladefiles  = $(shell find .. -type f -iname '*.glade')

python_potfile = python.pot
glade_potfile = glade.pot

.PHONY: all
all: $(target_mofiles)

$(target_mofile_dirs): % :
	mkdir -p $@

xgettext_opts = --force-po --no-location --sort-output --omit-header --from-code=UTF-8

$(glade_potfile): $(gladefiles)
	$(xgettext_bin) \
		$(xgettext_opts) \
		-L Glade \
		$^ \
		-o $@ \
		&& touch $@

# create an empty catalog
$(python_potfile): $(pythonfiles)
	$(xgettext_bin) \
		-L Python \
		$(xgettext_opts) \
		$^ \
		-o $@ \
		&& touch $@

$(potfile): $(glade_potfile) $(python_potfile)
	$(msgcat_bin) --force-po -o $@ $^

# update the translated catalog
%.po: $(potfile)
	VERSION_CONTROL=off $(msgmerge_bin) \
		-U \
		--sort-output \
		--force-po \
		--backup=off \
		$@ \
		$< \
		&& touch $@

# compile the translations
%/LC_MESSAGES/$(package_name).mo: %.po  | %/LC_MESSAGES/
	$(msgfmt_bin) \
		$< \
		-o $@ \
		&& touch $@

.PHONY: clean
clean:
	rm -f $(potfile) $(mofiles)
