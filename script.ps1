#Überprüft ob das Modul bereits installiert wurde.
if (!(Get-Module -ListAvailable -Name Mailozaurr)) {
    #Wenn das Modul nicht installiert ist, installiere das Modul
    Install-Module -Name Mailozaurr -AllowPrerelease2
}

# Welcome
Write-Host "|"
Write-Host "|  Willkommen zum CLI E-Mail Tool"
Write-Host "--------------------------------------------------------------------------------------"
Write-Host "|"
Write-Host "|  © 2024 by Levyn Schneider and David Meer"
Write-Host "|"

# Read Sender E-Mail from txt file
$sender = $null

# Simple function to create a new file and insert the email
function Get-Email() {
  Param($text)

  $sender = Read-Host "|  $text"

  if ($sender -match "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") {
    $sender | Out-File .\settings.txt
    Write-Host "|"
    Write-Host "--------------------------------------------------------------------------------------"
    Write-Host ""
  } else {
    Get-Email "Diese E-Mail-Adresse ist ungültig. Bitte geben Sie eine gültige E-Mail-Adresse ein"
  }
}

# Check if file exists
if (-not (Test-Path .\settings.txt)) {
    New-Item -ItemType file -Path .\settings.txt | Out-Null
    Get-Email "Bitte geben Sie Ihre E-Mail Adresse ein um fortzufahren"
} else {
  $sender = Get-Content .\settings.txt

  if ($sender -ne "" || $sender -ne $null) {
    if ($sender -match "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") {
      Write-Host "|  Konfigurierte Sender E-Mail Adresse: $sender"
      Write-Host "|"
      Write-Host "--------------------------------------------------------------------------------------"
      Write-Host ""
    } else {
      Get-Email "Deine Konfigurierte E-Mail Adresse ist ungültig. Bitte gib eine gültige E-Mail Adresse ein"
    }
  } else {
    Get-Email "Bitte geben Sie Ihre E-Mail Adresse ein um fortzufahren"
  }
}

# Menu Selector
Write-Host "Bitte wählen Sie eine Option:"
Write-Host "1 (Sender E-Mail)"
Write-Host "2 (E-Mail Senden)"
Write-Host "3 (E-Mail Empfangen)"
Write-Host "4 (Exit)"

# User Input
Write-Host ""
$option = Read-Host "Option wählen"

switch ($option) {
    1 { .\sender.ps1 }
    2 { .\send.ps1 }
    3 { .\receive.ps1 }
    4 { 
      Write-Host ""
      Write-Host "Auf Wiedersehen!"
     }
    default { Write-Host "Ungültige Option" }
}


# Send-MailMessage -From 'Absender@domain.com' -To 'Empfänger@domain.com' -Subject 'Betreff' -Body 'Nachrichtentext' -SmtpServer 'smtp.domain.com'