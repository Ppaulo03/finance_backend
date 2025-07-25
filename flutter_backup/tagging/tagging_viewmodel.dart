// tagging_viewmodel.dart
import 'package:controle_financas/core/models/financial_entry.dart';
import 'package:controle_financas/core/models/financial_categories.dart';
import 'package:controle_financas/core/viewmodels/financial_view_model.dart';

import 'package:flutter/material.dart';

import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class TaggingViewModel extends FinancialViewModel {
  final Map<String, TextEditingController> _nomeControllers = {};
  TextEditingController getNomeController(FinancialEntry entry) {
    return _nomeControllers.putIfAbsent(entry.id.toString(), () {
      final controller = TextEditingController(text: entry.nome);
      controller.addListener(() {
        _updateNomeEntry(entry.copyWith(nome: controller.text));
      });
      return controller;
    });
  }

  final Map<String, TextEditingController> _notasControllers = {};
  TextEditingController getNotasController(FinancialEntry entry) {
    return _notasControllers.putIfAbsent(entry.id.toString(), () {
      final controller = TextEditingController(text: entry.nome);
      controller.addListener(() {
        _updateNotasEntry(entry.copyWith(nome: controller.text));
      });
      return controller;
    });
  }

  void disposeControllers() {
    for (final controller in _nomeControllers.values) {
      controller.dispose();
    }
    _nomeControllers.clear();

    for (final controller in _notasControllers.values) {
      controller.dispose();
    }
    _notasControllers.clear();
  }

  void _updateNotasEntry(FinancialEntry entryAtualizado) {}
  void _updateNomeEntry(FinancialEntry entryAtualizado) {}

  List<FinancialEntry> entriesToTag = [];
  bool isSaving = false;

  TaggingViewModel() {
    _loadCategories();
    loadEntries();
  }

  Future<void> _loadCategories() async {
    final jsonString =
        await rootBundle.loadString('assets/financial_categories.json');
    final Map<String, dynamic> rawJson = jsonDecode(jsonString);

    tiposFinanceiros = rawJson.map(
      (key, value) => MapEntry(key, FinancialType.fromJson(value)),
    );
  }

  Future<void> loadEntries({bool forceReload = false}) async {
    isLoading = true;
    notifyListeners();

    reload(force: forceReload);
    updateFunction();

    isLoading = false;
    notifyListeners();
  }

  @override
  Future<void> updateFunction() async {
    entriesToTag = transacoes.where((entry) => entry.needTagging).toList();
    disposeControllers();
  }

  void updateEntry(int index, FinancialEntry updated) {
    entriesToTag[index] = updated;
    notifyListeners();
  }

  Future<void> saveTaggedEntries() async {
    isSaving = true;
    notifyListeners();
    for (int idx = 0; idx < entriesToTag.length; idx++) {
      entriesToTag[idx] = entriesToTag[idx].copyWith(needTagging: false);
    }
    updateEntries(entriesToTag);

    isSaving = false;
    notifyListeners();
  }
}
