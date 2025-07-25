import 'package:controle_financas/core/models/financial_account.dart';
import 'package:controle_financas/core/models/financial_categories.dart';
import 'package:controle_financas/core/models/financial_entry.dart';
import 'package:flutter/material.dart';

class TaggingEntryTile extends StatelessWidget {
  final FinancialEntry entry;
  final Map<String, FinancialType> tiposFinanceiros;
  final Map<String, FinancialAccount> contas;
  final ValueChanged<FinancialEntry> onChanged;
  final TextEditingController nomeController;
  final TextEditingController notasController;

  const TaggingEntryTile({
    super.key,
    required this.entry,
    required this.onChanged,
    required this.tiposFinanceiros,
    required this.nomeController,
    required this.notasController,
    required this.contas,
  });

  @override
  Widget build(BuildContext context) {
    final isTransfer = entry.tipo.toLowerCase() == 'transferência';
    final valueColor = isTransfer
        ? Colors.blue
        : entry.valor < 0
            ? Colors.red
            : Colors.green;
    final formattedDate =
        "${entry.data.day.toString().padLeft(2, '0')}/${entry.data.month.toString().padLeft(2, '0')}/${entry.data.year}";
    final formattedValue =
        "R\$ ${entry.valor.toStringAsFixed(2).replaceAll('.', ',')}";

    final tipoKeys = tiposFinanceiros.keys.toList();
    final tipo = tipoKeys.isEmpty
        ? ""
        : tipoKeys.contains(entry.tipo)
            ? entry.tipo
            : tipoKeys.first;

    final List<String> categoriaKeys = tipo == ""
        ? []
        : tiposFinanceiros[tipo]!.financialCategories.keys.toList();
    final categoria = categoriaKeys.isEmpty
        ? ""
        : categoriaKeys.contains(entry.categoria)
            ? entry.categoria
            : categoriaKeys.first;

    final List<String> subcategoriaKeys = categoria == ""
        ? []
        : tiposFinanceiros[tipo]!.financialCategories[categoria]!.subcategories;
    final subcategoria = subcategoriaKeys.isEmpty
        ? ""
        : subcategoriaKeys.contains(entry.subcategoria)
            ? entry.subcategoria
            : subcategoriaKeys.first;
    final String selectedConta =
        contas.isNotEmpty && contas.keys.contains(entry.conta)
            ? entry.conta
            : (contas.isNotEmpty ? contas.keys.first : "");

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(formattedDate,
                    style: Theme.of(context).textTheme.titleSmall),
                const Spacer(),
                Text(formattedValue,
                    style: Theme.of(context)
                        .textTheme
                        .titleLarge!
                        .copyWith(color: valueColor))
              ],
            ),
            Text(entry.destinoOrigem,
                style: Theme.of(context).textTheme.titleMedium),
            Text(entry.descricao,
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            tiposFinanceiros.isEmpty
                ? const CircularProgressIndicator()
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                        DropdownButton<String>(
                          value: selectedConta, 
                          onChanged: (value) => _update(entry.copyWith(conta: value), context),
                          items: contas.entries
                              .map((acc) => DropdownMenuItem(
                                  value: acc.key,
                                  child: Text(acc.value.nome)))
                              .toList(),
                        ),
                        const SizedBox(height: 8),
                        DropdownButton<String>(
                          value: tipo,
                          onChanged: (value) =>
                              _update(entry.copyWith(tipo: value), context),
                          items: tipoKeys
                              .map((tipo) => DropdownMenuItem(
                                  value: tipo, child: Text(tipo)))
                              .toList(),
                        ),
                        const SizedBox(height: 8),
                        DropdownButton<String>(
                          value: categoria,
                          onChanged: (value) => _update(
                              entry.copyWith(categoria: value), context),
                          items: categoriaKeys
                              .map((cat) => DropdownMenuItem(
                                  value: cat, child: Text(cat)))
                              .toList(),
                        ),
                        const SizedBox(height: 8),
                        DropdownButton<String>(
                          value: subcategoria,
                          onChanged: (value) => _update(
                              entry.copyWith(subcategoria: value), context),
                          items: subcategoriaKeys
                              .map((sub) => DropdownMenuItem(
                                  value: sub, child: Text(sub)))
                              .toList(),
                        ),
                        TextField(
                          controller: nomeController,
                          decoration: const InputDecoration(labelText: 'Nome'),
                          onChanged: (value) =>
                              _update(entry.copyWith(nome: value), context),
                        ),
                        const SizedBox(height: 8),
                        TextField(
                          controller: notasController,
                          decoration: const InputDecoration(labelText: 'Notas'),
                          onChanged: (value) =>
                              _update(entry.copyWith(notas: value), context),
                          maxLines: null,
                          minLines: 3,
                          keyboardType: TextInputType.multiline,
                        ),
                      ]),
          ],
        ),
      ),
    );
  }

  void _update(FinancialEntry updated, BuildContext context) {
    onChanged(updated);
  }
}
