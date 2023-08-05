# Finlay
A Testing Project for uploading at Pypi.

# So (quickly) How to Do it. 
0. Install `setuptools`, `wheel` `tqdm` and `twine` in the base environment ( not in vir env)
1. Open an account in `pypi.org`.
2. Build the package  with command `python3 setup.py sdist bdist_wheel`
3. Now upload with Twine `twine upload --repository-url https://upload.pypi.org/legacy/ dist/*`