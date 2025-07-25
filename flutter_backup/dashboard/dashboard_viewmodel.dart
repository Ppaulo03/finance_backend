import 'package:controle_financas/core/models/financial_data.dart';
import 'package:controle_financas/core/models/financial_account.dart';
import 'package:controle_financas/core/listeners/financial_data_listener.dart';
import 'package:controle_financas/core/models/financial_entry.dart';
import 'package:controle_financas/core/models/financial_summary.dart';
import 'package:controle_financas/core/services/fetch_financial_data_service.dart';
import 'package:flutter/material.dart';

class DashboardViewModel extends ChangeNotifier
    implements FinancialDataListener {
  final _fectchFinancialDataService = FetchFinancialDataService();

  FinancialSummary? resumo;
  bool isLoading = true;

  DashboardViewModel() {
    loadResumo();
  }

  Future<void> loadResumo({bool forceReload = false}) async {
    isLoading = true;
    notifyListeners();

    final financialData = await _fectchFinancialDataService.fetchFinancialData(
        forceReload: forceReload);

    double saldoTotal = 0;
    Map<String, dynamic> saldoPorContaId = {};
    List<Map<String, dynamic>> saldoPorConta = [];

    for (FinancialEntry financa in financialData.financas) {
      saldoTotal += financa.valor;
      if (!saldoPorContaId.containsKey(financa.conta)) {
        saldoPorContaId[financa.conta] = 0;
      }
      saldoPorContaId[financa.conta] += financa.valor;
    }

    Map<String, FinancialAccount> contasDict = Map.fromEntries(
      financialData.accounts.map(
        (acc) => MapEntry(acc.id.toString(), acc),
      ),
    );

    for (String accId in saldoPorContaId.keys) {
      double value = saldoPorContaId[accId];
      if (contasDict.containsKey(accId)) {
        FinancialAccount acc = contasDict[accId]!;
        saldoTotal += acc.saldoInicial;
        saldoPorConta
            .add({"nome": acc.nome, "valor": acc.saldoInicial + value});
      } else {
        saldoPorConta.add({"nome": "Conta $accId", "valor": value});
      }
    }

    for (FinancialAccount acc in financialData.accounts) {
      if (!saldoPorContaId.containsKey(acc.id.toString())) {
        saldoPorConta.add({"nome": acc.nome, "valor": acc.saldoInicial});
      }
    }
    
    resumo = FinancialSummary.fromJson({
      "saldo_total": saldoTotal,
      "saldo_por_conta": saldoPorConta,
    });

    isLoading = false;
    notifyListeners();
  }

  @override
  void onFinancialDataUpdated(FinancialData data) {
    loadResumo();
    notifyListeners();
  }
}
