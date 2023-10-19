VALIDATE 		= ${D_BASE}/tools/ildg-schema-validate.py

F_LST_VALID 	= $(wildcard ${D_REF_VALID}/*.xml)
F_LST_NONVALID	= $(wildcard ${D_REF_NONVALID}/*.xml)

.PHONY: clean veryclean

all: ${TARGET}

validate.log: ${F_SCHEMA} ${F_LST_VALID} ${F_LST_NONVALID}
		${VALIDATE} --schema ${F_SCHEMA} --valid ${F_LST_VALID} --nonvalid ${F_LST_NONVALID} 2>&1 | tee -a $@
		
clean:

veryclean: clean
	rm -f ${TARGET}