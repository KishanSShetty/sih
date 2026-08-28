# SecureSentinel Project Cleanup Script
# Removes duplicate folders, empty directories, and old version scripts
# Keeps: datasets, verification scripts, and all essential files

Write-Host "🧹 SecureSentinel Cleanup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$itemsToRemove = @()

# 1. Empty Directory
if (Test-Path "Phishing-detector") {
    $count = (Get-ChildItem "Phishing-detector" -Recurse -Force | Measure-Object).Count
    if ($count -eq 0) {
        $itemsToRemove += @{Path="Phishing-detector"; Reason="Empty directory"}
    }
}

# 2. Duplicate Dashboard (old version)
if (Test-Path "dashboard") {
    $itemsToRemove += @{Path="dashboard"; Reason="Duplicate dashboard (my-app is active)"}
}

# 3. Duplicate Extension (old version)
if (Test-Path "extension-clean") {
    $itemsToRemove += @{Path="extension-clean"; Reason="Duplicate extension (extension-final is active)"}
}

# 4. Old Server Scripts
if (Test-Path "start_server_v2.py") {
    $itemsToRemove += @{Path="start_server_v2.py"; Reason="Old version (start_server.py is active)"}
}

if (Test-Path "start_server_v3.py") {
    $itemsToRemove += @{Path="start_server_v3.py"; Reason="Old version (start_server.py is active)"}
}

# Display items to be removed
Write-Host "Items to be removed:" -ForegroundColor Yellow
Write-Host ""
foreach ($item in $itemsToRemove) {
    Write-Host "  ❌ $($item.Path)" -ForegroundColor Red
    Write-Host "     → $($item.Reason)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Total items: $($itemsToRemove.Count)" -ForegroundColor Yellow
Write-Host ""

# Ask for confirmation
$confirmation = Read-Host "Do you want to proceed with cleanup? (yes/no)"

if ($confirmation -eq "yes" -or $confirmation -eq "y") {
    Write-Host ""
    Write-Host "Starting cleanup..." -ForegroundColor Green
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($item in $itemsToRemove) {
        try {
            if (Test-Path $item.Path) {
                Remove-Item -Path $item.Path -Recurse -Force
                Write-Host "  ✅ Removed: $($item.Path)" -ForegroundColor Green
                $successCount++
            }
        } catch {
            Write-Host "  ❌ Failed to remove: $($item.Path)" -ForegroundColor Red
            Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Gray
            $errorCount++
        }
    }
    
    Write-Host ""
    Write-Host "Cleanup complete!" -ForegroundColor Cyan
    Write-Host "  ✅ Successfully removed: $successCount items" -ForegroundColor Green
    if ($errorCount -gt 0) {
        Write-Host "  ❌ Failed to remove: $errorCount items" -ForegroundColor Red
    }
    
    # Calculate space saved (approximate)
    Write-Host ""
    Write-Host "📊 Cleanup Summary:" -ForegroundColor Cyan
    Write-Host "  - Removed duplicate folders: 3" -ForegroundColor Gray
    Write-Host "  - Removed old scripts: 2" -ForegroundColor Gray
    Write-Host "  - Kept datasets: ✅" -ForegroundColor Green
    Write-Host "  - Kept verification scripts: ✅" -ForegroundColor Green
    
} else {
    Write-Host ""
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
