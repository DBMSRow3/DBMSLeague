::python-3.6.1.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
FOR /F "tokens=* USEBACKQ" %%F IN (`where python.exe`) DO (
set pythondir=%%F
copy /y "%~dp0cassiopeia\type\core\common.py" "%pythondir:~0,-11%\Lib\site-packages\cassiopeia\type\core\common.py"
)
pip install cassiopeia
pip install https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-1.0.12.tar.gz