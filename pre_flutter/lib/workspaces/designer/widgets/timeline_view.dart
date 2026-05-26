import 'package:flutter/material.dart';
import '../../../core/timeline_engine/timeline_model.dart';

class TimelineView extends StatelessWidget {
  final List<TimelineEvent> events;

  const TimelineView({super.key, required this.events});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: events.length,
      itemBuilder: (context, index) {
        final event = events[index];
        final isLast = index == events.length - 1;

        return Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Column(
              children: [
                Container(
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                    color: _getEventColor(event.type),
                    shape: BoxShape.circle,
                  ),
                ),
                if (!isLast)
                  Container(
                    width: 2,
                    height: 50,
                    color: Colors.grey[300],
                  ),
              ],
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    event.title,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  if (event.content != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 4),
                      child: Text(
                        event.content!,
                        style: TextStyle(color: Colors.grey[600], fontSize: 13),
                      ),
                    ),
                  const SizedBox(height: 4),
                  Text(
                    "${event.creatorName} • ${event.createdAt.toString().substring(11, 16)}",
                    style: TextStyle(color: Colors.grey[400], fontSize: 11),
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ],
        );
      },
    );
  }

  Color _getEventColor(TimelineEventType type) {
    switch (type) {
      case TimelineEventType.upload: return Colors.blue;
      case TimelineEventType.annotationCreated: return Colors.orange;
      case TimelineEventType.annotationResolved: return Colors.green;
      case TimelineEventType.statusChanged: return Colors.purple;
      case TimelineEventType.fileLocked: return Colors.red;
      default: return Colors.grey;
    }
  }
}
