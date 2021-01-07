
CORE := RDFprocessor/framework/
ANALYSISONDATA := analysisOnData
ANALYSISONGEN := analysisOnGen

.PHONY: all $(CORE) $(ANALYSISONDATA) $(ANALYSISONGEN)
all:$(CORE) $(ANALYSISONDATA) $(ANALYSISONGEN)

$(CORE) $(ANALYSISONDATA) $(ANALYSISONGEN):
	$(MAKE) --directory=$@

$(ANALYSISONDATA): $(CORE)
$(ANALYSISONGEN): $(CORE)

.PHONY: fast
fast:
	$(MAKE) --directory=$(CORE) fast
	$(MAKE) --directory=$(ANALYSISONDATA)  fast
	$(MAKE) --directory=$(ANALYSISONGEN)  fast

.PHONY: clean
clean:
	$(MAKE) --directory=$(CORE)  clean
	$(MAKE) --directory=$(ANALYSISONDATA)  clean
	$(MAKE) --directory=$(ANALYSISONGEN)  clean
