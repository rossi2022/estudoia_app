@echo off
echo =========================================
echo EstudoIA App - Limpando instalador antigo
echo =========================================
timeout /t 1 > nul

REM Apagar a pasta electron
if exist electron (
    rmdir /s /q electron
    echo Pasta electron/ deletada.
) else (
    echo Pasta electron/ nao encontrada.
)

REM Apagar a pasta dist
if exist dist (
    rmdir /s /q dist
    echo Pasta dist/ deletada.
) else (
    echo Pasta dist/ nao encontrada.
)

REM Apagar o start_tudo.bat (opcional)
if exist start_tudo.bat (
    del start_tudo.bat
    echo Arquivo start_tudo.bat deletado.
) else (
    echo Arquivo start_tudo.bat nao encontrado.
)

echo =========================================
echo Limpeza concluida!
echo =========================================
pause
