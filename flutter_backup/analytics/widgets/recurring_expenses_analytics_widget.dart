import 'package:controle_financas/core/models/financial_entry.dart';
import 'package:controle_financas/pages/analytics/analytics_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

class RecurringExpensesWidget extends StatelessWidget {
  

  const RecurringExpensesWidget({super.key});

  @override
  Widget build(BuildContext context) {
    // Filtra só gastos (tipo 'Gasto')
    final vm = context.watch<AnalysisViewModel>();
    final gastos = vm.filteredEntries;

    if (gastos.isEmpty) {
      return const Center(
        child: SizedBox(
          height: 400,
          child: Center(child: Text("Nenhuma recorrência encontrada")),
        ),
      );
    }


    Map<String, Map<String, List<FinancialEntry>>> groupedByDescAndMonth = {};

    for (var entry in gastos) {
      final key = '${entry.nome} - ${entry.categoria}';
      final month = DateFormat('yyyy-MM').format(entry.data);

      groupedByDescAndMonth.putIfAbsent(key, () => {});
      groupedByDescAndMonth[key]!.putIfAbsent(month, () => []);
      groupedByDescAndMonth[key]![month]!.add(entry);
    }

    // Identificar recorrentes: que aparecem em >= 3 meses (exemplo)
    final recurringKeys = groupedByDescAndMonth.entries
        .where((e) => e.value.length >= 3)
        .toList();

    // Para cada recorrente, calcular valor médio mensal
    final recurringSummaries = recurringKeys.map((entry) {
      final key = entry.key;
      final months = entry.value.length;
      double totalValue = 0;
      for (var listEntries in entry.value.values) {
        totalValue += listEntries.fold(0, (sum, e) => sum + e.valor);
      }
      final avgMonthly = totalValue / months;
      return {
        'key': key,
        'months': months,
        'avgMonthly': avgMonthly,
      };
    }).toList();

    // Ordenar do maior para o menor gasto médio
    recurringSummaries.sort((a, b) => (b['avgMonthly'] as double).compareTo(a['avgMonthly'] as double));

    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Gastos Recorrentes', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          Expanded(
            child: recurringSummaries.isEmpty
                ? const Center(child: Text('Nenhum gasto recorrente encontrado'))
                : ListView.separated(
                    itemCount: recurringSummaries.length,
                    separatorBuilder: (_, __) => const Divider(),
                    itemBuilder: (context, index) {
                      final item = recurringSummaries[index];
                      final key = item['key'] as String;
                      final avgMonthly = item['avgMonthly'] as double;
                      final months = item['months'] as int;

                      return ListTile(
                        title: Text(key),
                        subtitle: Text('Média mensal em $months meses'),
                        trailing: Text(
                          NumberFormat.currency(locale: 'pt_BR', symbol: 'R\$').format(avgMonthly),
                          style: TextStyle(
                            color: avgMonthly > 0 ? Colors.green : Colors.red,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
