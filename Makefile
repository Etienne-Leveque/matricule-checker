build-app:
	rm -rf dist
	rm -rf build
	rm -rf matricule_checker
	rm -f matricule_checker.spec
	pyinstaller \
		--clean \
		--onefile \
		--icon icons/icons.svg \
		matricule_checker.py
	cp dist/matricule_checker matricule_checker
