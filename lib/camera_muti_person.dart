import 'dart:async';
import 'dart:convert';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:socket_io_client/socket_io_client.dart' as socket_io;
import 'package:webview_flutter/webview_flutter.dart';

import 'package:webview_flutter_android/webview_flutter_android.dart';
import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';

class CameraMultiSocketIO extends StatefulWidget {
  final String exercise;
  final String roomId;
  final String authHeader;

  const CameraMultiSocketIO(
      {required this.exercise,
      required this.roomId,
      required this.authHeader,
      Key? key})
      : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraMultiSocketIO> {
  CameraController? _controller;
  List<CameraDescription>? cameras;
  bool _isCameraInitialized = false;
  socket_io.Socket? _socket;
  String? _sid;

  late final WebViewController _webViewController;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
    _initializeSocketIO();

    late final PlatformWebViewControllerCreationParams params;

    // String authHeader =
    //     'Basic ${base64Encode(utf8.encode('$username:$password'))}';

    if (WebViewPlatform.instance is WebKitWebViewPlatform) {
      params = WebKitWebViewControllerCreationParams(
        allowsInlineMediaPlayback: true,
        mediaTypesRequiringUserAction: const <PlaybackMediaTypes>{},
      );
    } else {
      params = const PlatformWebViewControllerCreationParams();
    }

    final WebViewController webViewController =
        WebViewController.fromPlatformCreationParams(params);

    webViewController
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(
          Uri.parse('http://192.168.10.38:5000/?room_id=${widget.roomId}'),
          headers: {'authorization': widget.authHeader});

    // Uri.parse('http://192.168.0.37:8080'));

    if (webViewController.platform is AndroidWebViewController) {
      AndroidWebViewController.enableDebugging(true);
      (webViewController.platform as AndroidWebViewController)
          .setMediaPlaybackRequiresUserGesture(false);
    }

    // TODO: Fix this
    _webViewController = webViewController;
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
      'extraHeaders': {'Authorization': widget.authHeader},
    });

    _socket?.onConnect((_) {
      _sid = _socket?.id;
      debugPrint('Connected to /abc with sid: $_sid');
    });

    _socket?.on('new_video_frame', (data) {
      // Handle processed frame (e.g., display in Flutter UI)
      debugPrint('Received new video frame for ${widget.roomId}');
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
    // const username = 'abc';
    // const password = 'abc12';
    // final authHeader =
    //     'Basic ${base64Encode(utf8.encode('$username:$password'))}';

    Timer.periodic(const Duration(milliseconds: 500), (timer) async {
      // if (_sid == null) return; // Wait for SocketIO connection
      final videoData = await _captureFrame();
      final url = Uri.parse(
          'http://192.168.10.38:5000/send_video?room_id=${widget.roomId}');

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': widget.authHeader,
        },
        body: json.encode({
          'videoData': videoData,
          // 'process': widget.exercise,
          // // 'sid': _sid, // Correct sid from SocketIO
          // 'roomId': widget.roomId,
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
      return Center(child: CircularProgressIndicator());
    } else {
      return Container(
        child: _webViewController != null
            ? SizedBox(
                height: 300,
                width: 300,
                child: WebViewWidget(controller: _webViewController!))
            : CircularProgressIndicator(),
      );
    }

    // if (!_isCameraInitialized) {
    //   return const Center(child: CircularProgressIndicator());
    // }
    // return Scaffold(
    //   appBar: AppBar(title: const Text('Home GYM')),
    //   body: CameraPreview(_controller!),
    // );
  }

  @override
  void dispose() {
    _controller?.dispose();
    _socket?.disconnect();
    super.dispose();
  }
}
