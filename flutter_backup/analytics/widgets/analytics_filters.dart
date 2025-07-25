import 'package:controle_financas/pages/analytics/analytics_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';

class AnalyticsFiltersWidget extends StatelessWidget {
  const AnalyticsFiltersWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AnalysisViewModel>();
    final formatter = DateFormat('dd/MM/yyyy');

    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        children: [
          Row(
            children: [
              // Categoria
              Expanded(
                child: DropdownButton<String?>(
                  isExpanded: true,
                  value: vm.selectedCategory,
                  onChanged: vm.setCategory,
                  hint: const Text('Categoria'),
                  items: ["Todas", ...vm.availableCategorias]
                      .map((cat) {
                    return DropdownMenuItem<String?>(
                      value: cat,
                      child: Text(cat),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(width: 8),
              // Tipo de análise
              Expanded(
                child: DropdownButton<String>(
                  isExpanded: true,
                  value: vm.selectedAnalysisType,
                  onChanged: (value) {
                    if (value != null) {
                      vm.setAnalysisType(value);
                    }
                  },
                  items: vm.availableAnalysisTypes.map((type) {
                    return DropdownMenuItem(
                      value: type,
                      child: Text(type),
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              // Data Início
              Expanded(
                child: OutlinedButton(
                  onPressed: () =>
                      _selectDate(context, vm.startDate, vm.minDate, vm.endDate, vm.setStartDate),
                  child: Text('Início: ${formatter.format(vm.startDate)}'),
                ),
              ),
              const SizedBox(width: 8),
              // Data Fim
              Expanded(
                child: OutlinedButton(
                  onPressed: () =>
                      _selectDate(context, vm.endDate, vm.startDate, vm.maxDate, vm.setEndDate),
                  child: Text('Fim: ${formatter.format(vm.endDate)}'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Future<void> _selectDate(BuildContext context, DateTime current, DateTime firstDate, DateTime lastDate,
      Function(DateTime) onSelected) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: current,
      firstDate: firstDate,
      lastDate: lastDate
    );
    if (picked != null) {
      onSelected(picked);
    }
  }
}
