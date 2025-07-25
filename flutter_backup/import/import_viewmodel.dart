import 'dart:io';
import 'package:controle_financas/core/services/backend_service.dart';
import 'package:controle_financas/core/services/fetch_financial_data_service.dart';
import 'package:flutter/material.dart';

class ImportViewModel extends ChangeNotifier {
  final _backendService = BackendService();
  final _fectchFinancialDataService = FetchFinancialDataService();

  File? selectedFile;
  bool isUploading = false;
  String? statusMessage;

  void selectFile(File file) {
    selectedFile = file;
    statusMessage = null;
    notifyListeners();
  }

  Future<void> upload() async {
    if (selectedFile == null) return;

    isUploading = true;
    statusMessage = null;
    notifyListeners();

    try {
      final success = await _backendService.uploadCsv(selectedFile!);
      statusMessage = success ? "Importação concluída!" : "Erro ao importar.";
      if (success) {
        await _fectchFinancialDataService.fetchFinancialData(forceReload: true);
      }
    } catch (e) {
      statusMessage = "Falha na conexão.";
    }

    isUploading = false;
    notifyListeners();
  }

  void reset() {
    selectedFile = null;
    statusMessage = null;
    notifyListeners();
  }
}
