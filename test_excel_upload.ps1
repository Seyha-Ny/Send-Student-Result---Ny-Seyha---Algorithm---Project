# Test Excel file upload
$filePath = "test_students.xlsx"

if (-not (Test-Path $filePath)) {
    Write-Host "Error: $filePath not found"
    exit 1
}

Write-Host "Uploading Excel file: $filePath"

# Create multipart form data
$uri = "http://localhost:5000/api/upload"
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$fileName = [System.IO.Path]::GetFileName($filePath)

# Create boundary
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

# Build the body
$bodyLines = @(
    "--$boundary",
    "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
    "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "",
    [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($fileBytes),
    "--$boundary--"
)

$body = $bodyLines -join $LF

try {
    $response = Invoke-WebRequest -Uri $uri `
        -Method POST `
        -ContentType "multipart/form-data; boundary=$boundary" `
        -Body $body `
        -UseBasicParsing

    Write-Host "Upload Status: $($response.StatusCode)"
    Write-Host "Response:"
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Host "Response Status: $($_.Exception.Response.StatusCode)"
        Write-Host "Response Content: $($_.Exception.Response.Content.ReadAsStream() | Get-Content)"
    }
}

