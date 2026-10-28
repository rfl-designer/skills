#!/usr/bin/env php
<?php

declare(strict_types=1);

const SECOES_DA_FEATURE = ['Sub-features', 'Como chegar (visão do usuário)', 'Como conduzir', 'Armadilhas'];
const SECOES_DO_INDICE = [
    'Pré-condições base', 'Convenções de condução', 'Prova e lacunas', 'Varredura completa',
    'Domínios', 'Fora do mapa', 'Contrato dos Arquivos de Feature', 'Manutenção',
];
const PREFIXOS = ['rota', 'livewire', 'comando', 'agenda', 'notificacao', 'flag', 'outro'];
const LINHA_BASE = '/^Base: commit [0-9a-f]{7,40} em \d{4}-\d{2}-\d{2}\b/u';
const LINHA_ESTADO = '/^Estado: (conduzida|parcial|não conduzida|bloqueada) em \d{4}-\d{2}-\d{2}, commit [0-9a-f]{7,40}\b/u';
const ID_DA_SUB_FEATURE = '/^- `([a-z0-9]+(?:-[a-z0-9]+)*)`/u';

$uso = "Uso: php conferir-mapa.php <pasta-do-mapa> [--ancoras=<arquivo>]\n";
$argumentos = array_slice($argv, 1);
if ($argumentos === [] || in_array($argumentos[0], ['-h', '--help'], true)) {
    fwrite($argumentos === [] ? STDERR : STDOUT, $uso);
    exit($argumentos === [] ? 2 : 0);
}

$pasta = null;
$inventario = null;
for ($i = 0; $i < count($argumentos); $i++) {
    $argumento = $argumentos[$i];
    if (str_starts_with($argumento, '--ancoras=')) {
        $inventario = substr($argumento, strlen('--ancoras='));
    } elseif ($argumento === '--ancoras' && isset($argumentos[$i + 1])) {
        $inventario = $argumentos[++$i];
    } elseif ($pasta === null && !str_starts_with($argumento, '-')) {
        $pasta = $argumento;
    } else {
        fwrite(STDERR, "Argumento desconhecido: {$argumento}\n{$uso}");
        exit(2);
    }
}

$raiz = $pasta === null ? false : realpath($pasta);
if ($raiz === false || !is_dir($raiz)) {
    fwrite(STDERR, "Pasta do mapa não encontrada: {$pasta}\n");
    exit(2);
}
if ($inventario !== null && !is_file($inventario)) {
    fwrite(STDERR, "Inventário não encontrado: {$inventario}\n");
    exit(2);
}

$erros = conferir($raiz, $inventario);
foreach ($erros['lista'] as $erro) {
    echo $erro, PHP_EOL;
}
if ($erros['lista'] !== []) {
    exit(1);
}
echo $erros['resumo'], PHP_EOL;
exit(0);

/**
 * @return array{lista: list<string>, resumo: string}
 */
