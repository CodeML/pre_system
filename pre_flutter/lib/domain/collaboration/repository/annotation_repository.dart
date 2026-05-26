import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/annotation_engine/annotation_model.dart';
import '../../../core/network/api_client.dart';

class AnnotationRepository {
  final Dio _dio;
  AnnotationRepository(this._dio);

  Future<List<AnnotationEntity>> getAnnotations(String targetType, String targetId) async {
    final response = await _dio.get('/collaboration/comments/$targetType/$targetId');
    final List<dynamic> list = response.data;
    return list.map((item) => _mapJsonToEntity(item)).toList();
  }

  Future<AnnotationEntity> createAnnotation(AnnotationEntity entity) async {
    final payload = {
      'target_type': entity.targetType,
      'target_id': int.parse(entity.targetId),
      'content': entity.content,
      'pos_x': entity.x,
      'pos_y': entity.y,
      'width': entity.normalizedRect.width,
      'height': entity.normalizedRect.height,
      'page_index': entity.pageIndex,
      'artboard_id': entity.artboardId,
      'annotation_type': entity.type.name,
      'annotation_status': entity.status.name,
    };

    final response = await _dio.post('/collaboration/comments', data: payload);
    return _mapJsonToEntity(response.data);
  }

  Future<void> updateStatus(String id, AnnotationStatus status) async {
    await _dio.put('/collaboration/comments/$id/status/${status.name}');
  }

  AnnotationEntity _mapJsonToEntity(Map<String, dynamic> json) {
    return AnnotationEntity(
      id: json['id'].toString(),
      targetId: json['target_id'].toString(),
      targetType: json['target_type'],
      type: AnnotationType.values.firstWhere((e) => e.name == json['annotation_type'], orElse: () => AnnotationType.point),
      status: AnnotationStatus.values.firstWhere((e) => e.name == json['annotation_status'], orElse: () => AnnotationStatus.open),
      normalizedRect: Rect.fromLTWH(
        (json['pos_x'] as num?)?.toDouble() ?? 0,
        (json['pos_y'] as num?)?.toDouble() ?? 0,
        (json['width'] as num?)?.toDouble() ?? 0,
        (json['height'] as num?)?.toDouble() ?? 0,
      ),
      content: json['content'],
      createdBy: json['author_id'].toString(),
      createdAt: DateTime.parse(json['create_time']),
      artboardId: json['artboard_id'],
      pageIndex: json['page_index'] ?? 0,
    );
  }
}

final annotationRepositoryProvider = Provider((ref) {
  final dio = ref.watch(apiClientProvider);
  return AnnotationRepository(dio);
});
