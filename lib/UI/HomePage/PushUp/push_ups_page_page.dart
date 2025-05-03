import 'dart:convert';
import 'dart:math';

import 'package:camera_webview/UI/HomePage/PushUp/push_ups_page_initial_params.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../camera_muti_person.dart';
import '../../../camera_webview.dart';
import 'push_ups_page_cubit.dart';

class PushUpsPagePage extends StatefulWidget {
  final PushUpsPageCubit cubit;
  // final UserDeInitialParams initialParams;
  const PushUpsPagePage({Key? key, required this.cubit}) : super(key: key);

  @override
  State<PushUpsPagePage> createState() => _PushUpsPagePageState();
}

class _PushUpsPagePageState extends State<PushUpsPagePage> {
  PushUpsPageCubit get cubit => widget.cubit;

  @override
  void initState() {
    super.initState();
    // TODO : Fix it Later
    cubit.onInit(PushUpsPageInitialParams());
    cubit.navigator.context = context;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Center(
            child: ElevatedButton(
                onPressed: () {
                  Random random = new Random();
                  int randomNumber =
                      random.nextInt(100); // from 0 upto 99 included

                  const username = 'abc';
                  const password = 'abc12';
                  final authHeader =
                      'Basic ${base64Encode(utf8.encode('$username:$password'))}';

                  Navigator.of(context).push(MaterialPageRoute(
                      builder: (context) => CameraMultiSocketIO(
                            roomId: 'room' + randomNumber.toString(),
                            exercise: 'DH',
                            authHeader: authHeader,
                          )));
                },
                child: Text('PushUp')),
          ),
        ],
      ),
    );
  }
}
