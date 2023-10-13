VALIDATE = ${D_BASE}/tools/ildg-schema-validate.py

.PHONY: clean veryclean

all: ${TARGET}

validate.log: $(wildcard ${D_REF}/*.xml)
		${VALIDATE} ${F_SCHEMA} $^ 2>&1 | tee -a $@
		
clean:

veryclean: clean
	rm -f ${TARGET}