# Install


# Development Environment Setup

```
python==3.12.7
langchain-core==0.3.21,
langchain-openai==0.2.10
langgraph==0.2.53
langgraph-checkpoint==2.0.7
langgraph-sdk==0.1.40
```

# Manual

__Error1__: 


## Problem: pip install pygraphviz failed

When run the following code in p2_langgraph_components.ipynb, I got the error. 
```python
from IPython.display import Image

Image(abot.graph.get_graph().draw_png())
```

__Error Message__: 
```bash
      pygraphviz/graphviz_wrap.c:9:9: warning: 'SWIG_PYTHON_STRICT_BYTE_CHAR' macro redefined [-Wmacro-redefined]
          9 | #define SWIG_PYTHON_STRICT_BYTE_CHAR
            |         ^
      <command line>:2:9: note: previous definition is here
          2 | #define SWIG_PYTHON_STRICT_BYTE_CHAR 1
            |         ^
      pygraphviz/graphviz_wrap.c:3023:10: fatal error: 'graphviz/cgraph.h' file not found
       3023 | #include "graphviz/cgraph.h"
            |          ^~~~~~~~~~~~~~~~~~~
      1 warning and 1 error generated.
      error: command '/usr/bin/clang' failed with exit code 1
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pygraphviz
Failed to build pygraphviz
ERROR: ERROR: Failed to build installable wheels for some pyproject.toml based projects (pygraphviz)
```

Solution:
```bash
(.venv) ➜  graphviz git:(stable) export PATH=$(brew --prefix graphviz):$PATH
(.venv) ➜  graphviz git:(stable)  export CFLAGS="-I $(brew --prefix graphviz)/include"
(.venv) ➜  graphviz git:(stable) export LDFLAGS="-L $(brew --prefix graphviz)/lib"
(.venv) ➜  graphviz git:(stable) pip install pygraphviz
Collecting pygraphviz
  Using cached pygraphviz-1.14.tar.gz (106 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Building wheels for collected packages: pygraphviz
  Building wheel for pygraphviz (pyproject.toml) ... done
```
