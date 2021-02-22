
CORE := RDFprocessor/framework/
TEMPL := templateMaker
NANOTOOLS := nanotools

.PHONY: all $(CORE) $(TEMPL) $(NANOTOOLS) 
all: $(CORE) $(TEMPL) $(NANOTOOLS)

$(CORE) $(TEMPL) $(NANOTOOLS):
	$(MAKE) --directory=$@

$(TEMPL): $(CORE)
$(NANOTOOLS): $(CORE)

.PHONY: fast
fast:
	$(MAKE) --directory=$(CORE) fast
	$(MAKE) --directory=$(TEMPL)  fast
	$(MAKE) --directory=$(NANOTOOLS)  fast

.PHONY: clean
clean:
	$(MAKE) --directory=$(CORE)  clean
	$(MAKE) --directory=$(TEMPL)  clean
	$(MAKE) --directory=$(NANOTOOLS)  clean
