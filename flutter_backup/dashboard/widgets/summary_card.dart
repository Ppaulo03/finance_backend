import 'package:flutter/material.dart';

class SummaryCard extends StatelessWidget {
  final String label;
  final double value;
  final Color? backgroundColor;
  final Color? textColor;

  const SummaryCard({
    super.key,
    required this.label,
    required this.value,
    this.backgroundColor,
    this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final formattedValue = value.toStringAsFixed(2).replaceAll('.', ',');

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
      color: backgroundColor ?? theme.colorScheme.primaryContainer,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      elevation: 3,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: theme.textTheme.titleMedium?.copyWith(
                color: textColor ?? theme.colorScheme.onPrimaryContainer,
                fontWeight: FontWeight.w600,
              ),
            ),
            Text(
              'R\$ $formattedValue',
              style: theme.textTheme.titleLarge?.copyWith(
                color: textColor ?? theme.colorScheme.onPrimaryContainer,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
