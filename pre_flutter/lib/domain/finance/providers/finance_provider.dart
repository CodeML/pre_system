import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/api_client.dart';

class FinanceRepository {
  final Dio _dio;
  FinanceRepository(this._dio);

  Future<List<dynamic>> getRiskAlerts() async {
    final response = await _dio.get('/finance/risk-alerts');
    return response.data;
  }

  Future<Map<String, dynamic>> getPayrollPreview(String month) async {
    final response = await _dio.get('/finance/payroll-preview', queryParameters: {'month': month});
    return response.data;
  }
}

final financeRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return FinanceRepository(dio);
});

final riskAlertsProvider = FutureProvider((ref) async {
  final repo = ref.watch(financeRepositoryProvider);
  return repo.getRiskAlerts();
});

final payrollPreviewProvider = FutureProvider.family<Map<String, dynamic>, String>((ref, month) async {
  final repo = ref.watch(financeRepositoryProvider);
  return repo.getPayrollPreview(month);
});
