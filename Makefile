help:
	@echo '    setup ................... sets up project'
	@echo '    test .................... runs tests'
	@echo '    clean ................... cleans project'
	
setup:
	pip install -r requirements.local.txt
	pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@nosetests tests/
