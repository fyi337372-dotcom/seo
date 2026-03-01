# 传奇网站自动更新脚本
# 功能：每2小时自动更新文章时间戳，推送到GitHub

$workspace = "C:\Users\Administrator\.openclaw\workspace\seo"
$date = Get-Date -Format "yyyy-MM-dd"

# 切换到网站目录
Set-Location $workspace

# 更新所有HTML文件中的日期为今天
Write-Host "正在更新文章日期..."

# 获取所有HTML文件
$htmlFiles = Get-ChildItem -Path $workspace -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    # 读取文件内容
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    
    if ($content -match "\d{4}-\d{2}-\d{2}") {
        # 替换日期格式为当前日期
        $newContent = $content -replace '\d{4}-\d{2}-\d{2}', $date
        
        # 写回文件
        $newContent | Set-Content $file.FullName -NoNewline
        Write-Host "已更新: $($file.Name)"
    }
}

# Git提交和推送
Write-Host "正在提交更改到GitHub..."
git add .
git commit -m "自动更新：文章日期更新至 $date"
git pull --rebase origin main
git push

Write-Host "更新完成！"
