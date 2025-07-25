import 'package:flutter/material.dart';

class GastoDetalheCard extends StatelessWidget {
  final String categoria;
  final double valor;
  final double gastoTotal;
  final Color color;

  const GastoDetalheCard({
    super.key,
    required this.categoria,
    required this.valor,
    required this.gastoTotal,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color),
        title: Text(categoria),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              'R\$ ${valor.toStringAsFixed(2)}',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            Text(
              '${((valor.abs() / gastoTotal) * 100).toStringAsFixed(1)}%',
              style: TextStyle(
                fontSize: 12,
                color: Theme.of(context).textTheme.bodySmall?.color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
