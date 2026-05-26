import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'annotation_model.dart';

class ViewportState {
  final double scale;
  final Offset offset;
  final Size canvasSize;

  ViewportState({
    this.scale = 1.0,
    this.offset = Offset.zero,
    this.canvasSize = const Size(1920, 1080),
  });

  ViewportState copyWith({double? scale, Offset? offset, Size? canvasSize}) {
    return ViewportState(
      scale: scale ?? this.scale,
      offset: offset ?? this.offset,
      canvasSize: canvasSize ?? this.canvasSize,
    );
  }
}

class ViewportNotifier extends Notifier<ViewportState> {
  @override
  ViewportState build() => ViewportState();

  void updateTransform(double scale, Offset offset) {
    state = state.copyWith(scale: scale, offset: offset);
  }
}

final viewportProvider = NotifierProvider<ViewportNotifier, ViewportState>(() {
  return ViewportNotifier();
});

class AnnotationListNotifier extends Notifier<List<AnnotationEntity>> {
  @override
  List<AnnotationEntity> build() => [];

  void setAnnotations(List<AnnotationEntity> items) {
    state = items;
  }

  // 核心：本地优先（Local-First）添加
  void addAnnotation(AnnotationEntity item) {
    // 1. 立即更新 UI (Optimistic Update)
    state = [...state, item];
    
    // 2. 后续：触发异步同步到后端 (Service.sync)
    _syncToServer(item);
  }

  // 核心：批注解决流
  void resolve(String id) {
    state = [
      for (final a in state)
        if (a.id == id) a.copyWith(status: AnnotationStatus.resolved) else a
    ];
    // 异步同步...
  }

  void _syncToServer(AnnotationEntity item) {
    // 逻辑占位：调用 API 同步
  }
}

final annotationProvider = NotifierProvider<AnnotationListNotifier, List<AnnotationEntity>>(() {
  return AnnotationListNotifier();
});

class SelectedAnnotationNotifier extends Notifier<String?> {
  @override
  String? build() => null;
  void select(String? id) => state = id;
}

final selectedAnnotationProvider = NotifierProvider<SelectedAnnotationNotifier, String?>(() {
  return SelectedAnnotationNotifier();
});
