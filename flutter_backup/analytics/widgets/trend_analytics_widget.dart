import 'package:controle_financas/pages/analytics/widgets/trend/trend_chart.dart';

import 'package:controle_financas/pages/analytics/widgets/trend/trend_summary_list.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:controle_financas/pages/analytics/analytics_viewmodel.dart';

class TrendAnalysisWidget extends StatelessWidget {
  const TrendAnalysisWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AnalysisViewModel>();
    final entries = vm.filteredEntries;

    if (entries.isEmpty) {
      return const Center(
        child: SizedBox(
          height: 400,
          child: Center(child: Text("Nenhuma transação encontrada")),
        ),
      );
    }

    final Set<String> allMonthsSet =
        entries.map((e) => DateFormat('yyyy-MM').format(e.data)).toSet();
    final List<String> sortedMonths = allMonthsSet.toList()..sort();

    final Map<String, Map<String, double>> groupedValues = {};

    for (var entry in entries) {
      final monthKey = DateFormat('yyyy-MM').format(entry.data);
      final groupKey =
          vm.selectedCategory == "Todas" ? entry.categoria : entry.subcategoria;

      groupedValues.putIfAbsent(groupKey, () => {});
      groupedValues[groupKey]![monthKey] =
          (groupedValues[groupKey]![monthKey] ?? 0) - entry.valor;
    }

    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        children: [
          Text(
            'Tendência Mensal por ${vm.selectedCategory == "Todas" ? 'Categoria' : 'Subcategoria'}',
            style: Theme.of(context).textTheme.titleLarge,
          ),
    
    
          const SizedBox(height: 12),
          Expanded(
            child: TrendChart(
              groupedValues: groupedValues,
              sortedMonths: sortedMonths,
            ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 300,
            child: TrendSummaryList(groupedValues: groupedValues),
          ),
        ],
      ),
    );
  }
}
