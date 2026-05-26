import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/api_client.dart';

class TaskRepository {
  final Dio _dio;
  TaskRepository(this._dio);

  Future<List<Map<String, dynamic>>> getMyTasks() async {
    final response = await _dio.get('/task/list');
    return List<Map<String, dynamic>>.from(response.data);
  }
}

final taskRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return TaskRepository(dio);
});
