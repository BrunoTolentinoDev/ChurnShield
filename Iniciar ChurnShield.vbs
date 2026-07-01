' Duplo clique aqui para abrir o ChurnShield (janela fica aberta mesmo se der erro)
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = folder
shell.Run "cmd /k """ & folder & "\rodar.bat""", 1, False
