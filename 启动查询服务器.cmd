 
set VENV_PATH=.\DistributeServer\NGA_AutoSave_V3_DistributeServer\NGA_AutoSave_V3_DistributeServer\env1\Scripts  
call "%VENV_PATH%\activate.bat"  
cd .\DistributeServer\NGA_AutoSave_V3_DistributeServer\NGA_AutoSave_V3_DistributeServer
python manage.py runserver 8080
pause