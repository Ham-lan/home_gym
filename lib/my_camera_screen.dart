import 'dart:async';
import 'dart:convert';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:socket_io_client/socket_io_client.dart' as socket_io;

class CameraSocketIO extends StatefulWidget {
  final String exercise;
  final String userId;

  const CameraSocketIO({required this.exercise, required this.userId, Key? key})
      : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraSocketIO> {
  CameraController? _controller;
  List<CameraDescription>? cameras;
  bool _isCameraInitialized = false;
  socket_io.Socket? _socket;
  String? _sid;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
    _initializeSocketIO();
  }

  Future<void> _initializeCamera() async {
    cameras = await availableCameras();
    _controller = CameraController(cameras!.first, ResolutionPreset.high);
    await _controller?.initialize();
    setState(() {
      _isCameraInitialized = true;
    });
    _startStreamingToServer();
  }

  void _initializeSocketIO() {
    const username = 'abc';
    const password = 'abc12';
    final authHeader =
        'Basic ${base64Encode(utf8.encode('$username:$password'))}';

    _socket = socket_io.io('http://192.168.10.38:5000', {
      'transports': ['websocket'],
      'extraHeaders': {'Authorization': authHeader},
    });

    _socket?.onConnect((_) {
      _sid = _socket?.id;
      debugPrint('Connected to /abc with sid: $_sid');
    });

    _socket?.on('new_video_frame', (data) {
      // Handle processed frame (e.g., display in Flutter UI)
      debugPrint('Received new video frame for ${widget.userId}');
    });

    _socket?.onDisconnect((_) => debugPrint('Disconnected from /abc'));
    _socket?.connect();
  }

  Future<String> _captureFrame() async {
    final image = await _controller?.takePicture();
    final bytes = await image!.readAsBytes();
    return base64Encode(bytes);
  }

  void _startStreamingToServer() {
    const username = 'abc';
    const password = 'abc12';
    final authHeader =
        'Basic ${base64Encode(utf8.encode('$username:$password'))}';

    Timer.periodic(const Duration(milliseconds: 500), (timer) async {
      // if (_sid == null) return; // Wait for SocketIO connection
      final videoData = await _captureFrame();
      final url =
          Uri.parse('http://192.168.10.38:5000/send_video?room_id=${'room15'}');

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authHeader,
        },
        body: json.encode({
          'videoData': videoData,
          // 'process': widget.exercise,
          // // 'sid': _sid, // Correct sid from SocketIO
          // 'userId': widget.userId,
        }),
      );

      if (response.statusCode == 200) {
        debugPrint('Video frame sent successfully');
      } else {
        debugPrint('Failed to send video frame: ${response.body}');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!_isCameraInitialized) {
      return const Center(child: CircularProgressIndicator());
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Home GYM')),
      body: CameraPreview(_controller!),
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    _socket?.disconnect();
    super.dispose();
  }
}
