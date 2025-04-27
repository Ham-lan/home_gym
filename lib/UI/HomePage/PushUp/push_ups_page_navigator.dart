import 'package:camera_webview/UI/HomePage/PushUp/push_ups_page_page.dart';
import 'package:flutter/material.dart';

import '../../../Navigation/navigator.dart';
import '../../../main.dart';
import 'push_ups_page_initial_params.dart';

class PushUpsPageNavigator with PushUpsPageRoute {
  PushUpsPageNavigator(this.navigator);
  @override
  // TODO: implement context
  late BuildContext context;

  @override
  // TODO: implement navigator
  AppNavigator navigator;
}

mixin PushUpsPageRoute {
  openPushUpsPagePage(PushUpsPageInitialParams initialParams) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => PushUpsPagePage(
              cubit: getIt(param1: initialParams),
            )));
  }

  BuildContext get context;
  AppNavigator get navigator;
}
