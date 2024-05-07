Write-Host ""
Write-Host "Bitte wählen Sie eine Option:"
Write-Host "1 (Meine E-Mail-Adresse ändern)"
Write-Host "2 (Meine ausgewählte E-Mail-Adresse zeigen)" 

Write-Host ""
$option = Read-Host "Option wählen"

switch ($option) {
  1 { 
    $confirm = Read-Host "Sind Sie sicher, dass Sie die E-Mail-Adresse ändern möchten? (j/n)"
    if ($confirm -eq 'j') {
      $sender = $null

      while ($sender -eq $null) {
        $sender = Read-Host "Bitte geben Sie eine neue E-Mail-Adresse ein"
        if ($sender -match "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") {
          $sender | Out-File .\settings.txt
          .\script.ps1
        } else {
          Write-Host ""
          Write-Host "Diese E-Mail-Adresse ist ungültig. Bitte geben Sie eine gültige E-Mail-Adresse ein."
          $sender = $null
        }
      }
    } else {
      Write-Host "Änderung abgebrochen."
      .\script.ps1
    }
  }
  2 { 
    $sender = Get-Content .\settings.txt
    Write-Host ""
    Write-Host "Ihre konfigurierte Sender E-Mail-Adresse ist: $sender"
    Write-Host ""
    .\script.ps1
   }
   default { Write-Host "Ungültige Option" }
}