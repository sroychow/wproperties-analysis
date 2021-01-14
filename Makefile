
CORE := RDFprocessor/framework/
TEMPL := templateMaker

.PHONY: all $(CORE) $(TEMPL) 
all:$(CORE) $(TEMPL)

$(CORE) $(TEMPL):
	$(MAKE) --directory=$@

$(TEMPL): $(CORE)

.PHONY: fast
fast:
	$(MAKE) --directory=$(CORE) fast
	$(MAKE) --directory=$(TEMPL)  fast
	

.PHONY: clean
clean:
	$(MAKE) --directory=$(CORE)  clean
	$(MAKE) --directory=$(TEMPL)  clean
