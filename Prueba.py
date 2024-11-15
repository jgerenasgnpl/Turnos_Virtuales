import pyodbc

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=SGNPL\fabian.gerena\MSSQLSERVER01;'
    r'DATABASE=Turno_Virtuales;'
    r'UID=usuario;'
    r'PWD=contraseña;'
)
try:
    conn = pyodbc.connect(conn_str)
    print("Conexión exitosa.")
except Exception as e:
    print("Error en la conexión:", e)