function conferir(string $raiz, ?string $inventario): array
{
    $erros = [];
    $indice = $raiz . DIRECTORY_SEPARATOR . 'README.md';
    if (!is_file($indice)) {
        return ['lista' => ['README.md: índice ausente'], 'resumo' => ''];
    }

    $arquivos = arquivosMarkdown($raiz);
    $documentos = [];
    foreach ($arquivos as $arquivo) {
        $documento = ler($arquivo);
        if ($documento['cerca_aberta']) {
            $erros[] = relativo($raiz, $arquivo) . ': bloco de código sem fechamento';
        }
        $documentos[$arquivo] = $documento;
    }

    $erros = array_merge($erros, conferirIndice($documentos[$indice]));
    $erros = array_merge($erros, conferirLinks($raiz, $indice, $documentos));

    $ancoras = [];
    $ids = [];
    $features = 0;
    foreach ($documentos as $arquivo => $documento) {
        $nome = relativo($raiz, $arquivo);
        if (basename($arquivo) === 'README.md' || $nome === 'jornadas.md') {
            continue;
        }
        $features++;
        $erros = array_merge($erros, conferirFeature($nome, $documento, $ancoras, $ids));
    }

    $foraDoMapa = [];
    foreach (secoes($documentos[$indice]['prosa'])['secoes']['Fora do mapa'] ?? [] as $numero => $linha) {
        foreach (codigosInline($linha) as $codigo) {
            if (ehAncora($codigo)) {
                $foraDoMapa[$codigo] = "README.md:{$numero}";
            }
        }
    }

    foreach (array_intersect_key($foraDoMapa, $ancoras) as $codigo => $origem) {
        $erros[] = "{$origem}: Âncora em Fora do mapa e também em {$ancoras[$codigo]}: {$codigo}";
    }

    $resumo = sprintf('OK: %d Arquivos de Feature, %d Sub-features, %d Âncoras', $features, count($ids), count($ancoras));
    if ($inventario !== null) {
        [$errosDoInventario, $cobertos] = conferirInventario($inventario, $ancoras, $foraDoMapa);
        $erros = array_merge($erros, $errosDoInventario);
        $resumo .= sprintf('; inventário: %d itens cobertos', $cobertos);
    }

    return ['lista' => $erros, 'resumo' => $resumo];
}

/**
 * @param array{prosa: array<int, string>, cerca_aberta: bool} $documento
 * @return list<string>
 */
function conferirIndice(array $documento): array
{
    $erros = [];
    $partes = secoes($documento['prosa']);
    if (!array_filter($partes['cabecalho'], fn (string $linha): bool => preg_match(LINHA_BASE, $linha) === 1)) {
        $erros[] = 'README.md: falta a linha "Base: commit <sha> em AAAA-MM-DD" antes da primeira H2';
    }
    foreach (SECOES_DO_INDICE as $secao) {
        if (!array_key_exists($secao, $partes['secoes'])) {
            $erros[] = "README.md: falta a seção \"## {$secao}\"";
        }
    }
    return $erros;
}

/**
 * @param array<string, array{prosa: array<int, string>, cerca_aberta: bool}> $documentos
 * @return list<string>
 */
function conferirLinks(string $raiz, string $indice, array $documentos): array
{
    $erros = [];
    $alcancados = [$indice => true];
    $fila = [$indice];
    while ($fila !== []) {
        $arquivo = array_shift($fila);
        foreach ($documentos[$arquivo]['prosa'] as $numero => $linha) {
            foreach (alvosDeLinks($linha) as $alvo) {
                $caminho = realpath(dirname($arquivo) . DIRECTORY_SEPARATOR . $alvo);
                if ($caminho === false) {
                    $erros[] = relativo($raiz, $arquivo) . ":{$numero}: link quebrado: {$alvo}";
                    continue;
                }
                if (isset($documentos[$caminho]) && !isset($alcancados[$caminho])) {
                    $alcancados[$caminho] = true;
                    $fila[] = $caminho;
                }
            }
        }
    }
    foreach (array_keys($documentos) as $arquivo) {
        if (!isset($alcancados[$arquivo])) {
            $erros[] = relativo($raiz, $arquivo) . ': arquivo fora do índice; ligue-o a partir do README.md';
        }
    }
    return $erros;
}

/**
 * @param array{prosa: array<int, string>, cerca_aberta: bool} $documento
 * @param array<string, string> $ancoras
 * @param array<string, string> $ids
 * @return list<string>
 */
