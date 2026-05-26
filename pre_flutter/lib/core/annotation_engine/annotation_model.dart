import 'package:flutter/material.dart';

enum AnnotationType { point, rect, circle, arrow, freehand }
enum AnnotationStatus { open, resolved, ignored, reopened }

class AnnotationEntity {
  final String id;
  final String targetId;   // 关联的文件或任务ID
  final String targetType; // 'file' or 'task'
  
  final String? artboardId;
  final int pageIndex;

  final AnnotationType type;
  final AnnotationStatus status;

  // 使用 Rect 存储归一化坐标 (0.0 - 1.0)
  // 对于 point 类型，width/height 为 0
  final Rect normalizedRect;

  final String content;
  final String createdBy;
  final DateTime createdAt;
  
  final List<String> mentions;
  final int revisionRound;

  AnnotationEntity({
    required this.id,
    required this.targetId,
    required this.targetType,
    this.artboardId,
    this.pageIndex = 0,
    required this.type,
    this.status = AnnotationStatus.open,
    required this.normalizedRect,
    required this.content,
    required this.createdBy,
    required this.createdAt,
    this.mentions = const [],
    this.revisionRound = 1,
  });

  // 辅助 Getter
  double get x => normalizedRect.left;
  double get y => normalizedRect.top;

  AnnotationEntity copyWith({
    AnnotationStatus? status,
    String? content,
  }) {
    return AnnotationEntity(
      id: id,
      targetId: targetId,
      targetType: targetType,
      artboardId: artboardId,
      pageIndex: pageIndex,
      type: type,
      status: status ?? this.status,
      normalizedRect: normalizedRect,
      content: content ?? this.content,
      createdBy: createdBy,
      createdAt: createdAt,
      mentions: mentions,
      revisionRound: revisionRound,
    );
  }

  bool isHit(Offset normalizedPoint, {double threshold = 0.02}) {
    if (type == AnnotationType.point) {
      return (Offset(x, y) - normalizedPoint).distance < threshold;
    }
    return normalizedRect.contains(normalizedPoint);
  }
}
