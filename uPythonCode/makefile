PORT = COM3
AMPY = ampy
AMPY_ARGS = -p $(PORT)

SRC := $(wildcard *.py)

blank :=
define newline

$(blank)
endef

upload-and-display: $(SRC)
	make upload
	make open-prompt

open-prompt:
	- PuTTY.exe -serial COM3 -sercfg 115200,8,n,1,N

# Upload all python files in the directory
upload: $(SRC)
	$(foreach file, $(SRC), $(AMPY) $(AMPY_ARGS) put $(file) $(newline))

clean:
	$(foreach file, $(SRC), $(AMPY) $(AMPY_ARGS) rm $(file) $(newline))

reset:
	$(AMPY) $(AMPY_ARGS) reset




