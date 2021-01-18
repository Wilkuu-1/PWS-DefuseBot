#Anode and Cathode - remote raspberry pi control 

ANOD =./code/Anode/
ANODS=Anode_Server.py
ANODG=Anode_GUI.py
CATH =./code/Cathode/
CATHH=Cathode.py
CONN =./code/
CONNF=ANCA_Connect.py 
LIB  =/usr/lib/python3.9/
help:
	@echo "Anode-Cathode make options:(All run with sudo)"
	@echo "anode:"
	@echo "    Installs Anode to /bin/"
	@echo "    (also installs ANCA_Connect package)"
	@echo ""
	@echo "cathode:"
	@echo "    Installs Cathode to /bin/"
	@echo "    (also installs ANCA_Connect package)"
	@echo ""
	@echo "uninstall"
	@echo "    Uninstalls any of the two programs"
	@echo ""
	@echo "DO NOT DELETE THIS FOLDER OR ANY OTHER FOLDERS BESIDES ./code/test"
connect:
	cp  $(CONN)$(CONNF) $(LIB)$(CONNF)
anode: connect
	cp  $(ANOD)$(ANODS) $(LIB)$(ANODS)
	cp  $(ANOD)$(ANODG) /bin/anode
	chmod 755 $(ANOD)$(ANODG) 

cathode: connect
	cp $(CATH)$(CATHH) /bin/cathode
	chmod 755 $(CATH)$(CATHH)

uninstall: 
	rm -f /bin/cathode\
		/bin/anode\
		$(LIB)$(CONNF)\
		$(LIB)$(ANODS)
