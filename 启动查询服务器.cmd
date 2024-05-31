::@echo off
::在此修改服务器IP:Port以自动启动页面
set base_url=127.0.0.1
set base_port=8080
set full_url=http://%base_url%:%base_port%/mainApp/dbGetAll
start %full_url%
:: 启动服务器
set VENV_PATH=.\DistributeServer\NGA_AutoSave_V3_DistributeServer\NGA_AutoSave_V3_DistributeServer\env1\Scripts  
call "%VENV_PATH%\activate.bat"  
cd .\DistributeServer\NGA_AutoSave_V3_DistributeServer\NGA_AutoSave_V3_DistributeServer
python manage.py runserver %base_port%
pause