import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'dashboard_viewmodel.dart';
import 'widgets/summary_card.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<DashboardViewModel>(
      builder: (context, vm, _) {
        return Scaffold(
          body: RefreshIndicator(
            onRefresh: () => vm.loadResumo(forceReload: true),
            child: vm.isLoading
                ? const Center(child: CircularProgressIndicator())
                : vm.resumo == null
                    ? ListView(
                        physics: const AlwaysScrollableScrollPhysics(),
                        children: const [
                          SizedBox(
                            height: 400,
                            child:
                                Center(child: Text("Nenhum dado encontrado")),
                          ),
                        ],
                      )
                    : ListView(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        children: [
                          SummaryCard(
                            label: "Saldo Total",
                            value: vm.resumo!.saldoTotal,
                            backgroundColor: Colors.grey[100],
                            textColor: vm.resumo!.saldoTotal >= 0
                                ? Colors.green[900]
                                : Colors.red[900],
                          ),
                          const SizedBox(height: 8),
                          ...vm.resumo!.saldoPorConta.map((conta) {
                            final isPositivo = conta.valor >= 0;

                            return SummaryCard(
                              label: conta.nome,
                              value: conta.valor,
                              backgroundColor: isPositivo
                                  ? Colors.green[50]
                                  : Colors.red[50],
                              textColor: isPositivo
                                  ? Colors.green[900]
                                  : Colors.red[900],
                            );
                          }),
                          const SizedBox(height: 16),
                        ],
                      ),
          ),
        );
      },
    );
  }
}
