# tools
## installation
`pip install hckmtrx_tools`

## how to use
get current directory of python file
```python
import hckmtrx_tools

reader = open(tools.FileSystem.CurrentDirectory(__file__) + "data.txt")
lines = reader.readlines()
```
```
C:
|
|___folder1
|   |   folder1_main.py
|   |   folder1_data.txt
|   |
|   |___folder2
|       |   folder2_main.py
|       |   folder2_data.txt

D:
|
|___folder3
|   |   folder3_main.py
|   |   folder3_data.txt
```
### function return in:
- folder1_main.py `C:\folder1\`
- folder2_main.py `C:\folder1\folder2\`
- folder3_main.py `D:\folder3\`