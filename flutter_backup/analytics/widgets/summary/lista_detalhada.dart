import 'package:flutter/material.dart';

class ListaDetalhada extends StatelessWidget {
  final Map<String, double> totals;
  final double gastoTotal;

  const ListaDetalhada({
    super.key,
    required this.totals,
    required this.gastoTotal,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: totals.entries.toList().length,
      itemBuilder: (context, index) {
        final e = totals.entries.toList()[index];
        final color = Colors.primaries[index % Colors.primaries.length];
        return ListTile(
          leading: CircleAvatar(backgroundColor: color, radius: 8),
          title: Text(e.key),
          trailing: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                'R\$ ${e.value.toStringAsFixed(2)}',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              Text(
                gastoTotal > 0
                    ? '${((e.value.abs() / gastoTotal) * 100).toStringAsFixed(1)}%'
                    : '',
                style: TextStyle(
                  fontSize: 12,
                  color: Theme.of(context).textTheme.bodySmall?.color,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
