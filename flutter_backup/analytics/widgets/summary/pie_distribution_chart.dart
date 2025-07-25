import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class PieDistributionChart extends StatelessWidget {
  final Map<String, double> totals;
  final int? touchedIndex;
  final Function(int?) onTouch;

  const PieDistributionChart({
    super.key,
    required this.totals,
    required this.touchedIndex,
    required this.onTouch,
  });

  @override
  Widget build(BuildContext context) {
    final keys = totals.keys.toList();

    final sections = keys.asMap().entries.map((entry) {
      final index = entry.key;
      final label = entry.value;
      final value = totals[label]!;
      final isTouched = touchedIndex == index;

      return PieChartSectionData(
        color: Colors.primaries[index % Colors.primaries.length],
        value: value,
        radius: isTouched ? 70 : 60,
        title: '',
      );
    }).toList();

    return SizedBox(
      height: 250,
      child: PieChart(
        PieChartData(
          sections: sections,
          sectionsSpace: 2,
          centerSpaceRadius: 30,
          pieTouchData: PieTouchData(
            touchCallback: (event, response) {
              if (!event.isInterestedForInteractions || response?.touchedSection == null) {
                onTouch(null);
              } else {
                onTouch(response!.touchedSection!.touchedSectionIndex);
              }
            },
          ),
        ),
      ),
    );
  }
}
