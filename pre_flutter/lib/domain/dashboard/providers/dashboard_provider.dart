import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/api_client.dart';

class DashboardRepository {
  final Dio _dio;
  DashboardRepository(this._dio);

  Future<Map<String, dynamic>> getOverview() async {
    final response = await _dio.get('/dashboard/overview');
    return response.data;
  }

  Future<Map<String, dynamic>> getTeamCapacity() async {
    final response = await _dio.get('/dashboard/capacity/team');
    return response.data;
  }
}

final dashboardRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return DashboardRepository(dio);
});

final dashboardOverviewProvider = FutureProvider((ref) async {
  final repo = ref.watch(dashboardRepositoryProvider);
  return repo.getOverview();
});

final teamCapacityProvider = FutureProvider((ref) async {
  final repo = ref.watch(dashboardRepositoryProvider);
  return repo.getTeamCapacity();
});
