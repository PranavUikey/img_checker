# AUTOGENERATED! DO NOT EDIT! File to edit: core.ipynb (unless otherwise specified).

__all__ = ['get_files', 'get_images_path', 'notebook_json']

# Cell
import json, re, os
from  pathlib import Path

# Cell
def _get_files(p, fs, extensions=None):
    p = Path(p)
    res = [p/f for f in fs if not f.startswith('.')
           and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)]
    return res

# Cell
def get_files(path, extensions=None, recurse=True, folders=None, followlinks=True):
    "Get all the files in `path` with optional `extensions`, optionally with `recurse`, only in `folders`, if specified."
    path = Path(path)
    extensions = set(extensions)
    extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path, followlinks=followlinks)):
            if folders is not None and i==0: d[:] = [o for o in d if o in folders]
            else:                         d[:] = [o for o in d if not o.startswith('.')]
            if folders is not None and i==0 and '.' not in folders: continue
            res += _get_files(p, f, extensions)
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, f, extensions)
    return res

# Cell
def get_images_path(dct):
    """Create a Function to match and return the pattern of image path"""
    all_paths = []
    for cell in dct['cells']:
        if cell['cell_type'] != 'code':
            src = cell['source']

            ### find all images with extension as .jpg or .png .
            all_matches = re.findall(r"\(.*jpg\)|\(.*png\)", src[0])

            ### Keep in mind that images and notebooks folder are on the same level of directory structure.
            for match in all_matches:
                all_paths.append(match.strip('(./))'))
    return all_paths

# Cell
def notebook_json(path):
    """Create a Function to read notebook as json and get the list of all the images used in the notebook"""
    img_paths = []
    fns = []
    path = Path(path)

    if path.is_file():
        fns.append(path)

    else:
        fns = get_files(path,extensions=['.ipynb'])

    for fn in fns:
        main_dic = json.load(open(fn,'r'))
        img_paths+=get_images_path(main_dic)

    print('Unnecessary Images in folder are as follows:-')
    print()
    for img_dir in Path('images').iterdir():
        if str(img_dir) not in img_paths:
            print(img_dir)