function conferirFeature(string $nome, array $documento, array &$ancoras, array &$ids): array
{
    $erros = [];
    $prosa = $documento['prosa'];
    $primeira = array_values(array_filter($prosa, fn (string $linha): bool => trim($linha) !== ''))[0] ?? '';
    if (!str_starts_with($primeira, '# ')) {
        $erros[] = "{$nome}: a primeira linha deve ser o título H1";
    }

    $partes = secoes($prosa);
    $linhaDeAncoras = null;
    $temEstado = false;
    foreach ($partes['cabecalho'] as $numero => $linha) {
        if (str_starts_with($linha, 'Âncoras:')) {
            $linhaDeAncoras = $numero;
            $codigos = codigosInline($linha);
            if ($codigos === []) {
                $erros[] = "{$nome}:{$numero}: a linha Âncoras não tem Âncora entre crases";
            }
            foreach ($codigos as $codigo) {
                if (!ehAncora($codigo)) {
                    $erros[] = "{$nome}:{$numero}: Âncora com prefixo inválido: {$codigo}";
                } elseif (isset($ancoras[$codigo])) {
                    $erros[] = "{$nome}:{$numero}: Âncora repetida; já está em {$ancoras[$codigo]}: {$codigo}";
                } else {
                    $ancoras[$codigo] = "{$nome}:{$numero}";
                }
            }
        }
        if (preg_match(LINHA_ESTADO, $linha) === 1) {
            $temEstado = true;
        }
    }
    if ($linhaDeAncoras === null) {
        $erros[] = "{$nome}: falta a linha \"Âncoras:\" antes da primeira H2";
    }
    if (!$temEstado) {
        $erros[] = "{$nome}: falta a linha \"Estado: <valor> em AAAA-MM-DD, commit <sha>\" antes da primeira H2";
    }

    $titulos = array_keys($partes['secoes']);
    if ($titulos !== SECOES_DA_FEATURE) {
        $erros[] = sprintf('%s: as H2 devem ser exatamente "%s", nesta ordem; encontradas: "%s"',
            $nome, implode('", "', SECOES_DA_FEATURE), implode('", "', $titulos));
    }

    $subFeatures = 0;
    foreach ($partes['secoes']['Sub-features'] ?? [] as $numero => $linha) {
        if (!str_starts_with($linha, '- ')) {
            continue;
        }
        if (preg_match(ID_DA_SUB_FEATURE, $linha, $m) !== 1) {
            $erros[] = "{$nome}:{$numero}: a Sub-feature deve começar com um ID kebab-case entre crases";
            continue;
        }
        $subFeatures++;
        if (isset($ids[$m[1]])) {
            $erros[] = "{$nome}:{$numero}: ID de Sub-feature repetido; já está em {$ids[$m[1]]}: {$m[1]}";
        } else {
            $ids[$m[1]] = "{$nome}:{$numero}";
        }
    }
    if (isset($partes['secoes']['Sub-features']) && $subFeatures === 0) {
        $erros[] = "{$nome}: a seção Sub-features não tem item";
    }

    $conducao = $partes['secoes']['Como conduzir'] ?? null;
    if ($conducao !== null && !array_filter($conducao, fn (string $linha): bool => str_starts_with($linha, 'Pré-condições:'))) {
        $erros[] = "{$nome}: a seção Como conduzir deve ter a linha \"Pré-condições:\"";
    }

    return $erros;
}

/**
 * @param array<string, string> $ancoras
 * @param array<string, string> $foraDoMapa
 * @return array{0: list<string>, 1: int}
 */
function conferirInventario(string $inventario, array $ancoras, array $foraDoMapa): array
{
    $erros = [];
    $itens = [];
    foreach (preg_split('/\R/u', (string) file_get_contents($inventario)) as $indice => $linha) {
        $item = trim($linha);
        if ($item === '' || str_starts_with($item, '#')) {
            continue;
        }
        if (!ehAncora($item)) {
            $erros[] = "inventário:" . ($indice + 1) . ": item com prefixo inválido: {$item}";
            continue;
        }
        $itens[$item] = true;
    }

    $cobertos = 0;
    $conhecidas = $ancoras + $foraDoMapa;
    foreach (array_keys($itens) as $item) {
        $cobre = array_filter(array_keys($conhecidas), fn (string $ancora): bool => cobre($ancora, $item));
        if ($cobre === []) {
            $erros[] = "inventário: item sem Feature e fora da seção Fora do mapa: {$item}";
        } else {
            $cobertos++;
        }
    }

    foreach ($conhecidas as $ancora => $origem) {
        if (str_starts_with($ancora, 'outro:')) {
            continue;
        }
        if (!array_filter(array_keys($itens), fn (string $item): bool => cobre($ancora, $item))) {
            $erros[] = "{$origem}: Âncora sem correspondência no inventário: {$ancora}";
        }
    }

    return [$erros, $cobertos];
}

