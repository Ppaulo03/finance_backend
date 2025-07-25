import 'package:flutter/material.dart';

class TrendSummaryList extends StatelessWidget {
  final Map<String, Map<String, double>> groupedValues;

  const TrendSummaryList({super.key, required this.groupedValues});

  @override
  Widget build(BuildContext context) {
    final colors = Colors.primaries;

    return ListView(
      children: groupedValues.entries.toList().asMap().entries.map((entry) {
        final idx = entry.key;
        final groupKey = entry.value.key;
        final monthMap = entry.value.value;

        final sortedValues = monthMap.entries.toList()
          ..sort((a, b) => a.key.compareTo(b.key));

        if (sortedValues.length < 2) return const SizedBox();

        final first = sortedValues.first.value;
        final last = sortedValues.last.value;

        double percentChange = 0;
        if (first != 0) percentChange = ((last - first) / first) * 100;

        final arrow = percentChange > 2
            ? '↑'
            : percentChange < -2
                ? '↓'
                : '→';

        final colorTrend = percentChange > 2
            ? Colors.red
            : percentChange < -2
                ? Colors.green
                : Colors.grey;

        final color = colors[idx % colors.length].shade700;
        final formattedChange = '${percentChange.abs().toStringAsFixed(1)}%';

        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Row(
            children: [
              Container(width: 20, height: 10, color: color),
              const SizedBox(width: 8),
              Expanded(
                child: Text(groupKey, style: const TextStyle(fontSize: 14)),
              ),
              Text(
                '$arrow $formattedChange',
                style:
                    TextStyle(fontWeight: FontWeight.bold, color: colorTrend),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}
