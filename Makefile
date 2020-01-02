run:
	poetry run python matricule_checker.py

build-app:
	rm -rf dist
	rm -rf build
	rm -rf matricule_checker
	rm -f matricule_checker.zip
	rm -f matricule_checker.spec
	poetry run pyinstaller \
		--clean \
		--onefile \
		matricule_checker.py
	cp dist/matricule_checker matricule_checker
	zip matricule_checker.zip matricule_checker
