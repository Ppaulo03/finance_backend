import 'package:controle_financas/core/models/financial_entry.dart';
import 'package:controle_financas/core/viewmodels/financial_view_model.dart';


class AnalysisViewModel extends FinancialViewModel{

  String selectedCategory = "Todas";
  DateTime startDate = DateTime.now();
  DateTime endDate = DateTime.now();

  DateTime minDate = DateTime.now();
  DateTime maxDate = DateTime.now();

  List<FinancialEntry> get filteredEntries => _applyFilters();

  String selectedAnalysisType = 'Sumário';
  List<String> get availableGastosCategorias {
    final categorias = transacoes
        .where((e) => e.tipo == 'Gasto')
        .map((e) => e.categoria)
        .where((cat) => cat.isNotEmpty)
        .toSet()
        .toList();
    categorias.sort();
    return categorias;
  }

  final List<String> availableAnalysisTypes = [
    'Sumário',
    'Tendência',
    'Recorrência',
    'Previsão',
  ];

  AnalysisViewModel() {
    loadEntries();
  }

  Future<void> loadEntries({bool forceReload = false}) async {
    isLoading = true;
    notifyListeners();

    reload(force: forceReload);

    if (transacoes.isEmpty) {
      isLoading = false;
      notifyListeners();
      return;
    }

    minDate = transacoes.reduce((a, b) => a.data.isBefore(b.data) ? a : b).data;

    maxDate = transacoes.reduce((a, b) => a.data.isAfter(b.data) ? a : b).data;

    startDate = minDate;
    endDate = maxDate;

    isLoading = false;
    notifyListeners();
  }

  void setCategory(String? category) {
    selectedCategory = category ?? 'Todas';
    notifyListeners();
  }

  void setStartDate(DateTime date) {
    startDate = date;
    notifyListeners();
  }

  void setEndDate(DateTime date) {
    endDate = date;
    notifyListeners();
  }

  void setAnalysisType(String type) {
    selectedAnalysisType = type;
    notifyListeners();
  }

  bool isInRange(DateTime date) {
    return date.isAfter(startDate.subtract(const Duration(days: 1))) &&
        date.isBefore(endDate.add(const Duration(days: 1)));
  }

  List<FinancialEntry> _applyFilters() {
    return transacoes.where((entry) {
      final inCategory =
          selectedCategory == "Todas" || entry.categoria == selectedCategory;
      return inCategory && isInRange(entry.data) && entry.tipo == 'Gasto';
    }).toList();
  }

 
}
