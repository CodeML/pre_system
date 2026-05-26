import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/timeline_engine/timeline_model.dart';
import '../../../core/network/api_client.dart';

class TimelineRepository {
  final Dio _dio;
  TimelineRepository(this._dio);

  Future<List<TimelineEvent>> getTimeline(String module, String targetId) async {
    final response = await _dio.get('/system/timeline/$module/$targetId');
    final List<dynamic> list = response.data;
    return list.map((item) => _mapJsonToEvent(item, targetId)).toList();
  }

  TimelineEvent _mapJsonToEvent(Map<String, dynamic> json, String targetId) {
    return TimelineEvent(
      id: "evt_${DateTime.now().millisecondsSinceEpoch}", 
      targetId: targetId,
      type: _parseType(json['action']),
      title: _formatTitle(json['action'], json['content']),
      content: json['content'],
      creatorId: json['user_id'].toString(),
      creatorName: "用户 ${json['user_id']}",
      createdAt: DateTime.parse(json['time']),
    );
  }

  TimelineEventType _parseType(String? action) {
    switch (action) {
      case 'create_comment': return TimelineEventType.annotationCreated;
      case 'resolve_comment': return TimelineEventType.annotationResolved;
      case 'update_status': return TimelineEventType.statusChanged;
      case 'lock': return TimelineEventType.fileLocked;
      default: return TimelineEventType.statusChanged;
    }
  }

  String _formatTitle(String? action, String? content) {
    return action ?? "业务变更";
  }
}

final timelineRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return TimelineRepository(dio);
});
