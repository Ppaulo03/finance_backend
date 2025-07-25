import 'package:controle_financas/pages/analytics/analytics_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

class ForecastAnalysisWidget extends StatelessWidget {
  const ForecastAnalysisWidget({super.key});

  List<String> _getSortedMonths(DateTime start, DateTime end) {
    List<String> months = [];
    DateTime current = DateTime(start.year, start.month);
    while (!current.isAfter(end)) {
      months.add(DateFormat('yyyy-MM').format(current));
      current = DateTime(current.year, current.month + 1);
    }
    return months;
  }

  String _formatValue(double value) {
    final formatter = NumberFormat.compactCurrency(
      decimalDigits: 0,
      symbol: 'R\$',
      locale: 'pt_BR',
    );
    return formatter.format(value);
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AnalysisViewModel>();
    final filtered = vm.filteredEntries;

    if (filtered.isEmpty) {
      return const Center(child: Text('Nenhuma transação encontrada'));
    }

    final now = DateTime.now();
    final startDate = DateTime(now.year, now.month - 6);
    final endDate = DateTime(now.year, now.month);

    // Agrupa valores por mês
    Map<String, double> monthlySums = {};
    for (var e in filtered) {
      final monthKey = DateFormat('yyyy-MM').format(e.data);
      monthlySums[monthKey] = (monthlySums[monthKey] ?? 0) - e.valor;
    }

    // Meses ordenados
    final months = _getSortedMonths(startDate, endDate);

    // Valores históricos
    final historicalValues = months.map((m) => monthlySums[m] ?? 0).toList();

    // Média móvel últimos 3 meses para previsão
    double avgLast3Months = 0;
    if (historicalValues.length >= 3) {
      avgLast3Months = historicalValues
              .sublist(historicalValues.length - 3)
              .reduce((a, b) => a + b) /
          3;
    }

    // Meses da previsão (próximos 3 meses)
    final forecastMonths = _getSortedMonths(
        DateTime(now.year, now.month), DateTime(now.year, now.month + 3));
    final forecastValues =
        List<double>.filled(forecastMonths.length, avgLast3Months);

    // Criar spots para gráfico (histórico + previsão)
    List<FlSpot> historicalSpots = [];
    List<FlSpot> forecastSpots = [];

    for (int i = 0; i < months.length; i++) {
      historicalSpots.add(FlSpot(i.toDouble(), historicalValues[i]));
    }

    for (int i = 0; i < forecastMonths.length; i++) {
      forecastSpots
          .add(FlSpot(months.length + i.toDouble(), forecastValues[i]));
    }

    // Máximo para eixo Y
    final maxYValue = [
      ...historicalValues,
      ...forecastValues,
    ].reduce((a, b) => a > b ? a : b);
    final maxY = (maxYValue * 1.2).ceilToDouble();

    // Controla quantos rótulos do eixo X mostrar para não poluir
    int intervalX = 1;
    if ((months.length + forecastMonths.length) > 8) {
      intervalX = 2;
    }
    if ((months.length + forecastMonths.length) > 12) {
      intervalX = 3;
    }

    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        children: [
          Text('Previsão de Gastos e Receitas',
              style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          Expanded(
            child: LineChart(
              LineChartData(
                minX: 0,
                maxX: (months.length + forecastMonths.length - 1).toDouble(),
                minY: 0,
                maxY: maxY,
                titlesData: FlTitlesData(
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      interval: intervalX.toDouble(),
                      getTitlesWidget: (value, meta) {
                        int idx = value.toInt();
                        String label = '';
                        if (idx < months.length) {
                          label = DateFormat('MM/yyyy')
                              .format(DateTime.parse('${months[idx]}-01'));
                        } else {
                          int forecastIdx = idx - months.length;
                          if (forecastIdx < forecastMonths.length) {
                            label = DateFormat('MM/yyyy').format(DateTime.parse(
                                '${forecastMonths[forecastIdx]}-01'));
                          }
                        }
                        return SideTitleWidget(
                          meta: meta,
                          child:
                              Text(label, style: const TextStyle(fontSize: 10)),
                        );
                      },
                    ),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 50,
                      interval: maxY / 5 > 0 ? maxY / 5 : 1,
                      getTitlesWidget: (value, meta) {
                        return Padding(
                          padding: const EdgeInsets.only(right: 6),
                          child: Text(
                            _formatValue(value),
                            style: const TextStyle(
                                fontSize: 10, color: Colors.black87),
                            textAlign: TextAlign.right,
                          ),
                        );
                      },
                    ),
                  ),
                  topTitles:
                      AxisTitles(sideTitles: SideTitles(showTitles: false)),
                ),
                gridData: FlGridData(show: true, horizontalInterval: maxY / 5),
                lineTouchData: LineTouchData(
                  touchTooltipData: LineTouchTooltipData(
                    getTooltipItems: (touchedSpots) {
                      return touchedSpots.map((spot) {
                        String monthLabel;
                        if (spot.x.toInt() < months.length) {
                          monthLabel = DateFormat('MM/yyyy').format(
                              DateTime.parse('${months[spot.x.toInt()]}-01'));
                        } else {
                          int fIdx = spot.x.toInt() - months.length;
                          monthLabel = DateFormat('MM/yyyy').format(
                              DateTime.parse('${forecastMonths[fIdx]}-01'));
                        }
                        return LineTooltipItem(
                          '$monthLabel\n${_formatValue(spot.y)}',
                          const TextStyle(color: Colors.white),
                        );
                      }).toList();
                    },
                  ),
                ),
                lineBarsData: [
                  LineChartBarData(
                    spots: historicalSpots,
                    isCurved: true,
                    color: Colors.blue,
                    barWidth: 3,
                    dotData: FlDotData(show: true),
                    belowBarData: BarAreaData(
                        show: true, color: Colors.blue.withValues(alpha: 0.3)),
                  ),
                  LineChartBarData(
                    spots: forecastSpots,
                    isCurved: true,
                    color: Colors.orange,
                    barWidth: 3,
                    dashArray: [6, 4],
                    dotData: FlDotData(show: false),
                    belowBarData: BarAreaData(
                        show: true,
                        color: Colors.orange.withValues(alpha: 0.3)),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: const [
              LegendItem(color: Colors.blue, label: 'Histórico'),
              SizedBox(width: 16),
              LegendItem(color: Colors.orange, label: 'Previsão'),
            ],
          ),
        ],
      ),
    );
  }
}

class LegendItem extends StatelessWidget {
  final Color color;
  final String label;

  const LegendItem({super.key, required this.color, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(width: 20, height: 10, color: color),
        const SizedBox(width: 6),
        Text(label),
      ],
    );
  }
}
