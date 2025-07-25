import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class ProporcaoGastoChart extends StatelessWidget {
  final List<double> totaisGastos;
  final double receitaTotal;

  const ProporcaoGastoChart({
    super.key,
    required this.totaisGastos,
    required this.receitaTotal,
  });

  @override
  Widget build(BuildContext context) {
    final totalGastos = totaisGastos.fold(0.0, (a, b) => a + b);
    final restante = receitaTotal - totalGastos;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Proporção do Gasto em relação à Receita',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: 8),
        SizedBox(
          height: 250,
          child: PieChart(
            PieChartData(
              sections: [
                PieChartSectionData(
                  color: Colors.red,
                  value: totalGastos,
                  title: 'Gasto',
                  radius: 60,
                  titleStyle: const TextStyle(
                      fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
                ),
                PieChartSectionData(
                  color: Colors.green,
                  value: restante,
                  title: 'Restante',
                  radius: 60,
                  titleStyle: const TextStyle(
                      fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
                ),
              ],
              sectionsSpace: 2,
              centerSpaceRadius: 30,
            ),
          ),
        ),
      ],
    );
  }
}
