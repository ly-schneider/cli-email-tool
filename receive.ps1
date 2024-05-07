# Infinite loop to continuously fetch emails
while ($true) {
  $Content = Get-Content .\settings.txt
  $From = $Content[0]
  $Password = $Content[1]

  # load rss-feed
  $webclient = new-object System.Net.WebClient

  # access the rss-feed
  $webclient.Credentials = new-object System.Net.NetworkCredential ($From, $Password)

  # download the rss as xml
  [xml]$xml= $webclient.DownloadString("https://mail.google.com/mail/feed/atom")

  # display only sender name and message title as custom table
  $format= @{Expression={$_.issued};Label="Zugestellt"},
           @{Expression={$_.author.email};Label="E-Mail"},
           @{Expression={$_.title};Label="Subjekt"},
           @{Expression={$_.summary};Label="Nachricht"}

  if ($xml.feed.entry -eq $null) {
      Write-Host "Keine ungelesenen E-Mails vorhanden"
  } else {
      # display the table
      $xml.feed.entry | Format-Table $format
  }

  # Wait for 30 seconds before fetching emails again
  Start-Sleep -Seconds 10
}
