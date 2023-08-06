## Development

### Install mamba

Download mamba-forge

### Manage pypi packages

- https://pypi.org/

### Create mobie-dev env

```
mamba create -y -n mobie-dev -c conda-forge openjdk=8 jgo pip
```

### Release a new version

Example for version `3.0.10`:

#### mobie-viewer-fiji repo

Use the below lines to make a maven release:

```
mamba activate mobie-dev # this activates java 8!
./install.sh 3.0.10-SNAPSHOT # test the line of code suggested by the script!
git add .; git commit -m "prepare for release"; git push
../scijava-scripts/release-version.sh --skip-version-check --skip-license-update
# if successful this will say
# * [new tag]mobie-viewer-fiji-3.0.10 -> mobie-viewer-fiji-3.0.10
```

#### mobie-cmd repo

Go to `setup.py` and change the `version` to `3.0.10`

```
git add setup.py
git commit -m "Version bump 3.0.10'
```


##### test locally

```
mamba activate mobie-dev
pip install -e .
mobie --help
export DATA="/Users/tischer/Documents/mobie/src/test/resources/input/mlj-2d-tiff"
mobie -i "${DATA}/image.tif" -s "${DATA}/segmentation.tif" -t "${DATA}/table-mlj.csv"
```

##### deploy

```
git tag 3.0.10
git push --tags
```

