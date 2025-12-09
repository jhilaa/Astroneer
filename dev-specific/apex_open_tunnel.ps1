# Démarre FastAPI + ngrok, récupère l’URL HTTPS et l’envoie à APEX

# Charger les variables du fichier .env
Get-Content ".env" | ForEach-Object {
	if ($_ -match "^(.*?)=(.*)$") {
		Set-Item -Path "env:$($matches[1])" -Value $matches[2]
	}
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 1. Démarrer le serveur Python en arrière-plan
Start-Process -FilePath "uvicorn" `
  -ArgumentList "server:app --host 0.0.0.0 --port $env:APP_PORT" `
  -WorkingDirectory $scriptDir `
  -NoNewWindow
Write-Host "➡️ Serveur Python lancé sur le port $env:APP_PORT"

# 2. Lancer ngrok en arrière-plan
Start-Process -FilePath "ngrok" -ArgumentList "http $env:APP_PORT" -NoNewWindow
Start-Sleep -Seconds 5  # attendre que ngrok démarre

# 3. Récupérer l’URL publique HTTPS de ngrok
$response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels"
$ngrokUrl = ($response.tunnels | Where-Object { $_.proto -eq "https" }).public_url

Write-Host "➡️ URL publique ngrok : $ngrokUrl"

# 4. Envoyer l’URL à APEX (via REST)
Invoke-RestMethod -Uri $env:APEX_ENDPOINT `
	-Method Post `
	-ContentType "application/json" `
	-Body (@{ngrok_url=$ngrokUrl} | ConvertTo-Json)

Write-Host "✅ URL envoyée à APEX"

Pause
