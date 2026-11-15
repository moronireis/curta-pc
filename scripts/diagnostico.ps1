# Diagnostico da maquina para o curta no PC. So le; nao instala nem altera nada.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\diagnostico.ps1
# Mensagens sem acento de proposito (PowerShell 5.1 le UTF-8 sem BOM como ANSI).

$ErrorActionPreference = 'SilentlyContinue'
$raiz = Split-Path -Parent $PSScriptRoot
$saida = Join-Path $raiz 'relatorio\maquina.md'

function Versao($cmd, $arg) {
    $c = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($null -eq $c) { return 'nao encontrado' }
    try { return ((& $cmd $arg 2>&1 | Select-Object -First 1) -as [string]) } catch { return 'erro ao consultar' }
}

$cpu  = (Get-CimInstance Win32_Processor | Select-Object -First 1)
$sis  = Get-CimInstance Win32_ComputerSystem
$so   = Get-CimInstance Win32_OperatingSystem
$gpus = Get-CimInstance Win32_VideoController
$pag  = Get-CimInstance Win32_PageFileUsage
$ramGB = [math]::Round($sis.TotalPhysicalMemory / 1GB)

$linhas = @()
$linhas += '# Maquina'
$linhas += ''
$linhas += "Coletado em $(Get-Date -Format 'yyyy-MM-dd HH:mm')."
$linhas += ''
$linhas += "- CPU: $($cpu.Name.Trim()) ($($cpu.NumberOfCores) nucleos, $($cpu.NumberOfLogicalProcessors) threads)"
$linhas += "- RAM: $ramGB GB"
$linhas += "- Windows: $($so.Caption) $($so.Version) ($($so.OSArchitecture))"
foreach ($g in $gpus) {
    $linhas += "- Placa de video: $($g.Name) | driver $($g.DriverVersion) de $($g.DriverDate.ToString('yyyy-MM-dd'))"
}
foreach ($p in $pag) {
    $linhas += "- Arquivo de paginacao: $($p.Name) | alocado $($p.AllocatedBaseSize) MB | pico $($p.PeakUsage) MB"
}
$linhas += ''
$linhas += '## Discos'
$linhas += ''
foreach ($d in (Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Free -gt 0 })) {
    $tipo = ''
    $linhas += "- $($d.Name): livre $([math]::Round($d.Free / 1GB)) GB de $([math]::Round(($d.Free + $d.Used) / 1GB)) GB"
}
foreach ($f in (Get-PhysicalDisk)) {
    $linhas += "- Disco fisico: $($f.FriendlyName) | $($f.MediaType) | $([math]::Round($f.Size / 1GB)) GB"
}
$linhas += ''
$linhas += '## Ferramentas'
$linhas += ''
$linhas += "- git: $(Versao 'git' '--version')"
$linhas += "- python: $(Versao 'python' '--version')"
$linhas += "- py launcher: $(Versao 'py' '--list')"
$linhas += "- ffmpeg: $(Versao 'ffmpeg' '-version')"
$linhas += "- gh: $(Versao 'gh' '--version')"
$linhas += "- 7z: $(Versao '7z' 'i')"
$linhas += "- winget: $(Versao 'winget' '--version')"
$linhas += "- C:\curta existe: $(Test-Path 'C:\curta')"
$linhas += ''
$linhas += '## Portao da fase A'
$linhas += ''
$livreMax = (Get-PSDrive -PSProvider FileSystem | Measure-Object -Property Free -Maximum).Maximum
$livreGB = [math]::Round($livreMax / 1GB)
$okRam = $ramGB -ge 16
$okDisco = $livreGB -ge 80
$linhas += "- RAM >= 16 GB: $okRam ($ramGB GB)"
$linhas += "- Disco livre >= 80 GB em alguma unidade: $okDisco ($livreGB GB)"
if ($ramGB -lt 32) { $linhas += '- Aviso: menos de 32 GB de RAM. Usar modelos quantizados menores e esperar lentidao.' }

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $saida) | Out-Null
$linhas | Out-File -FilePath $saida -Encoding utf8
$linhas | ForEach-Object { Write-Output $_ }
