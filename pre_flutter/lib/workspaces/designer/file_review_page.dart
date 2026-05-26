import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:vector_math/vector_math_64.dart' as v64;
import '../../core/annotation_engine/annotation_model.dart';
import '../../core/annotation_engine/annotation_painter.dart';
import '../../core/annotation_engine/viewport_provider.dart';
import '../../core/timeline_engine/timeline_model.dart';
import '../../core/state/workspace_state.dart';
import '../../domain/collaboration/providers/annotation_provider.dart';
import '../../domain/task_flow/providers/timeline_provider.dart';
import 'widgets/timeline_view.dart';

class FileReviewPage extends ConsumerStatefulWidget {
  final String fileId;
  const FileReviewPage({super.key, required this.fileId});
  
  @override
  ConsumerState<FileReviewPage> createState() => _FileReviewPageState();
}

class _FileReviewPageState extends ConsumerState<FileReviewPage> {
  final TransformationController _transformationController = TransformationController();
  AnnotationType _currentTool = AnnotationType.point;
  bool _isFocusMode = false;

  @override
  Widget build(BuildContext context) {
    final annotationsAsync = ref.watch(annotationListProvider(widget.fileId));
    final timelineAsync = ref.watch(timelineFetcherProvider(widget.fileId));
    final workspace = ref.watch(workspaceProvider);
    final viewport = ref.watch(viewportProvider);

    return CallbackShortcuts(
      bindings: {
        const SingleActivator(LogicalKeyboardKey.keyC): () => setState(() => _currentTool = AnnotationType.point),
        const SingleActivator(LogicalKeyboardKey.keyR): () => setState(() => _currentTool = AnnotationType.rect),
        const SingleActivator(LogicalKeyboardKey.keyF): () => setState(() => _isFocusMode = !_isFocusMode),
      },
      child: Focus(
        autofocus: true,
        child: Row(
          children: [
            // 1. 中间主画布
            Expanded(
              child: Column(
                children: [
                  _buildCanvasToolbar(),
                  Expanded(
                    child: annotationsAsync.when(
                      data: (list) => _buildCanvas(list, workspace.selectedAnnotationId, viewport),
                      loading: () => const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Center(child: Text("Error: $e")),
                    ),
                  ),
                ],
              ),
            ),
            
            // 2. 右侧协作区 (如果未开启 Focus Mode)
            if (!_isFocusMode && workspace.isCommentPanelOpen)
              _buildRightSidebar(timelineAsync, annotationsAsync, workspace.selectedAnnotationId),
          ],
        ),
      ),
    );
  }

