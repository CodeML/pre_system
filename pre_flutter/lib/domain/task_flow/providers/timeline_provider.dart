import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repository/timeline_repository.dart';
import '../../../core/timeline_engine/timeline_model.dart';
import '../../../core/network/api_client.dart';

final timelineRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return TimelineRepository(dio);
});

final timelineFetcherProvider = FutureProvider.family<List<TimelineEvent>, String>((ref, targetId) async {
  final repo = ref.watch(timelineRepositoryProvider);
  return repo.getTimeline("项目", targetId);
});
