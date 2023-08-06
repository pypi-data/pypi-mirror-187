Checklist to update version:
 1) edit code
 2) edit setup.py (increase version number)
 3) cd to same level as setup.py
 4) python -m build
 5) twine upload dist/* --skip-existing
