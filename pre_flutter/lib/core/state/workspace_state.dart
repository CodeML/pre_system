import 'package:flutter_riverpod/flutter_riverpod.dart';

class WorkspaceState {
  final String? currentTaskId;
  final String? currentFileId;
  final int? currentRevisionRound;
  final String? selectedAnnotationId;
  
  // UI Panels
  final bool isTaskQueueOpen;
  final bool isTimelineOpen;
  final bool isCommentPanelOpen;

  WorkspaceState({
    this.currentTaskId,
    this.currentFileId,
    this.currentRevisionRound,
    this.selectedAnnotationId,
    this.isTaskQueueOpen = true,
    this.isTimelineOpen = false,
    this.isCommentPanelOpen = true,
  });

  WorkspaceState copyWith({
    String? currentTaskId,
    String? currentFileId,
    int? currentRevisionRound,
    String? selectedAnnotationId,
    bool? isTaskQueueOpen,
    bool? isTimelineOpen,
    bool? isCommentPanelOpen,
  }) {
    return WorkspaceState(
      currentTaskId: currentTaskId ?? this.currentTaskId,
      currentFileId: currentFileId ?? this.currentFileId,
      currentRevisionRound: currentRevisionRound ?? this.currentRevisionRound,
      selectedAnnotationId: selectedAnnotationId ?? this.selectedAnnotationId,
      isTaskQueueOpen: isTaskQueueOpen ?? this.isTaskQueueOpen,
      isTimelineOpen: isTimelineOpen ?? this.isTimelineOpen,
      isCommentPanelOpen: isCommentPanelOpen ?? this.isCommentPanelOpen,
    );
  }
}

class WorkspaceNotifier extends Notifier<WorkspaceState> {
  @override
  WorkspaceState build() => WorkspaceState();

  void selectTask(String taskId) {
    state = state.copyWith(currentTaskId: taskId, currentFileId: null);
  }

  void selectFile(String fileId) {
    state = state.copyWith(currentFileId: fileId);
  }

  void toggleTaskQueue() => state = state.copyWith(isTaskQueueOpen: !state.isTaskQueueOpen);
  void toggleTimeline() => state = state.copyWith(isTimelineOpen: !state.isTimelineOpen);
}

final workspaceProvider = NotifierProvider<WorkspaceNotifier, WorkspaceState>(() {
  return WorkspaceNotifier();
});
