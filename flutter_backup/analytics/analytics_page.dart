import 'package:controle_financas/pages/analytics/analytics_viewmodel.dart';
import 'package:controle_financas/pages/analytics/widgets/analytics_filters.dart';
import 'package:controle_financas/pages/analytics/widgets/forecast_analysis_widget.dart';
import 'package:controle_financas/pages/analytics/widgets/recurring_expenses_analytics_widget.dart';
import 'package:controle_financas/pages/analytics/widgets/summary_analytics_widget.dart';
import 'package:controle_financas/pages/analytics/widgets/trend_analytics_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AnalysisPage extends StatelessWidget {
  const AnalysisPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AnalysisViewModel(),
      child: Consumer<AnalysisViewModel>(
        builder: (context, vm, _) {
          return Column(
            children: [
              const AnalyticsFiltersWidget(),
              const Divider(height: 1),
              Expanded(
                child: _buildAnalysisContent(vm),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildAnalysisContent(AnalysisViewModel vm) {
    switch (vm.selectedAnalysisType) {
      case 'Sumário':
        return SummaryAnalysisWidget();
      case 'Tendência':
        return TrendAnalysisWidget();
      case 'Recorrência':
        return RecurringExpensesWidget();
      case 'Previsão':
        return ForecastAnalysisWidget();
      default:
        return const Center(child: Text('Tipo de análise desconhecido.'));
    }
  }
}
