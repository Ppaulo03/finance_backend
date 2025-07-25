import 'package:controle_financas/core/models/financial_entry.dart';
import 'package:controle_financas/pages/tagging/tagging_viewmodel.dart';
import 'package:controle_financas/pages/tagging/widgets/tagging_entry_tile.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TaggingPage extends StatelessWidget {
  const TaggingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<TaggingViewModel>(
      builder: (context, vm, _) {
        return Scaffold(
          body: Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(12.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Entradas para Classificação',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    ElevatedButton.icon(
                      onPressed: vm.saveTaggedEntries,
                      icon: const Icon(Icons.save),
                      label: const Text("Salvar alterações"),
                    )
                  ],
                ),
              ),
              const Divider(),
              Expanded(
                child: RefreshIndicator(
                  onRefresh: () => vm.loadEntries(forceReload: true),
                  child: vm.isLoading
                      ? const Center(child: CircularProgressIndicator())
                      : vm.entriesToTag.isEmpty
                          ? ListView(
                              physics: const AlwaysScrollableScrollPhysics(),
                              children: const [
                                SizedBox(
                                  height:
                                      400, // altura mínima pra permitir o pull
                                  child: Center(
                                      child:
                                          Text("Nenhuma transação encontrada")),
                                ),
                              ],
                            )
                          : ListView.separated(
                              padding: const EdgeInsets.all(12),
                              itemCount: vm.entriesToTag.length,
                              separatorBuilder: (_, __) =>
                                  const Divider(height: 1),
                              itemBuilder: (context, index) {
                                final entry = vm.entriesToTag[index];
                                return TaggingEntryTile(
                                  entry: entry,
                                  tiposFinanceiros: vm.tiposFinanceiros,
                                  onChanged: (FinancialEntry updated) =>
                                      vm.updateEntry(index, updated),
                                  nomeController: vm.getNomeController(entry),
                                  notasController: vm.getNotasController(entry),
                                  contas:vm.accountsMap,
                                );
                              },
                            ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
