<div>
    <table>
        @foreach ($pedidos as $pedido)
            <tr wire:key="pedido-{{ $pedido->id }}">
                <td>{{ $pedido->id }}</td>
                <td>{{ number_format($pedido->total_centavos / 100, 2, ',', '.') }}</td>
                <td>{{ $pedido->status->name }}</td>
            </tr>
        @endforeach
    </table>
</div>
