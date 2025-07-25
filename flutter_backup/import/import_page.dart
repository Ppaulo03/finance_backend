import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'import_viewmodel.dart';

class ImportPage extends StatelessWidget {
  const ImportPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ImportViewModel(),
      child: Scaffold(
        body: const Padding(
          padding: EdgeInsets.all(16),
          child: ImportForm(),
        ),
      ),
    );
  }
}

class ImportForm extends StatelessWidget {
  const ImportForm({super.key});

  Future<void> _pickFile(BuildContext context) async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv'],
    );

    if (result != null && result.files.single.path != null) {
      final file = File(result.files.single.path!);
      if (!context.mounted) return;
      context.read<ImportViewModel>().selectFile(file);
    }
  }

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<ImportViewModel>();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ElevatedButton.icon(
          icon: const Icon(Icons.upload_file),
          label: const Text("Selecionar CSV"),
          onPressed: () => _pickFile(context),
        ),
        const SizedBox(height: 16),
        if (viewModel.selectedFile != null)
          Text("Selecionado: ${viewModel.selectedFile!.path.split('/').last}"),
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: viewModel.selectedFile == null || viewModel.isUploading
              ? null
              : () => viewModel.upload(),
          child: viewModel.isUploading
              ? const CircularProgressIndicator()
              : const Text("Enviar para o servidor"),
        ),
        const SizedBox(height: 20),
        if (viewModel.statusMessage != null)
          Text(
            viewModel.statusMessage!,
            style: TextStyle(
              color: viewModel.statusMessage == "Importação concluída!"
                  ? Colors.green
                  : Colors.red,
            ),
          ),
      ],
    );
  }
}
