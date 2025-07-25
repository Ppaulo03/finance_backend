import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import 'dart:math' as math;

class TrendChart extends StatelessWidget {
  final Map<String, Map<String, double>> groupedValues;
  final List<String> sortedMonths;

  const TrendChart({
    super.key,
    required this.groupedValues,
    required this.sortedMonths,
  });

  @override
  Widget build(BuildContext context) {
    final formatterCurrency = NumberFormat.simpleCurrency(locale: 'pt_BR');
    final colors = Colors.primaries;

    double maxYValue = 0;
    final series = groupedValues.entries.toList().asMap().entries.map((entry) {
      final idx = entry.key;
      final monthMap = entry.value.value;

      final spots = List.generate(sortedMonths.length, (i) {
        final val = monthMap[sortedMonths[i]] ?? 0;
        if (val > maxYValue) maxYValue = val;
        return FlSpot(i.toDouble(), val);
      });

      final color = colors[idx % colors.length].shade700;

      return LineChartBarData(
        spots: spots,
        isCurved: true,
        curveSmoothness: 0.3,
        color: color,
        barWidth: 4,
        isStrokeCapRound: true,
        dotData: FlDotData(
          show: true,
          getDotPainter: (spot, percent, barData, index) => FlDotCirclePainter(
            radius: 5,
            color: color,
            strokeWidth: 2,
            strokeColor: Colors.white,
          ),
        ),
        belowBarData: BarAreaData(
          show: true,
          gradient: LinearGradient(
            colors: [color.withValues(alpha: 0.4), color.withValues(alpha: 0.1)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
      );
    }).toList();

    double axisMaxY = (maxYValue / 10).ceil() * 10;
    if (axisMaxY == 0) axisMaxY = 10;

    return LineChart(
      LineChartData(
        minX: 0,
        maxX: (sortedMonths.length - 1).toDouble() * 1.1,
        minY: 0,
        maxY: axisMaxY * 1.1,
        clipData: FlClipData.all(),
        lineTouchData: LineTouchData(
          touchTooltipData: LineTouchTooltipData(
            getTooltipItems: (spots) => spots.map((spot) {
              if (spot.y == 0) return null;
              final label = groupedValues.keys.toList()[spot.barIndex];
              return LineTooltipItem(
                '$label\nR\$ ${spot.y.toStringAsFixed(2)}',
                const TextStyle(
                    color: Colors.white, fontWeight: FontWeight.bold),
              );
            }).toList(),
          ),
        ),
        titlesData: FlTitlesData(
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              interval: 1,
              reservedSize: 32,
              getTitlesWidget: (value, meta) {
                final index = value.toInt();
                if (index < 0 ||
                    index >= sortedMonths.length ||
                    index % 2 != 0) {
                  return const SizedBox.shrink();
                }
                final label = DateFormat('MM/yy')
                    .format(DateTime.parse('${sortedMonths[index]}-01'));
                return SideTitleWidget(
                  meta: meta,
                  space: 6,
                  child: Transform.rotate(
                    angle: -math.pi / 6,
                    child: Text(label, style: const TextStyle(fontSize: 10)),
                  ),
                );
              },
            ),
          ),
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 70,
              interval: axisMaxY / 5,
              getTitlesWidget: (value, meta) {
                if (value == 0) return const SizedBox.shrink();
                return SideTitleWidget(
                  meta: meta,
                  space: 6,
                  child: Text(formatterCurrency.format(value),
                      style: const TextStyle(fontSize: 10)),
                );
              },
            ),
          ),
          rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        ),
        gridData: FlGridData(
          show: true,
          drawVerticalLine: true,
          horizontalInterval: axisMaxY / 5,
          verticalInterval: 1,
          getDrawingHorizontalLine: (_) =>
              FlLine(color: Colors.grey.withValues(alpha: 0.3), strokeWidth: 1),
          getDrawingVerticalLine: (_) =>
              FlLine(color: Colors.grey.withValues(alpha: 0.3), strokeWidth: 1),
        ),
        borderData: FlBorderData(
          show: true,
          border: Border.all(color: Colors.grey.shade300),
        ),
        lineBarsData: series,
      ),
    );
  }
}
