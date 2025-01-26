# Create an ordered dictionary
$auditResults = [ordered]@{}

# Example: Check for Windows Update status
$updateStatus = Get-Service -Name wuauserv
if ($updateStatus.Status -eq "Running") {
    $auditResults["updateService"] = "Windows Update service is running."
} else {
    $auditResults["updateService"] = "Warning: Windows Update service is not running."
}

# Example: Check for Windows Defender status
$defenderStatus = Get-Service -Name WinDefend
if ($defenderStatus.Status -eq "Running") {
    $auditResults["defender"] = "Windows Defender Antivirus is running."
} else {
    $auditResults["defender"] = "Warning: Windows Defender Antivirus is not running."
}

# Add more CIS checks here...

# Add the completion message last
$auditResults["completion"] = "Audit completed."

# Convert to JSON
$auditResults | ConvertTo-Json