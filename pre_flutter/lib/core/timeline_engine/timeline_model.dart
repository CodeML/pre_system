enum TimelineEventType {
  upload,
  annotationCreated,
  annotationResolved,
  statusChanged,
  revisionCreated,
  fileLocked,
}

class TimelineEvent {
  final String id;
  final String targetId; // 文件或任务ID
  final TimelineEventType type;
  
  final String title;
  final String? content;
  
  final String creatorId;
  final String creatorName;
  final DateTime createdAt;
  
  final Map<String, dynamic>? metadata;

  TimelineEvent({
    required this.id,
    required this.targetId,
    required this.type,
    required this.title,
    this.content,
    required this.creatorId,
    required this.creatorName,
    required this.createdAt,
    this.metadata,
  });
}