function cobre(string $ancora, string $item): bool
{
    if (str_ends_with($ancora, '*')) {
        return str_starts_with($item, substr($ancora, 0, -1));
    }
    return $ancora === $item;
}

function ehAncora(string $codigo): bool
{
    return preg_match('/^([a-z]+):\S/u', $codigo, $m) === 1 && in_array($m[1], PREFIXOS, true);
}

/**
 * @return list<string>
 */
function codigosInline(string $linha): array
{
    preg_match_all('/`([^`]+)`/u', $linha, $m);
    return $m[1];
}

/**
 * @return list<string>
 */
function alvosDeLinks(string $linha): array
{
    $semCodigo = preg_replace('/`[^`]+`/u', '', $linha) ?? $linha;
    preg_match_all('/\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)/u', $semCodigo, $m);
    $alvos = [];
    foreach ($m[1] as $alvo) {
        $alvo = trim($alvo, '<>');
        if (preg_match('/^[a-z][a-z0-9+.-]*:/i', $alvo) === 1 || str_starts_with($alvo, '#')) {
            continue;
        }
        $alvo = rawurldecode((string) preg_replace('/[#?].*$/u', '', $alvo));
        if ($alvo !== '') {
            $alvos[] = $alvo;
        }
    }
    return $alvos;
}

/**
 * @param array<int, string> $prosa
 * @return array{cabecalho: array<int, string>, secoes: array<string, array<int, string>>}
 */
function secoes(array $prosa): array
{
    $cabecalho = [];
    $secoes = [];
    $atual = null;
    foreach ($prosa as $numero => $linha) {
        if (preg_match('/^## (.+?)\s*$/u', $linha, $m) === 1) {
            $atual = $m[1];
            $secoes[$atual] = $secoes[$atual] ?? [];
            continue;
        }
        if ($atual === null) {
            $cabecalho[$numero] = $linha;
        } else {
            $secoes[$atual][$numero] = $linha;
        }
    }
    return ['cabecalho' => $cabecalho, 'secoes' => $secoes];
}

/**
 * @return array{prosa: array<int, string>, cerca_aberta: bool}
 */
function ler(string $arquivo): array
{
    $prosa = [];
    $cerca = null;
    foreach (preg_split('/\R/u', (string) file_get_contents($arquivo)) as $indice => $linha) {
        if (preg_match('/^\s*(`{3,}|~{3,})(.*)$/u', $linha, $m) === 1) {
            if ($cerca === null) {
                $cerca = $m[1];
            } elseif ($m[1][0] === $cerca[0] && strlen($m[1]) >= strlen($cerca) && trim($m[2]) === '') {
                $cerca = null;
            }
            continue;
        }
        if ($cerca === null) {
            $prosa[$indice + 1] = $linha;
        }
    }
    return ['prosa' => $prosa, 'cerca_aberta' => $cerca !== null];
}

/**
 * @return list<string>
 */
function arquivosMarkdown(string $raiz): array
{
    $arquivos = [];
    $iterador = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($raiz, FilesystemIterator::SKIP_DOTS));
    foreach ($iterador as $arquivo) {
        if ($arquivo->isFile() && strtolower($arquivo->getExtension()) === 'md') {
            $arquivos[] = (string) $arquivo->getRealPath();
        }
    }
    sort($arquivos);
    return $arquivos;
}

function relativo(string $raiz, string $arquivo): string
{
    return str_replace(DIRECTORY_SEPARATOR, '/', substr($arquivo, strlen($raiz) + 1));
}
