#!/usr/bin/env php
<?php

declare(strict_types=1);

const LIMITE_PADRAO = 10.0;

$uso = "Uso: php crap.php <clover.xml> [--limite=10] [arquivo.php ...]\n";
$argumentos = array_slice($argv, 1);
if ($argumentos === [] || in_array($argumentos[0], ['-h', '--help'], true)) {
    fwrite($argumentos === [] ? STDERR : STDOUT, $uso);
    exit($argumentos === [] ? 2 : 0);
}

$relatorio = null;
$limite = LIMITE_PADRAO;
$filtros = [];
foreach ($argumentos as $argumento) {
    if (preg_match('/^--limite=(.+)$/u', $argumento, $m) === 1) {
        if (!is_numeric($m[1]) || (float) $m[1] <= 0) {
            fwrite(STDERR, "Limite inválido: {$m[1]}\n{$uso}");
            exit(2);
        }
        $limite = (float) $m[1];
    } elseif (str_starts_with($argumento, '-')) {
        fwrite(STDERR, "Argumento desconhecido: {$argumento}\n{$uso}");
        exit(2);
    } elseif ($relatorio === null) {
        $relatorio = $argumento;
    } else {
        $filtros[] = normalizar($argumento);
    }
}

$metodos = lerClover((string) $relatorio);
if ($metodos === null) {
    fwrite(STDERR, "Relatório Clover ilegível: {$relatorio}\n");
    exit(2);
}

$medidos = [];
$encontrados = [];
foreach ($metodos as $metodo) {
    $filtro = filtroDe($metodo['arquivo'], $filtros);
    if ($filtros !== [] && $filtro === null) {
        continue;
    }
    $encontrados[$filtro] = true;
    $medidos[] = $metodo;
}

$acima = array_values(array_filter($medidos, fn (array $metodo): bool => $metodo['crap'] >= $limite));
usort($acima, fn (array $a, array $b): int => $b['crap'] <=> $a['crap']);

foreach ($acima as $metodo) {
    printf(
        "CRAP %s  %s:%d  %s  complexidade %d\n",
        numero($metodo['crap']),
        exibir($metodo['arquivo']),
        $metodo['linha'],
        $metodo['nome'],
        $metodo['complexidade'],
    );
}
foreach ($filtros as $filtro) {
    if (!isset($encontrados[$filtro])) {
        echo "fora do relatório: {$filtro}", PHP_EOL;
    }
}
if ($acima !== []) {
    exit(1);
}
printf("OK: %d métodos, nenhum com CRAP >= %s.\n", count($medidos), numero($limite));
exit(0);

/**
 * @return list<array{arquivo: string, linha: int, nome: string, complexidade: int, crap: float}>|null
 */
function lerClover(string $caminho): ?array
{
    if (!is_file($caminho)) {
        return null;
    }
    $anterior = libxml_use_internal_errors(true);
    $xml = simplexml_load_file($caminho, options: LIBXML_NONET);
    libxml_use_internal_errors($anterior);
    if ($xml === false || $xml->getName() !== 'coverage') {
        return null;
    }

    $metodos = [];
    foreach ($xml->xpath('//file') ?: [] as $arquivo) {
        foreach ($arquivo->xpath('line[@type="method"]') ?: [] as $linha) {
            $metodos[] = [
                'arquivo' => (string) $arquivo['name'],
                'linha' => (int) $linha['num'],
                'nome' => (string) $linha['name'],
                'complexidade' => (int) $linha['complexity'],
                'crap' => (float) $linha['crap'],
            ];
        }
    }

    return $metodos;
}

/**
 * @param list<string> $filtros
 */
function filtroDe(string $arquivo, array $filtros): ?string
{
    $arquivo = normalizar($arquivo);
    foreach ($filtros as $filtro) {
        if ($arquivo === $filtro || str_ends_with($arquivo, '/' . $filtro)) {
            return $filtro;
        }
    }

    return null;
}

function normalizar(string $caminho): string
{
    $caminho = str_replace('\\', '/', $caminho);

    return str_starts_with($caminho, './') ? substr($caminho, 2) : $caminho;
}

function exibir(string $arquivo): string
{
    $raiz = normalizar((string) getcwd()) . '/';
    $arquivo = normalizar($arquivo);

    return str_starts_with($arquivo, $raiz) ? substr($arquivo, strlen($raiz)) : $arquivo;
}

function numero(float $valor): string
{
    return rtrim(rtrim(sprintf('%.2f', $valor), '0'), '.');
}
