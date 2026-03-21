# Legend website auto-update script
# Function: Update article timestamps every 2 hours, push to GitHub

$workspace = "C:\Users\Administrator\.openclaw\workspace\seo"
$date = Get-Date -Format "yyyy-MM-dd"

# Switch to website directory
Set-Location $workspace

# Update all HTML files with today's date
Write-Host "Updating article dates..."

# Get all HTML files
$htmlFiles = Get-ChildItem -Path $workspace -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    # Read file content
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    
    if ($content -match "\d{4}-\d{2}-\d{2}") {
        # Replace date format with current date
        $newContent = $content -replace '\d{4}-\d{2}-\d{2}', $date
        
        # Write back to file
        $newContent | Set-Content $file.FullName -NoNewline -Encoding UTF8
        Write-Host "Updated: $($file.Name)"
    }
}

# Git commit and push
Write-Host "Committing changes to GitHub..."
git add .
git commit -m "Auto update: Article date updated to $date"
git pull --rebase origin main
git push

Write-Host "Update complete!"
