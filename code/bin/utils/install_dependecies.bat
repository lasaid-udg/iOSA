@echo off
pip install -r requirements.txt
echo Python dependecies installed
python install_requierments.py
echo Executing files created
pause 
start create_direct_access.vbs
echo Direct Access created
pause