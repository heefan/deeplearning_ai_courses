IPython for Jupyter

```
brew install graphviz


python -m pip install \
--config-setting="--global-option=build_ext" \
--config-setting="--global-option=-I$(brew --prefix graphviz)/include/" \
--config-setting="--global-option=-L$(brew --prefix graphviz)/lib/" \
pygraphviz
```

Python Source Code

```
from PIL import Image
img = Image.open("test.png")
img.show()
```
