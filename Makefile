TARGET_DIR=$(HOME)/bin
BASE_NAME=playerctl-currently-playing

default:
	@echo 'Targets:'
	@echo '  deploy'

make-executable:
	chmod u+x $(BASE_NAME).py

deploy: make-executable
	cp $(BASE_NAME).py $(TARGET_DIR)/$(BASE_NAME)