  Widget _buildCanvas(List<AnnotationEntity> annotations, String? selectedId, ViewportState viewport) {
    // Focus Mode 逻辑：只看 Open 状态
    final filtered = _isFocusMode 
        ? annotations.where((a) => a.status == AnnotationStatus.open).toList()
        : annotations;

    return ClipRect(
      child: GestureDetector(
        onTapUp: _handleCanvasTap,
        child: InteractiveViewer(
          transformationController: _transformationController,
          boundaryMargin: const EdgeInsets.all(1000),
          minScale: 0.1,
          maxScale: 10.0,
          onInteractionUpdate: (details) {
            final matrix = _transformationController.value;
            final v64.Vector3 translation = matrix.getTranslation();
            ref.read(viewportProvider.notifier).updateTransform(
              matrix.getMaxScaleOnAxis(),
              Offset(translation.x, translation.y),
            );
          },
          child: Stack(
            children: [
              Center(
                child: Image.network(
                  "https://via.placeholder.com/1920x1080",
                  loadingBuilder: (context, child, progress) => progress == null ? child : const CircularProgressIndicator(),
                ),
              ),
              Positioned.fill(
                child: CustomPaint(
                  painter: AnnotationPainter(
                    annotations: filtered,
                    selectedId: selectedId,
                    scale: viewport.scale,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRightSidebar(AsyncValue<List<TimelineEvent>> timeAsync, AsyncValue<List<AnnotationEntity>> annAsync, String? selectedId) {
    return Container(
      width: 350,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(left: BorderSide(color: Color(0xFFE0E0E0))),
      ),
      child: DefaultTabController(
        length: 2,
        child: Column(
          children: [
            const TabBar(
              tabs: [Tab(text: "批注讨论"), Tab(text: "操作时间轴")],
              labelColor: Colors.blue,
              indicatorSize: TabBarIndicatorSize.label,
            ),
            Expanded(
              child: TabBarView(
                children: [
                  annAsync.when(
                    data: (list) => _buildCommentList(list, selectedId),
                    loading: () => const Center(child: CircularProgressIndicator()),
                    error: (e, _) => Text("Error: $e"),
                  ),
                  timeAsync.when(
                    data: (events) => TimelineView(events: events),
                    loading: () => const Center(child: CircularProgressIndicator()),
                    error: (e, _) => Text("Error: $e"),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCanvasToolbar() {
    return Container(
      height: 48,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(bottom: BorderSide(color: Color(0xFFE0E0E0))),
      ),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.menu_open), 
            onPressed: () => ref.read(workspaceProvider.notifier).toggleTaskQueue(),
            tooltip: "切换侧边栏 (Cmd+1)",
          ),
          const VerticalDivider(width: 20),
          const Text("设计稿 V3", style: TextStyle(fontWeight: FontWeight.bold)),
          const Spacer(),
          _buildToolBtn(AnnotationType.point, Icons.ads_click, "点选 (C)"),
          _buildToolBtn(AnnotationType.rect, Icons.crop_din, "矩形 (R)"),
          const VerticalDivider(width: 20),
          ActionChip(
            avatar: Icon(_isFocusMode ? Icons.visibility_off : Icons.visibility, size: 16),
            label: const Text("专注模式 (F)"),
            onPressed: () => setState(() => _isFocusMode = !_isFocusMode),
            backgroundColor: _isFocusMode ? Colors.blue[100] : null,
          ),
          const VerticalDivider(width: 20),
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green, foregroundColor: Colors.white),
            child: const Text("提交终稿"),
          ),
        ],
      ),
    );
  }

  Widget _buildToolBtn(AnnotationType type, IconData icon, String label) {
    final isSelected = _currentTool == type;
    return IconButton(
      icon: Icon(icon, color: isSelected ? Colors.blue : Colors.grey),
      tooltip: label,
      onPressed: () => setState(() => _currentTool = type),
    );
  }

  Widget _buildCommentList(List<AnnotationEntity> annotations, String? selectedId) {
    return ListView.builder(
      itemCount: annotations.length,
      itemBuilder: (context, index) {
        final ann = annotations[index];
        return _buildCommentCard(ann, ann.id == selectedId);
      },
    );
  }

  Widget _buildCommentCard(AnnotationEntity ann, bool isSelected) {
    final isResolved = ann.status == AnnotationStatus.resolved;
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      color: isSelected ? Colors.blue[50] : (isResolved ? Colors.grey[50] : Colors.white),
      elevation: 0,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: isSelected ? Colors.blue : const Color(0xFFEEEEEE)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(radius: 10, child: Text(ann.createdBy[0].toUpperCase(), style: const TextStyle(fontSize: 10))),
                const SizedBox(width: 8),
                Text("用户 #${ann.createdBy}", style: const TextStyle(fontWeight: FontWeight.bold)),
                const Spacer(),
                if (isResolved) const Icon(Icons.check_circle, color: Colors.green, size: 16),
              ],
            ),
            const SizedBox(height: 8),
            Text(ann.content, style: TextStyle(decoration: isResolved ? TextDecoration.lineThrough : null, color: isResolved ? Colors.grey : null)),
            if (!isResolved)
              Align(
                alignment: Alignment.centerRight,
                child: TextButton.icon(
                  icon: const Icon(Icons.done, size: 16),
                  label: const Text("Resolve"),
                  onPressed: () => ref.read(annotationControllerProvider(widget.fileId)).resolve(ann.id),
                ),
              )
          ],
        ),
      ),
    );
  }

  void _handleCanvasTap(TapUpDetails details) {
    final RenderBox box = context.findRenderObject() as RenderBox;
    final Offset local = box.globalToLocal(details.globalPosition);
    final nx = local.dx / box.size.width;
    final ny = (local.dy - 48) / (box.size.height - 48);
    
    final newAnn = AnnotationEntity(
        id: "temp_${DateTime.now().millisecondsSinceEpoch}",
        targetId: widget.fileId,
        targetType: "file",
        content: "改稿意见 #${DateTime.now().second}",
        type: _currentTool,
        normalizedRect: _currentTool == AnnotationType.rect 
            ? Rect.fromLTWH(nx, ny, 0.05, 0.05) 
            : Rect.fromLTWH(nx, ny, 0, 0),
        createdAt: DateTime.now(),
        createdBy: "me",
    );
    
    ref.read(annotationControllerProvider(widget.fileId)).addAnnotation(newAnn);
  }
}
