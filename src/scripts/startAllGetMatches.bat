FOR /L %%i IN (0,1,9) DO (
start "Script %%i" "retryGetMatches.bat" %%i
timeout /t 1
)