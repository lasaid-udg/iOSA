import mysql.connector
import pathlib


def set_admin_user() -> None:
    host = "localhost"
    port = 3306
    user = "admin"
    db = "mydb"
    password = "admin"

    try:
        connection = mysql.connector.connect(
                            host = host, 
                            port = port, 
                            user = user, 
                            password = password, 
                            database = db
                            )

        tuple_data = (
            "admin",
            "admin",
            "Admin",
            "User",
            0
        )
        cursor = connection.cursor(buffered=True)
        
        query = "INSERT INTO mydb.system_user (username, password, first_name, last_name, type_user) VALUES ('%s', '%s', '%s', '%s', %d)" %tuple_data
        cursor.execute(query)
        connection.commit()

    except Exception as e:
        print(e)
        print("An error has ocurre.\nPlease try again...")
    

def set_direct_acces() -> None:
    direct_acces_path = pathlib.Path(__file__).parent
    write_python_excecutable_file(direct_acces_path)
    write_vbs_cmd_hidde_script(direct_acces_path)
    write_direct_access_bat_file(direct_acces_path)


def write_python_excecutable_file(path: pathlib) -> None:
    with open(str(path.parents[0]) + r"\execute.bat", 'w') as fd:
        fd.write("@echo off\n")
        fd.write("python " + '"' + str(path.parents[1]) + r"\main.py" +'"')


def write_vbs_cmd_hidde_script(path: pathlib) -> None:
    with open(str(path.parents[0]) + r"\hidden_window.vbs", 'w') as fd:
        fd.write('Set WshShell = CreateObject("WScript.Shell")\n')
        fd.write('WshShell.Run chr(34) & "' + str(path.parents[0]) + r"\execute.bat" + '" & Chr(34), 0\n')
        fd.write("Set WshShell = Nothing")


def write_direct_access_bat_file(path: pathlib) -> None:
    with open(str(path.parents[0]) + r"\utils\create_direct_access.vbs", 'w') as fd:
        fd.write('Set WshShell = CreateObject("Wscript.shell")\n')
        fd.write('Set oMyShortcut = WshShell.CreateShortcut("' + str(path.parents[0]) + r'\iOSA.lnk")' + '\n')
        fd.write('oMyShortcut.TargetPath = "' + str(path.parents[0]) + r'\hidden_window.vbs"' + '\n')
        fd.write('oMyShortcut.IconLocation = "' + str(path.parents[0]) + r'\icons\WindowLogo.ico"' + '\n')
        fd.write("oMyShortCut.Save()")



def main() -> None:
    # set_admin_user()
    set_direct_acces()

    quit()


if __name__ == "__main__":
    main()
