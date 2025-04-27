import 'package:camera_webview/UI/HomePage/PushUp/push_ups_page_initial_params.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

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
      body: SingleChildScrollView(
        child: Column(
          children: [Text('PushUps')],
        ),
      ),
    );
  }
}
