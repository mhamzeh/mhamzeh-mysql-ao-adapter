PYTHON = python
PIP = pip

# lambda function name - may need to change for each project.
LAMBDA_FUNCTION_NAME = lambda_function_name

# lambda zip file - will be overridden by build process.
LAMBDA_ZIP = lambda.zip

PYTHON_PATH=$(shell which python)
PYTHON_LIB_PATH=$(shell python -c "import os, inspect; print os.path.dirname(inspect.getfile(inspect))")

.PHONY: jail
jail: ## make chroot jail
	@echo "Make jail"
	wget http://olivier.sessink.nl/jailkit/jailkit-2.19.tar.gz
	tar -xzvf jailkit-2.19.tar.gz
	cd jailkit-2.19;./configure && make && make install
	mkdir $(JAIL_DIR)
	jk_init -j $(JAIL_DIR) jk_lsh
	jk_cp -j $(JAIL_DIR) $(PYTHON_PATH)
	jk_cp -j $(JAIL_DIR) $(PYTHON_LIB_PATH)
	addgroup -S $(JAIL_GROUPNAME)
	adduser -S $(JAIL_USERNAME) -G $(JAIL_GROUPNAME)
	jk_jailuser -n -j $(JAIL_DIR) $(JAIL_USERNAME)

.PHONY: create-certs
create-certs:
	@echo "Creating Selfsigned certs"
	mkdir -p secrets/ssl/cert
	/usr/bin/openssl req -x509 -newkey rsa:2048 -nodes -keyout secrets/ssl/cert/private_key.pem -out secrets/ssl/cert/certificate.pem -days 365 -subj "/C=US/ST=Texas/L=Austin/O=Cisco/OU=longhorn/CN=python"

.PHONY: all
all: linux mocks test

.PHONY: linux
linux:
	@echo "building function worker (linux)"
	$(PYTHON) --version
	$(PYTHON) setup.py bdist_wheel

.PHONY: test
test: ## run unit tests
	@echo "Running Unit Tests"
	flake8
	scripts/run_tests.sh

.PHONY: mocks
mocks: ## run mocks
	@echo "Generating Mocks"
	@echo "No mocks to run"

.PHONY: staticanalysis
staticanalysis:
	@echo "Running Static Analysis"
	flake8
	pylint activities_python functions/$(LAMBDA_FUNCTION_NAME)/* $(PYLINT_ARGS)

.PHONY: lambda
lambda:
	@echo "Building Lambda distribution $(LAMBDA_ZIP)..."
	mkdir -p build
	cp -R functions/ build/
	cp -R activities_python build/$(LAMBDA_FUNCTION_NAME)

	# workaround for Mac/Homebrew pip issue - create setup.cfg...
	@echo "[install]" > build/$(LAMBDA_FUNCTION_NAME)/setup.cfg
	@echo "prefix=" >> build/$(LAMBDA_FUNCTION_NAME)/setup.cfg

	pushd build/$(LAMBDA_FUNCTION_NAME) && $(PIP) install -r ../../requires.txt -t .

	# delete workaround file
	$(RM) build/$(LAMBDA_FUNCTION_NAME)/setup.cfg

	# create lambda zip
	pushd build/$(LAMBDA_FUNCTION_NAME) && zip -r ../$(LAMBDA_ZIP) .


.PHONY: clean
clean:
	$(PYTHON) setup.py clean
	$(RM) -r build
	$(RM) -r dist
