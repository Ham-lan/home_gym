import 'package:camera_webview/UI/HomePage/PullUp/pull_ups_page_initial_params.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'pull_ups_page_cubit.dart';

class PullUpsPagePage extends StatefulWidget {
  final PullUpsPageCubit cubit;
  // final UserDeInitialParams initialParams;
  const PullUpsPagePage({Key? key, required this.cubit}) : super(key: key);

  @override
  State<PullUpsPagePage> createState() => _PullUpsPagePageState();
}

class _PullUpsPagePageState extends State<PullUpsPagePage> {
  PullUpsPageCubit get cubit => widget.cubit;

  @override
  void initState() {
    super.initState();
    // TODO : Fix it Later
    cubit.onInit(PullUpsPageInitialParams());
    cubit.navigator.context = context;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body:
            // SingleChildScrollView(
            // child:
            Column(
      children: [Text('PullUps')],
    )
        // ),
        );
  }
}
