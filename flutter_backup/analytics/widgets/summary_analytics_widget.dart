import 'package:controle_financas/pages/analytics/analytics_viewmodel.dart';
import 'package:controle_financas/pages/analytics/widgets/summary/gasto_detalhe_card.dart';
import 'package:controle_financas/pages/analytics/widgets/summary/lista_detalhada.dart';
import 'package:controle_financas/pages/analytics/widgets/summary/pie_distribution_chart.dart';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class SummaryAnalysisWidget extends StatefulWidget {
  const SummaryAnalysisWidget({super.key});

  @override
  State<SummaryAnalysisWidget> createState() => _SummaryAnalysisWidgetState();
}

class _SummaryAnalysisWidgetState extends State<SummaryAnalysisWidget> {
  int? touchedIndex;

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AnalysisViewModel>();

    final filteredEntries = vm.filteredEntries;

    final gastoTotal =
        filteredEntries.fold<double>(0, (sum, e) => sum - e.valor);

    final Map<String, double> totals = {};
    for (var e in filteredEntries) {
      final key = vm.selectedCategory == "Todas" ? e.categoria : e.subcategoria;
      totals[key] = (totals[key] ?? 0) + e.valor;
    }

    final keys = totals.keys.toList();

    if (totals.isEmpty) {
      return const Center(
        child: SizedBox(
          height: 400,
          child: Center(child: Text("Nenhuma transação encontrada")),
        ),
      );
    }

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            vm.selectedCategory == "Todas"
                ? 'Distribuição por Categoria'
                : 'Distribuição por Subcategoria',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          PieDistributionChart(
            totals: totals,
            touchedIndex: touchedIndex,
            onTouch: (i) => setState(() => touchedIndex = i),
          ),
          if (touchedIndex != null && touchedIndex! >= 0)
            GastoDetalheCard(
              categoria: keys[touchedIndex!],
              valor: totals[keys[touchedIndex!]]!,
              color: Colors.primaries[touchedIndex! % Colors.primaries.length],
              gastoTotal: gastoTotal,
            ),
          const SizedBox(height: 16),
          Text('Lista Detalhada',
              style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          Expanded(
            child: ListaDetalhada(
              totals: totals,
              gastoTotal: gastoTotal,
            ),
          ),
        ],
      ),
    );
  }
}
