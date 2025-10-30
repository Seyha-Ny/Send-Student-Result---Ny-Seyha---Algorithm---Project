# Test file upload
$filePath = "sample_data.csv"

if (-not (Test-Path $filePath)) {
    Write-Host "Error: sample_data.csv not found" -ForegroundColor Red
    exit 1
}

Write-Host "Testing file upload..." -ForegroundColor Green

$form = @{
    file = Get-Item -Path $filePath
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/upload" `
        -Method POST `
        -Form $form `
        -UseBasicParsing
    
    Write-Host "Response Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response Content:" -ForegroundColor Green
    Write-Host $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host $_.Exception.Response.Content
}

