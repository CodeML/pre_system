import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repository/task_repository.dart';
import '../../../core/network/api_client.dart';

final taskRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return TaskRepository(dio);
});

final taskQueueProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final repo = ref.watch(taskRepositoryProvider);
  return repo.getMyTasks();
});
